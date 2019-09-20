#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from db import db
from datetime import datetime
from flask import render_template
from mailjet_rest import Client

def send_mail(form):
    api_key = '4c392ed6313cbe35ff946c4a67bd5698'
    api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'
    cur = db.cursor()
    first_name = form['first_name']
    email = form['email']
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
            "Email": email,
            "Name": first_name
            }
        ],
        "Subject": "Inscription",
        "TextPart": "Inscription",
        "HTMLPart": "<h3>Bienvenue sur Api'Flat</h3>, <br>L'application de gestion de votre colocation.<br>Votre compte a été créé avec succès.</h3>",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)

def mail_to_friend(form, id_user):
    api_key = '4c392ed6313cbe35ff946c4a67bd5698'
    api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'
    cur = db.cursor()
    id_coloc = cur.execute('''SELECT id_colocation FROM Users
                        WHERE id=?''', (id_user,)).fetchone()[0]
    flat_name = cur.execute('''SELECT name FROM Colocations 
                        WHERE id=?''', (id_coloc,)).fetchone()[0]
    flat_password = form['flat_password']
    pwd = cur.execute('''SELECT password FROM Colocations
                        WHERE id=?''', (id_coloc,)).fetchone()[0]
    friend_name = form['friend_name']
    friend_email = form['friend_mail']
    response=0
    if friend_name and friend_email and flat_password:
        if functions.crypted_string(flat_password) != pwd:
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
                    "Email": friend_email,
                    "Name": friend_name
                    }
                ],
                "Subject": "Invitation sur Api'flat",
                "TextPart": "Invitation",
                "HTMLPart": "<h3>Bonjour <em> " +friend_name+ "<em>,</h3><br><p>Vous êtes invité à rejoindre le gestionnaire de colocation Api'flat. <br>Veuillez trouver ci-dessous les identifiants à renseigner lors de votre inscription. <br> Nom de la colocation : <em> " +flat_name+ "<em> <br>Mot de passe de la colocation : <em> " +flat_password+ "<em></p>",
                "CustomID": "AppGettingStartedTest"
                }
            ]
            }
            result = mailjet.send.create(data=data)
            response=2
    else:
        response=0
    return response

def file_date():
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%y_%H_%M_%S")
    return dt_string

def add_user(form):
    cur = db.cursor()
    first_name = form['first_name']
    last_name = form['last_name']
    email = form['email']
    password = form['password']
    flat_name = form['flat_name']
    flat_password = form['flat_password']
    response=0
    if flat_name:
        try:
            name_exist = cur.execute('''SELECT name from Colocations
                                    WHERE name=?''', (flat_name,)).fetchone()[0]
            pwd = cur.execute('''SELECT password FROM Colocations
                            WHERE name=?''', (flat_name,)).fetchone()[0]
            id_coloc = cur.execute('''SELECT id FROM Colocations
                            WHERE name=?''', (flat_name,)).fetchone()[0]
            db.commit()
            if functions.crypted_string(flat_password) != pwd:
                response=1
            else: 
                cur.execute('''INSERT INTO Users (first_name, last_name, email, password)
                        VALUES (?, ?, ?, ?)''',\
                (first_name, last_name, email, functions.crypted_string(password)))
                cur.execute('''UPDATE Users SET id_colocation=?
                        WHERE email=?''', (id_coloc, email))
                db.commit()
                response=4
        except:
            response=2
    else: 
        cur.execute('''INSERT INTO Users (first_name, last_name, email, password)
                VALUES (?, ?, ?, ?)''',\
        (first_name, last_name, email, functions.crypted_string(password)))
        db.commit()
        response=4
    return response

def add_invoice(form, id_user):
    cur = db.cursor()
    title = form['title']
    date = form['date']
    price = form['price']
    inv = file_date()+form['title']
    path_file = 'app/templates/uploads/'+inv
    if form.get('yes'):
        prorata = "yes"
    elif form.get('no'):
        prorata = "no"
    details = form['details']
    cur.execute('''INSERT INTO Invoices (title, date, prorata,  price, details, inv,id_paying_user)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (title, date, prorata, price, details, inv, id_user))
    db.commit()

def add_meal(form, id_user):
    cur = db.cursor()
    date = form['mdate']
    number = form['quantity']
    cur.execute('''INSERT INTO Meals (date, number, id_eating_user)
               VALUES (?, ?, ?)''', (date, number, id_user))
    db.commit()

def add_flat(form, id_user):
    cur = db.cursor()
    new_name = form['new_name']
    new_password = form['new_password']
    cur.execute('''INSERT INTO Colocations (name, password)
               VALUES (?, ?)''', (new_name, functions.crypted_string(new_password)))
    id_coloc = cur.execute('''SELECT id FROM Colocations WHERE name=?''', (new_name,)).fetchone()[0]
    cur.execute('''UPDATE Users SET id_colocation=? WHERE id=?''', (id_coloc, id_user))
    db.commit()

def add_person(form, id_user):
    cur = db.cursor()
    flat_name = form['flat_name']
    flat_password = form['flat_password']
    response=0
    try:
        name_exist = cur.execute('''SELECT name from Colocations
                                WHERE name=?''', (flat_name,)).fetchone()[0]
        pwd = cur.execute('''SELECT password FROM Colocations
                        WHERE name=?''', (flat_name,)).fetchone()[0]
        id_coloc = cur.execute('''SELECT id FROM Colocations
                            WHERE name=?''', (flat_name,)).fetchone()[0]
        if functions.crypted_string(flat_password) == pwd:
            cur.execute('''UPDATE Users SET id_colocation=?
                        WHERE id=?''', (id_coloc, id_user))
            response=2
        else:
            response=1
    except:
        response=1
    db.commit()
    return response
