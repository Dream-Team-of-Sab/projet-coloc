#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from mailjet_rest import Client
from db import req

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
api_key = '4c392ed6313cbe35ff946c4a67bd5698'
api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'
UPLOAD_FOLDER = 'app/static/uploads'

def mail_to_friend(form, user_id):
    flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
    flat_name = req.select('name', 'flats', flat_id=flat_id)[0][0]
    pwd = req.select('password', 'flats', flat_id=flat_id)[0][0]
    response=0
    if 'friend_name' in form.keys() and 'friend_mail' in form.keys() and 'flat_password' in form.keys():
        if crypted_string(form['flat_password']) != pwd:
            response=1
        else:
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data = {
            'Messages': [
                {
                "From": {
                    "Email": "ribeiromaxance@gmail.com",
                    "Name": "Api'Flat"
                }, 
                "To": [
                    {
                    "Email": form['friend_mail'],
                    "Name": form['friend_name']
                    }
                ],
                "Subject": "Invitation sur Api'flat",
                "TextPart": "Invitation",
                "HTMLPart": "<h3>Bonjour <em> " +form['friend_name']+ "<em>,</h3><br><p>Vous êtes invité à rejoindre le gestionnaire de colocation Api'flat. <br>Veuillez trouver ci-dessous les identifiants à renseigner lors de votre inscription. <br> Nom de la colocation : <em> " +flat_name+ "<em> <br>Mot de passe de la colocation : <em> " +form['flat_password']+ "<em></p>",
                "CustomID": "AppGettingStartedTest"
                }
            ]
            }
            mailjet.send.create(data=data)
            response=2
    else:
        response=0
        
    print(response)
    return response

def send_mail(form):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "ribeiromaxance@gmail.com",
            "Name": "Api'Flat"
        },
        "To": [
            {
            "Email": form['email'],
            "Name": form['first_name']
            }
        ],
        "Subject": "Inscription",
        "TextPart": "Inscription",
        "HTMLPart": "<h3>Bienvenue sur Api'Flat, l'appli de gestion de votre colocation. Votre compte a été créé avec succès",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    #mailjet.send.create(data=data)

#cryptage des données
def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal au format str.
    """
    b_string=string.encode()
    crypted_str=hashlib.sha1(b_string)
    return crypted_str.hexdigest()

# Index view
def allowed_file(filename):
    """
    Récupère puis vérifie que l'extension est bien
    dans la liste des extensions autorisées
    """
    if '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def file_date():
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%y_%H_%M_%S")
    return dt_string

def str_to_date(string):
    date = datetime.strptime(string, "%d/%m/%Y")
    return date

def str_to_float(string):
    if ',' in string:
        result = float(string.replace(',', '.'))
    else:
        result = float(string)
    return result

def upload_file(up_file):
    """
    Fonction permettant d'uploader une photo de la facturette
    d'un utilisateur
    """
    file_name = up_file.filename
    if allowed_file(file_name):
        new_file_name = '_'.join([file_date(),file_name])
        up_file.save(os.path.join(UPLOAD_FOLDER, new_file_name))

def which_flat(user_id):
    flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
    return flat_id

def user_flatmates(user_id):
    flat_id = which_flat(user_id)
    flatmates = [a[0] for a in req.select('user_id', 'users', flat_id=flat_id)]
    return flatmates

def spent_by_user(user_id, month, prorata=False):
    spent_fee = req.select('price', 'date', 'prorata', 'invoices', user_id=user_id)
    this_month_fee = [a[0] for a in spent_fee if (a[1].month == month and a[2]==prorata)]
    return sum(this_month_fee)

def fee_by_pers(user_id, month):
    user_id_list = user_flatmates(user_id)
    all_fee = [spent_by_user(a, month) for a in user_id_list]
    fee_by_pers = sum(all_fee)/len(user_id_list)
    return fee_by_pers

def meals_number(user_id, month):
    meals_list = [a[0] for a in req.select('number', 'date', 'meals', user_id=user_id) if a[1].month == month]
    return sum(meals_list)

def meal_price(user_id_list, month):
    all_food_spent = sum([spent_by_user(a, month, prorata=True) for a in user_id_list])
    meals_sum = sum([meals_number(b, month) for b in user_id_list])
    meal_price = all_food_spent/meals_sum
    return meal_price

def food_balance(user_id, month):
    price = meal_price(user_flatmates(user_id), month)
    pos = spent_by_user(user_id, month, prorata=True)
    neg = meals_number(user_id, month) * price
    balance = pos - neg
    return balance

def overall_balance(user_id):
    today = datetime.now()
    month = today.month - 1
    overall_balance = food_balance(user_id, month) + float(spent_by_user(user_id, month)) - float(fee_by_pers(user_id, month))
    return overall_balance
