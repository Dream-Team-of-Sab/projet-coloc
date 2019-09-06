#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from db import db


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
    if form.get('yes'):
        prorata = "yes"
    elif form.get('no'):
        prorata = "no"
    details = form['details']
    cur.execute('''INSERT INTO Invoices (title, date, prorata,  price, details, id_paying_user)
                VALUES (?, ?, ?, ?, ?, ?)''', (title, date, prorata, price, details, id_user))
    db.commit()

def add_meal(form, id_user):
    cur = db.cursor()
    date = form['mdate']
    number = form['quantity']
    cur.execute('''INSERT INTO Meals (date, number, id_eating_user)
               VALUES (?, ?, ?)''', (date, number, id_user))
    db.commit()

def add_flat(form, user_id):
    cur = db.cursor()
    new_name = form['new_name']
    new_address = form['new_address']
    cur.execute('''INSERT INTO Colocations (name, address)
               VALUES (?, ?)''', (new_name, new_address))
        id_coloc = cur.execute('''SELECT id FROM Colocations WHERE name=?''', (new_name,))
    cur.execute('''UPDATE Users SET id_colocation=? WHERE id=?''', (id_coloc, id_user)
    db.commit()
