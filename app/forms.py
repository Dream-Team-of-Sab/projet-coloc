#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from db import db
from datetime import datetime

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
    cur.execute('''INSERT INTO Colocations (name, address)
               VALUES (?, ?)''', (new_name, new_address))
    id_coloc = cur.execute('''SELECT id FROM Colocations WHERE name=?''', (new_name,)).fetchone()[0]
    cur.execute('''UPDATE Users SET id_colocation=? WHERE id=?''', (id_coloc, id_user))
    db.commit()
