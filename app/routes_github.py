#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
from flask import redirect, render_template, session, url_for, request
from db import req
from db import db
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
        if request.form['email'] in req.user_email():
            if functions.crypted_string(request.form['password']) == req.sel_pwd(request.form):
                session['logged'] = req.user_id(request.form['email'])
                return redirect(url_for('index'))
            return render_template('login.html', error=True)
        return render_template('login.html', error=True)
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
        if request.form['email'] in req.user_email():
            return render_template('sign.html', existing_email=True) 
        else:
            forms.signup(request.form)
            forms.send_mail(request.form)
            session['logged'] = req.user_id(request.form['email'])
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
            cur = db.cursor()
            id_user = session['logged']
            id_coloc = cur.execute('''SELECT id_colocation FROM Users
                                WHERE id=?''', (id_user,)).fetchone()[0]
            name_user = cur.execute('''SELECT first_name FROM Users
                                WHERE id=?''', (id_user,)).fetchone()[0]
            if id_coloc is None:
                return render_template('index.html', flat=False, name_us=name_user)
            elif id_coloc is not None:
                name_flat = cur.execute('''SELECT name FROM Colocations
                                    WHERE id=? ''', (id_coloc,)).fetchone()[0]
                return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat)
            db.commit()
        elif request.method == 'POST':
            id_user = session['logged']
            if request.form['index_btn'] == 'invoice':
                forms.add_invoice(request.form, id_user)
                functions.upload_file(request.files['file'])
                return redirect(url_for('index'))
            elif request.form['index_btn'] == 'meal':
                forms.add_meal(request.form, id_user)
                return redirect(url_for('index'))
        else:
            return "Unknown method"



#Invoices
@app.route('/invoice/', methods=['GET', 'POST'])
def invoice(): 
    """
    vue de la page permettant de voir toutes les factures de la colocation concernée
    """
    if request.method == 'GET':
        cur = db.cursor()
        list_invoice = cur.execute('''SELECT title, date, price FROM Invoices''').fetchall()
        invoice = [i for i in list_invoice]
        db.commit()
        return render_template('detail_facture.html', list_invoice = invoice)
    elif request.method == 'POST':
        id_user = session['logged']
        forms.add_invoice(request.form, id_user)
        functions.upload_file(request.files['file'])
        return redirect(url_for('invoice'))
    else:
        return "Unknown method"

#Add coloc
@app.route('/flat/', methods=['GET', 'POST'])
def flat():
    """
    vue de la page ajout d'une colocation
    """
    if request.method == 'GET':
        return render_template('flat.html')
    elif request.method == 'POST':
        id_user = session['logged']
        if request.form['index_btn'] == 'flat':
            if req.sel_data('users', 'id_flat', user_id = session['logged']) not True:
                forms.add_flat(request.form, id_user)
                return redirect(url_for('index'))
            return redirect(url_for('flat')) # Manque ('Deja dans une colocation') cote front
        elif request.form['index_btn'] == 'person':
            if request.form['flat_name'] in [a[0] for a in req.sel_data('name', 'flat')]:
                if functions.crypted_string(request.form['flat_password'])\
                        == req.sel_data('password', 'flat', name=request.form['flat_name'])[0][0]:
                    forms.add_person(request.form, id_user)
                    return redirect(url_for('index'))
                return  redirect(url_for('flat')) # Manque ('Mauvais mot de passe') cote front
            return redirect(url_for('flat')) # Manque ('Nom inconnu') cote front
    else:
        return "Unknown method"

@app.route('/logout/', methods=['GET'])
def logout():
    del session['logged']
    return redirect(url_for('login'))



