#!/usr/bin/env python
'''Code api_flat in python'''
# -*- coding: utf-8 -*-

import sqlite3
import os
from flask import redirect, render_template, session, url_for, request
from werkzeug.utils import secure_filename
from app import app
from app import functions

UPLOAD_FOLDER = '/vagrant/app/projet-coloc/app/templates/uploads'

# login view
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    vue de la page de connexion
    """
    #Existing open session
    if 'logged' in session.keys():
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    #Login
    if request.method == 'POST':
        conn = sqlite3.connect('app/api_flat.db')
        cur = conn.cursor()
        user_mail_list = [a[0] for a in cur.execute('SELECT email FROM Users').fetchall()]
        if request.form['email'] in user_mail_list:
            pwd = cur.execute('SELECT password FROM Users WHERE email = ?',\
                            (request.form['email'],))\
                            .fetchone()[0]
            if functions.crypted_string(request.form['password']) == pwd:
                user_id = cur.execute('SELECT id FROM Users WHERE email = ?',\
                                    (request.form['email'],))\
                                    .fetchone()[0]
                conn.close()
                session['logged'] = user_id
                return redirect(url_for('index'))
            conn.close()
            return redirect(url_for('index'))
        conn.close()
        return redirect(url_for('index'))


# sign up view
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    vue de la page de inscription
    """
    if request.method == 'GET':
        return render_template ('sign.html')
    elif request.method == 'POST':
        conn = sqlite3.connect('app/api_flat.db')
        cur = conn.cursor()
        email_list = cur.execute('SELECT email FROM Users').fetchone()
        if request.form['email'] in email_list :
            conn.close()
            return render_template('sign.html') #, existing_email = True)
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            cur.execute('''INSERT INTO Users (first_name, last_name, email, password)
                         VALUES (?, ?, ?, ?)''',\
                         (first_name, last_name, email, functions.crypted_string(password)))
            conn.commit()
            user_id = cur.execute('SELECT id FROM Users WHERE email = ?', (email,)).fetchone()[0]
            session['logged'] = user_id
            conn.close()
            return redirect(url_for('index'))
    else:
        return "Unknown method"


# index view
@app.route('/index/', methods=['GET', 'POST'])
def index():
    """
    vue de la page d'accueil
    """
    if 'logged' not in session.keys():
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            conn = sqlite3.connect('app/api_flat.db')
            cur = conn.cursor()
            #Add invoice
            title = request.form['title']
            date = request.form['date']
            price = request.form['price']
            details = request.form['details']
            if request.form.get('yes'):
                cur.execute('''INSERT INTO Invoices (title, date, prorata,  price, details)
                                VALUES (?, ?, ?, ? ,?)''', (title, date, True, price, details))
            elif request.form.get('no'):
                cur.execute('''INSERT INTO Invoices (title, date, prorata,  price, details)
                                VALUES (?, ?, ?, ?, ?)''', (title, date, False, price, details))
            #Download invoice
            invoice = request.files['file']
            file_name = invoice.filename
            if invoice and functions.allowed_file(invoice.filename):
                file_name = secure_filename(invoice.filename)
                invoice.save(os.path.join(UPLOAD_FOLDER, file_name))
            #Add meal
            email = request.form['email']
            password = request.form['password']
            id_user = cur.execute('''SELECT id from Users
                                    WHERE email = ? AND password = ?''', (email, password)).fetchone()
            date = request.form['date']
            number = request.form['number']
            id_eating_user = id_user
            cur.execute('''INSERT INTO Meals (date, number, id_eating_user)
                        VALUES (?, ?, ?)''', (date, number, id_eating_user))
            #Add new colocation
            new_name = request.form['new_name']
            new_address = request.form['new_address']
            cur.execute('''INSERT INTO Colocations (name, address)
                        VALUES (?, ?)''', (new_name, new_address))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else:
            return "Unknown method"

@app.route('/logout/', methods=['GET'])
def logout():
    del session['logged']
    return redirect(url_for('login'))
