#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

from flask import redirect, render_template, session, url_for, request
from db import req
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
        if request.form['email'] in [a[0] for a in req.sel_data('email', 'users')]:
            if functions.crypted_string(request.form['password']) == req.sel_data('password','users', email=request.form['email'])[0][0]:
                session['logged'] = req.sel_data('id', 'users', email=request.form['email'])[0][0]
                return redirect(url_for('index'))
            return render_template('login.html', error=True)
        return render_template('login.html', error=True)
    return 'Unknown method'

# sign up view
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    vue de la page de inscription
    """
    if request.method == 'GET':
        return render_template ('sign.html')
    elif request.method == 'POST':
        if request.form['email'] in [a[0] for a in req.sel_data('email', 'users')]:
            return render_template('sign.html', existing_email=True)
        else:
            forms.signup(request.form)
            session['logged'] = req.sel_data('id', 'users', email=request.form['email'])[0][0]
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
            id_user = session['logged']
            id_flat = req.sel_data('id_flat', 'users', 'id'=id_users)[0][0]
            name_user = req.sel_data('first_name','users', 'id'=id_user)[0][0]
            if id_flat is None:
                return render_template('index.html', flat=False, name_us=name_user)
            name_flat = req.sel_data('name', 'flat', 'id'=id_flat)
            return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat)
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
        list_invoice = req.sel_data('title', 'date', 'price', 'invoices')
        return render_template('detail_facture.html', list_invoice = list_invoice)
    elif request.method == 'POST':
        id_user = session['logged']
        forms.add_invoice(request.form, id_user)
        functions.upload_file(request.files['file'])
        return redirect(url_for('invoice'))
    else:
        return "Unknown method"

#Add flat
@app.route('/flat/', methods=['GET', 'POST'])
def flat():
    """
    vue de la page ajout d'une colocation
    """
    if request.method == 'GET':
        return render_template('flat.html')
    if request.method == 'POST':
        id_user = session['logged']
        forms.add_flat(request.form, id_user)
        return redirect(url_for('index'))

@app.route('/logout/', methods=['GET'])
def logout():
    del session['logged']
    return redirect(url_for('login'))
