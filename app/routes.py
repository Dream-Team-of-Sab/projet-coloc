#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import sqlite3
import os
from flask import redirect, render_template, session, url_for, request
from app import app
from app import functions
from app import forms

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
        conn = sqlite3.connect('db/api_flat.db')
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
            return render_template('login.html', error = True)
        conn.close()
        return render_template('login.html', error = True)
    return 'Wrong http method. How did you get here ?!'

# sign up view
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    vue de la page de inscription
    """
    if request.method == 'GET':
        return render_template ('sign.html')
    elif request.method == 'POST':
        conn = sqlite3.connect('db/api_flat.db')
        cur = conn.cursor()
        email_list = cur.execute('SELECT email FROM Users').fetchone()
        conn.close()
        if request.form['email'] in email_list :
            return render_template('sign.html') #, existing_email = True)
        else:
            forms.signup(request.form)
            conn = sqlite3.connect('db/appi_flat.db')
            cur = conn.cursor()
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
            return render_template('index.html', modal=None)
        elif request.method == 'POST':
            id_user = session['logged']
            if request.form['index_btn'] == 'invoice':
                #Add invoice
                forms.add_invoice(request.form, id_user)
                conn = sqlite3.connect('db/api_flat.db')
                cur = conn.cursor()
                invoice_id = cur.execute('''SELECT id FROM Invoices
                                         WHERE (title = ? 
                                         AND date = ? 
                                         AND price = ? 
                                         AND details = ?
                                         AND id_paying_user = ?)''', (request.form['title'], request.form['date'], request.form['price'], request.form['details'], id_user)).fetchone()[0]
                conn.commit()
                conn.close()
                functions.upload_file(request.files['file'], invoice_id)
                return redirect(url_for('index'))
            elif request.form['index_btn'] == 'meal':
                forms.add_meal(request.form, id_user)
                return redirect(url_for('index'))
        else:
            return "Unknown method"

@app.route('/logout/', methods=['GET'])
def logout():
    del session['logged']
    return redirect(url_for('login'))
