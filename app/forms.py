#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from db import req
from datetime import datetime

def signup(form):
    first_name = form['first_name']
    last_name = form['last_name']
    email = form['email']
    password = form['password']
    req.ins_data('users', 'first_name,last_name,email,password',first_name, last_name, email, functions.crypted_string(password))

def add_invoice(form, id_user):
    title = form['title']
    date = form['date']
    price = form['price']
    inv = functions.file_date()+form['title']
    if form.get('yes'):
        prorata = "yes"
    elif form.get('no'):
        prorata = "no"
    details = form['details']
    req.ins_data('invoices', 'title,price,prorata,date,details,file_path,id_user', title, price, prorata, date, details, inv, id_user)

def add_meal(form, id_user):
    cur = db.cursor()
    date = form['mdate']
    number = form['quantity']
    req.ins_data('meals','date, number, id_user', date, number, id_user)

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
