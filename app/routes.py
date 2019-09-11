#!/usr/bin/env python
'''Views code of api_flat app'''
# -*- coding: utf-8 -*-

<<<<<<< Dashboard_func
from flask import redirect, render_template, session, url_for, request, jsonify
from db import req
=======
import os
from flask import redirect, render_template, session, url_for, request
<<<<<<< Dashboard_func
from db import db, req
>>>>>>> everything ready to merge with dev
=======
from db import req
from db import db
>>>>>>> Ajout vue "Détail Facture" et affichage dynamique des factures
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
        if request.form['email'] in [a[0] for a in req.select('email', 'users')]:
            if functions.crypted_string(request.form['password']) == req.select('password','users', email=request.form['email'])[0][0]:
                session['logged'] = req.select('user_id', 'users', email=request.form['email'])[0][0]
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
<<<<<<< Dashboard_func
        forms.add_user(request.form)
        session['logged'] = req.select('user_id', 'users', email=request.form['email'])[0][0]
        return redirect(url_for('index'))
=======
        if request.form['email'] in req.user_email():
            return render_template('sign.html') 
        else:
            forms.signup(request.form)
            forms.send_mail(request.form)
            session['logged'] = req.user_id(request.form['email'])
            return redirect(url_for('index'))
>>>>>>> function send_mail
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
<<<<<<< Dashboard_func
<<<<<<< Dashboard_func
            user_id = session['logged']
            flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
            name_user = req.select('first_name','users', user_id=user_id)[0][0]
            if flat_id:
                name_flat = req.select('name', 'flats', flat_id=flat_id)[0][0]
                return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat, flat_id=flat_id)
            return render_template('index.html', flat=False, name_us=name_user)
=======
            id_user = session['logged']
            forms.home_text(request.form, id_user)
>>>>>>> add text in home
=======
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
>>>>>>> everything ready to merge with dev
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

<<<<<<< Dashboard_func
#Invoices
@app.route('/invoice/', methods=['GET', 'POST'])
def invoice():
    """
    vue de la page permettant de voir toutes les factures de la colocation concernée
    """
    if 'logged' not in session.keys():
        return redirect(url_for('login'))
    if request.method == 'GET':
        list_invoice = req.select('title', 'date', 'price', 'invoices')
        return render_template('detail_facture.html', list_invoice = list_invoice)
    elif request.method == 'POST':
        user_id = session['logged']
        forms.add_invoice(request.form, user_id)
=======


#Invoices
@app.route('/invoice/', methods=['GET', 'POST'])
def invoice(): 
    """
    vue de la page permettant de voir toutes les factures de la colocation concernée
    """
    if request.method == 'GET':
        cur = db.cursor()
        list_invoice = cur.execute('''SELECT title FROM Invoices ''').fetchall()
        invoice = [i[0] for i in list_invoice]
        db.commit()
        return render_template('detail_facture.html', list_invoice = list_invoice)
    elif request.method == 'POST':
        id_user = session['logged']
        forms.add_invoice(request.form, id_user)
>>>>>>> Ajout vue "Détail Facture" et affichage dynamique des factures
        functions.upload_file(request.files['file'])
        return redirect(url_for('invoice'))
    else:
        return "Unknown method"

<<<<<<< Dashboard_func
#Add flat
=======
    


#Add coloc
>>>>>>> Ajout vue "Détail Facture" et affichage dynamique des factures
@app.route('/flat/', methods=['GET', 'POST'])
def flat():
    """
    vue de la page ajout d'une colocation
    """
    if 'logged' not in session.keys():
        return redirect(url_for('login'))
    if request.method == 'GET':
#        user_id = session['logged']
#        flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
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

@app.route('/get_data/<int:flat_id>')
def dashboard_data(flat_id):
    working_list = [a[0] for a in db.select('user_id', 'users', flat_id=flat_id)]
    result = []
    for user_id in working_list:
        user_names = db.select('first_name', 'last_name', 'users', user_id=user_id)[0]
        json_disc = {
            "name" : user_names[0]+' '+user_names[1],
            "balance": round(functions.overall_balance(user_id), 2)
        }
        result.append(json_disc)
    return jsonify(result)

@app.route('/logout/', methods=['GET'])
def logout():
    if session['logged']:
        del session['logged']
    return redirect(url_for('login'))



