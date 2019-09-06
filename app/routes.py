#!/usr/bin/env python
'''View code of api_flat app'''
# -*- coding: utf-8 -*-

import os
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
            return render_template('sign.html') 
        else:
            forms.signup(request.form)
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
            return render_template('index.html')
        elif request.method == 'POST':
            id_user = session['logged']
            if request.form['index_btn'] == 'invoice':
                forms.add_invoice(request.form, id_user)
                functions.upload_file(request.files['file'], req.invoice_id(request.form, id_user))
                return redirect(url_for('index'))
            elif request.form['index_btn'] == 'meal':
                forms.add_meal(request.form, id_user)
                return redirect(url_for('index'))
        else:
            return "Unknown method"

#Add coloc
@app.route('/new-flat/', methods=['GET', 'POST'])
def flat():
    """
    vue de la page ajout d'une colocation
    """
    if request.method == 'GET':
        return render_template('new-flat.html')
    if request.method == 'POST':
        id_user = session['logged']
        forms.add_flat(request.form, id_user)
        return redirect(url_for('index'))

@app.route('/logout/', methods=['GET'])
def logout():
    del session['logged']
    return redirect(url_for('login'))
