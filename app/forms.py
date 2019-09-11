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
        "HTMLPart": "<h3>Bienvenue sur Api'Flat, l'appli de gestion de votre colocation. Votre compte a été créé avec succès",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)

def file_date():
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%y_%H_%M_%S")
    return dt_string

def signup(form):
    cur = db.cursor()
    first_name = form['first_name']
    last_name = form['last_name']
    email = form['email']
    password = form['password']
    cur.execute('''INSERT INTO Users (first_name, last_name, email, password)
                 VALUES (?, ?, ?, ?)''',\
                 (first_name, last_name, email, functions.crypted_string(password)))
    db.commit()

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
    new_address = form['new_address']
    new_password = form['new_password']
    cur.execute('''INSERT INTO Colocations (name, address, password)
               VALUES (?, ?, ?)''', (new_name, new_address, functions.crypted_string(new_password)))
    id_coloc = cur.execute('''SELECT id FROM Colocations WHERE name=?''', (new_name,)).fetchone()[0]
    cur.execute('''UPDATE Users SET id_colocation=? WHERE id=?''', (id_coloc, id_user))
    db.commit()

def add_person(form, id_user):
    cur = db.cursor()
    flat_name = form['flat_name']
    flat_password = form['flat_password']
    name_exist = cur.execute('''SELECT name from Colocations
                            WHERE name=?''', (flat_name,)).fetchone()[0]
    if name_exist is not None:
        pwd = cur.execute('''SELECT password FROM Colocations
                            WHERE name=?''', (flat_name,)).fetchone()[0]
        id_coloc = cur.execute('''SELECT id FROM Colocations
                            WHERE name=?''', (flat_name,)).fetchone()[0]
        if functions.crypted_string(flat_password) == pwd:
            cur.execute('''UPDATE Users SET id_colocation=?
                            WHERE id=?''', (id_coloc, id_user))
    db.commit()
