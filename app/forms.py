#!/usr/bin/env python
'''Forms code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from app import db
from datetime import datetime

def signup(form):
    first_name = form['first_name']
    last_name = form['last_name']
    email = form['email']
    password = form['password']
    db.insert('users', 'first_name,last_name,email,password',\
                first_name, last_name, email, functions.crypted_string(password))

def add_invoice(form, user_id):
    title = form['title']
    date = form['date']
    price = form['price']
    inv = functions.file_date()+form['title']
    if form.get('yes'):
        prorata = "yes"
    elif form.get('no'):
        prorata = "no"
    details = form['details']
    db.insert('invoices', 'title, price, prorata, date, details, file_path, user_id',\
                title, price, prorata, date, details, inv, user_id)

def add_meal(form, user_id):
    cur = db.cursor()
    date = form['mdate']
    number = form['quantity']
    db.insert('meals','date, number, user_id', date, number, user_id)

def add_flat(form, user_id):
    new_name = form['new_name']
    new_address = form['new_address']
    new_password = form['new_password']
    db.insert('flat', 'name, address, password', new_name, new_address, functions.crypted_string(new_password))
    flat_id = db.select('flat_id', 'flat', name=new_name)[0][0]
    db.update('users', flat_id=flat_id, user_id=user_id)

def add_flatmate(form, user_id):
    flat_name = form['flat_name']
    flat_password = form['flat_password']
    name_exist = db.select('name', 'flat', name=flat_name)[0][0]
    if name_exist:
        pwd = db.select('password', 'flat', name=flat_name)[0][0]
        flat_id = db.select('flat_id', 'flat', name=flat_name)[0][0]
        if functions.crypted_string(flat_password) == pwd:
            db.update('users', flat_id=flat_id, user_id=user_id)
