#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
import sqlite3
import hashlib
from flask import redirect, render_template, session, url_for, request

#
def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal.
    """
    b_string = string.encode()
    crypted_str = hashlib.sha1(b_string)
    return crypted_str.hexdigest()

# Login view
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Vue de la page de connexion
    """
    if 'logged' in session.keys():
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        conn = sqlite3.connect('app/api_flat.db')
        cur = conn.cursor()
        user_mail_list = [a[0] for a in cur.execute('SELECT email FROM Users').fetchall()]
        if request.form['email'] in user_mail_list:
            pwd = cur.execute('SELECT password FROM Users WHERE email = ?',\
                            (request.form['email'],))\
                            .fetchone()[0]
            if crypted_string(request.form['password']) == pwd:
                user_id = cur.execute('SELECT id FROM Users WHERE email = ?',\
                                    (request.form['email'],))\
                                    .fetchone()[0]
                conn.close()
                session['logged'] = user_id
                return redirect(url_for('index'))

            conn.close()
            return redirect(url_for('index'))           # Il manque l'affichage  du message d'erreur
                                                            # coté html
        conn.close()
        return redirect(url_for('index'))

    return 'Unknown http method'


# Sign up view
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Vue de la page de inscription
    """
    if request.method == 'GET':
        return render_template('sign.html')

    elif request.method == 'POST':
        conn = sqlite3.connect('app/app_database.db')
        c = conn.cursor()
        email_list = c.execute('SELECT email FROM Users').fetchone()
        if request.form['email'] in email_list :
            conn.close()
            return render_template('sign.html') #, existing_email = True) # Il manque l'affichage du message
                                                                          # coté html

        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            cur.execute('''INSERT INTO Users (first_name, last_name, email, password)
                         VALUES (?, ?, ?, ?)''',\
                         (first_name, last_name, email, crypted_string(password)))

            conn.commit()
            user_id = cur.execute('SELECT id FROM Users WHERE email = ?', (email,)).fetchone()[0]
            session['logged'] = user_id
            cur.close()
            c = conn.close()
            return redirect(url_for('index'))
    else:
        return "Unknown method"


# Index view
@app.route('/index/', methods=['GET', 'POST'])
def index():
    """
    Vue de la page d'accueil
    """
    if 'logged' not in session.keys():
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('index.html')

        elif request.method == 'POST':
            conn = sqlite3.connect('app/app_database.db')
            cur = conn.cursor()
#Pour l'ajout de facture
#           invoice_list = cur.execute('SELECT title FROM Invoices').fetchone() 
#           if request.form['title'] in invoice_list :
#               cur.close() 
#               conn.close() 
#               return render_template('index.html') #, existing_title = True) !! Stopped here!
#           else:
            title = request.form['title']
            date = request.form['date']
            price = request.form['price']
            details = request.form['details']
            cur.execute('''INSERT INTO Invoices (title, date, price, details)
                            VALUES (?, ?, ?, ?)''', (title, date, price, details)
                       )
            conn.commit()
            return redirect(url_for('index'))
        else:
            return "Unknown method"

