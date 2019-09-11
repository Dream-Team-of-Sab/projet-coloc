#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from db import db
from datetime import datetime

def signup(form):
    cur = db.cursor()
    first_name = form['first_name']
    last_name = form['last_name']
    email = form['email']
    password = form['password']
    cur.execute('''
    		INSERT INTO users
		(first_name, last_name, email, password)
                VALUES (%s, %s, %s, %s)''',\
                (first_name, last_name, email, functions.crypted_string(password)))
    db.commit()
    db.rollback()

def add_invoice(form, id_user):
    cur = db.cursor()
    title = form['title']
    date = form['date']
    price = form['price']
    inv = functions.file_date()+form['title']
    if form.get('yes'):
        prorata = "yes"
    elif form.get('no'):
        prorata = "no"
    details = form['details']
    cur.execute('''
    		INSERT INTO invoices
		(title, price, prorata, date, details, file_path, id_user)
                VALUES (%s, %s, %s, %s, %s, %s, %s)''',\
		(title, price, prorata, date, details, inv, id_user))
    db.commit()
    db.rollback()

def add_meal(form, id_user):
    cur = db.cursor()
    date = form['mdate']
    number = form['quantity']
    cur.execute('''
    		INSERT INTO meals
		(date, number, id_user)
               	VALUES (%s, %s, %s)''',\
		(date, number, id_user))
    db.commit()
    db.rollback()

#def add_flat(form, id_user):
#   cur = db.cursor()
#   new_name = form['new_name']
#   new_address = form['new_address']
#   cur.execute('''
#   		INSERT INTO flats
#   		(name, address)
#       	VALUES (%s, %s)''',\
#       	(new_name, new_address))
#   id_coloc = cur.execute('''SELECT id FROM Colocations WHERE name=?''', (new_name,)).fetchone()[0]
#   cur.execute('''UPDATE Users SET id_colocation=? WHERE id=?''', (id_coloc, id_user))
#   db.commit()
