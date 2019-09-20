#!/usr/bin/env python
'''Views code of api_flat app'''
# -*- coding: utf-8 -*-

from flask import redirect, render_template, session, url_for, request
from app import db
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
        if request.form['email'] in [a[0] for a in db.select(db, db, 'email', 'users')]:
            if functions.crypted_string(request.form['password']) == db.select(db, 'password','users', email=request.form['email'])[0][0]:
                session['logged'] = db.select(db, 'user_id', 'users', email=request.form['email'])[0][0]
                return redirect(url_for('index'))
            return render_template('login.html', error=True)
        return render_template('login.html', error=True)
    return 'Unknown method'

# sign up view
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    vue de la page d'inscription
    """
    if 'logged' in session.keys():
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template ('sign.html')
    elif request.method == 'POST':
        if request.form['first_name'] == '' or request.form['last_name'] == ''  or request.form['email'] == ''  or request.form['password'] == '':
            return render_template('sign.html', nothing=True)
        elif request.form['email'] in [a[0] for a in db.select(db, 'email', 'users')]:
            return render_template('sign.html', existing_email=True)
        else:
            is_added = forms.add_user(request.form)
            if is_added == 0:
                return render_template('sign.html', nothing=True)
            elif is_added == 1:
                return render_template('sign.html', wrong_flat_password=True)
            elif is_added == 2:
                return render_template('sign.html', wrong_flat_name=True)
            else:
                functions.send_mail(request.form)
                session['logged'] = db.select(db, 'user_id', 'users', email=request.form['email'])[0][0]
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
            user_id = session['logged']
            flat_id = db.select(db, 'flat_id', 'users', user_id=user_id)[0][0]
            name_user = db.select(db, 'first_name','users', user_id=user_id)[0][0]
            if flat_id:
                name_flat = db.select(db, 'name', 'flats', flat_id=flat_id)[0][0]
                return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat)
            return render_template('index.html', flat=False, name_us=name_user)
        elif request.method == 'POST':
            user_id = session['logged']
            if request.form['index_btn'] == 'invoice':
                forms.add_invoice(request.form, user_id)
                functions.upload_file(request.files['file'])
                return redirect(url_for('index'))
            elif request.form['index_btn'] == 'meal':
                forms.add_meal(request.form, user_id)
                return redirect(url_for('index'))
        else:
            return "Unknown method"

#Invoices
@app.route('/invoice/', methods=['GET', 'POST'])
def invoice():
    """
    vue de la page permettant de voir toutes les factures de la colocation concernée
    """
    if 'logged' not in session.keys():
        return redirect(url_for('login'))
    if request.method == 'GET':
        list_invoice = db.select(db, 'title', 'date', 'price', 'invoices')
        return render_template('detail_facture.html', list_invoice = list_invoice)
    elif request.method == 'POST':
        user_id = session['logged']
        forms.add_invoice(request.form, user_id)
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
    if 'logged' not in session.keys():
        return redirect(url_for('login'))
    if request.method == 'GET':
#        user_id = session['logged']
#        flat_id = db.select(db, 'flat_id', 'users', user_id=user_id)[0][0]
#        if flat_id:
#            return render_template('invitation.html')
#        else:
#            return render_template('flat.html')
        return render_template('flat.html')
    elif request.method == 'POST':
        id_user = session['logged']
        if request.form['index_btn'] == 'flat':
            forms.add_flat(request.form, user_id)
            return redirect (url_for('index'))
        elif request.form['index_btn'] == 'person':
            forms.add_person(request.form, user_id)
            return redirect(url_for('index'))
    else:
        return "Unknown method"

@app.route('/logout/', methods=['GET'])
def logout():
    if session['logged']:
        del session['logged']
    return redirect(url_for('login'))
