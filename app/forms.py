#!/usr/bin/env python
'''Forms code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from app import functions
from db import req
from datetime import datetime
from flask import render_template

def add_user(form):
    req.insert('users', 'first_name,last_name,email,password',\
                        form['first_name'],\
                        form['last_name'],\
                        form['email'],\
                        functions.crypted_string(form['password']))

#def add_user(form):
#    response=0
#    if form['flat_name']:
#        try:
#            name_exist = req.select('name', 'flats', name=form['flat_name'])[0][0]
#            pwd = req.select('password', 'flats', name=form['flat_name'])[0][0]
#            flat_id = req.select('flat_id', 'flats', name=form['flat_name'])[0][0]
#            if functions.crypted_string(form['flat_password']) != pwd:
#                response=1
#            else:
#                req.insert('users', 'first_name,last_name,email,password',\
#                                    form['first_name'],\
#                                    form['last_name'],\
#                                    form['email'],\
#                                    functions.crypted_string(form['password']))
#                req.update('users', flat_id=flat_id, email=form['email'])
#                response=4
#        except:
#            response=2
#    else:
#        req.insert('users', 'first_name,last_name,email,password',\
#                            form['first_name'],\
#                            form['last_name'],\
#                            form['email'],\
#                            functions.crypted_string(form['password']))
#        response=4
#    return response

<<<<<<< Dashboard_func
def add_invoice(form, user_id):
    file_name = functions.file_date()+form['title']
    req.insert('invoices', 'title,price,prorata,date,details,file_name,user_id',\
                form['title'],\
                form['price'],\
                bool(form.get('yes')),\
                form['date'],\
                form['details'],\
                file_name,\
                user_id)
=======
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
>>>>>>> Ajout vue "Détail Facture" et affichage dynamique des factures

def add_meal(form, user_id):
    req.insert('meals','date, number, user_id',\
                        form['mdate'],\
                        form['quantity'],\
                        user_id)

def add_flat(form, user_id):
    req.insert('flat', 'name, address, password',\
                        form['new_name'],\
                        form['new_adresse'],\
    functions.crypted_string(new_password))
    flat_id = req.select('flat_id', 'flat', name=new_name)[0][0]
    req.update('users', flat_id=flat_id, user_id=user_id)

def add_flatmate(form, user_id):
    name_exist = req.select('name', 'flat', name=flat_name)[0][0]
    if name_exist:
        pwd = req.select('password', 'flat', name=form['flat_name'])[0][0]
        flat_id = req.select('flat_id', 'flat', name=form['flat_name'])[0][0]
        if functions.crypted_string(flat_password) == pwd:
<<<<<<< Dashboard_func
            req.update('users', flat_id=flat_id, user_id=user_id)
=======
            cur.execute('''UPDATE Users SET id_colocation=?
                            WHERE id=?''', (id_coloc, id_user))
    db.commit()
<<<<<<< Dashboard_func

def home_text(form, id_user):
    cur= db.cursor()
    id_coloc = cur.execute('''SELECT id_colocation FROM Users 
                        WHERE id=?''', (id_user,)).fetchone()[0]
    name_user = cur.execute('''SELECT first_name FROM Users
  ¦   ¦   ¦   ¦   ¦   ¦ WHERE id=?''', (id_user,)).fetchone()[0]
    name_flat = cur.execute('''SELECT name FROM Colocations
      ¦   ¦   ¦   ¦   ¦ WHERE id=? ''', (id_coloc,)).fetchone()[0]
    if id_coloc is None:
        return render_template('index.html', flat=False, name_user=name_us)
    elif id_coloc is not None:
      ¦ return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat) 
    db.commit()
>>>>>>> add text in home
=======
>>>>>>> everything ready to merge with dev
