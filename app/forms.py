#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import sqlite3
import os
from app import functions


def signup(form):
    conn = sqlite3.connect('db/api_flat.db')
    cur = conn.cursor()
    first_name = form['first_name']
    last_name = form['last_name']
    email = form['email']
    password = form['password']
    cur.execute('''INSERT INTO Users (first_name, last_name, email, password)
                 VALUES (?, ?, ?, ?)''',\
                 (first_name, last_name, email, functions.crypted_string(password)))
    conn.commit()
    conn.close()

def add_invoice(form, id_user):
    conn = sqlite3.connect('db/api_flat.db')
    cur = conn.cursor()
    title = form['title']
    date = form['date']
    price = form['price']
    if form.get('yes'):
        prorata = "yes"
    elif form.get('no'):
        prorata = "no"
    details = form['details']
    cur.execute('''INSERT INTO Invoices (title, date, prorata,  price, details, id_paying_user)
                VALUES (?, ?, ?, ?, ?, ?)''', (title, date, prorata, price, details, id_user))
    conn.commit()
    conn.close()

def add_meal(form, id_user):
    conn = sqlite3.connect('db/api_flat.db')
    cur = conn.cursor()
    date = form['mdate']
    number = form['quantity']
    cur.execute('''INSERT INTO Meals (date, number, id_eating_user)
               VALUES (?, ?, ?)''', (date, number, id_user))
    conn.commit()
    conn.close()

#Add new colocation
#   new_name = request.form['new_name']
#   new_address = request.form['new_address']
#   cur.execute('''INSERT INTO Colocations (name, address)
#               VALUES (?, ?)''', (new_name, new_address))
