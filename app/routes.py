#!/usr/bin/env python
'''Views code of api_flat app'''
# -*- coding: utf-8 -*-

from flask import redirect, render_template, session, url_for, request, jsonify
from db import req
from app import app
from app import functions
from app import forms

#login view
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    vue de la page de connexion
    """
    #Existing open session
    if 'logged' in session.keys():
#        return redirect(url_for('index'))
        response = redirect(url_for('index'))
    else:
        if request.method == 'GET':
#            return render_template('login.html')
            response = render_template('login.html')
        #Login
        if request.method == 'POST':
            if request.form['email'] == " " or request.form['password'] == "":
#                return render_template('login.html', nothing=True)
                response = render_template('login.html', nothing=True)
            elif request.form['email'] in [a[0] for a in req.select('email', 'users')]:
                if functions.crypted_string(request.form['password']) != req.select('password','users', email=request.form['email'])[0][0]:
#                    return render_template('login.html', error=True)
                    response = render_template('login.html', error=True)
                else:
                    session['logged'] = req.select('user_id', 'users', email=request.form['email'])[0][0]
#                    return redirect(url_for('index'))
                    response = redirect(url_for('index'))
            else:
#                return render_template('login.html', error=True)
                response = render_template('login.html', error=True)
        else:
            response = 'Unknown method'
    return response

# sign up view
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    vue de la page d'inscription
    """
    if 'logged' in session.keys():
#        return redirect(url_for('index'))
        response = redirect(url_for('index'))
    else:
        if request.method == 'GET':
#            return render_template('sign.html')
            response = render_template('sign.html')
        elif request.method == 'POST':
#<<<    <<<< Dashboard_func
#<<<    <<<< Dashboard_func
            forms.add_user(request.form)
            session['logged'] = req.select('user_id', 'users', email=request.form['email'])[0][0]
#            return redirect(url_for('index'))
            response = redirect(url_for('index'))
#            if request.form['first_name'] == '' or request.form['last_name'] == ''  or request.form['email'] == ''  or request.form['password'] == '':
#                return render_template('sign.html', nothing=True)
#            elif request.form['email'] in req.user_email():
#>>>    >>>> debugg + errors messages
#                return render_template('sign.html', existing_email=True)
#            else:
#<<<    <<<< Dashboard_func
#                forms.add_user(request.form)
#                forms.send_mail(request.form)
#                session['logged'] = req.user_id(request.form['email'])
#                cur = db.cursor()
#                email = request.form['email']
#                flat_name = request.form['flat_name']
#                flat_password = request.form['flat_password']
#                if flat_name:
#                    try:
#                        name_exist = cur.execute('''SELECT name from Colocations
#                                            WHERE name=?''', (flat_name,)).fetchone()[0]
#                    except:
#                        return render_template('sign.html', wrong_flat_name=True)
#
#                   # if name_exist is None:
#                   #     return render_template('sign.html', wrong_flat_name=True)
#                   # if name_exist is not None:
#                   #     pwd = cur.execute('''SELECT password FROM Colocations
#                   #                     WHERE name=?''', (flat_name,)).fetchone()[0]
#                   #     id_coloc = cur.execute('''SELECT id FROM Colocations
#                   #                     WHERE name=?''', (flat_name,)).fetchone()[0]
#                   #     if functions.crypted_string(flat_password) != pwd:
#                   #         return render_template('sign.html', wrong_flat_password=True)
#                    #    elif functions.crypted_string(flat_password) == pwd:
#                    #        cur.execute('''UPDATE Users SET id_colocation=?
#                     #                   WHERE email=?''', (id_coloc, email))
#                #db.commit()
#                return redirect(url_for('index'))
#>>>    >>>> function send_mail
#===    ====
#                is_added = forms.add_user(request.form)
#                if is_added == 0:
#                    return render_template('sign.html', nothing=True)
#                elif is_added == 1:
#                    return render_template('sign.html', wrong_flat_password=True)
#                elif is_added == 2:
#                    return render_template('sign.html', wrong_flat_name=True)
#                else:
#                    forms.send_mail(request.form)
#                    session['logged'] = req.user_id(request.form['email'])
#                    return redirect(url_for('index'))
#>>>    >>>> add error message
        else:
            response = "Unknown method"
    return response

# index view
@app.route('/index/', methods=['GET', 'POST'])
def index():
    """
    vue de la page d'accueil
    """
    if 'logged' not in session.keys():
#        return redirect(url_for('login'))
        response = redirect(url_for('login'))
    else:
        user_id = session['logged']
        if request.method == 'GET':
            flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
            name_user = req.select('first_name','users', user_id=user_id)[0][0]
            if flat_id:
                name_flat = req.select('name', 'flats', flat_id=flat_id)[0][0]
#                return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat, flat_id=flat_id)
                response = render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat, flat_id=flat_id)
#            return render_template('index.html', flat=False, name_us=name_user)
            response = render_template('index.html', flat=False, name_us=name_user)
            forms.home_text(request.form, user_id)
            flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
            name_user = req.select('first_name', 'users', user_id=user_id)[0][0]
            if flat_id is None:
#                return render_template('index.html', flat=False, name_us=name_user)
                response = render_template('index.html', flat=False, name_us=name_user)
            else:
                flat_name = req.select('name','flat', flat_id=flat_id)[0][0]
#                return render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat)
                response = render_template('index.html', flat=True, name_us=name_user, name_fl=name_flat)
        elif request.method == 'POST':
            if request.form['index_btn'] == 'invoice':
                forms.add_invoice(request.form, user_id)
                functions.upload_file(request.files['file'])
#                return redirect(url_for('index'))
                response = redirect(url_for('index'))
            elif request.form['index_btn'] == 'meal':
                forms.add_meal(request.form, user_id)
                response = redirect(url_for('index'))
        else:
            response = "Unknown method"
    return response

#Invoices
@app.route('/invoice/', methods=['GET', 'POST'])
def invoice():
    """
    vue de la page permettant de voir toutes les factures de la colocation concernée
    """
    if 'logged' not in session.keys():
#        return redirect(url_for('login'))
        response = redirect(url_for('login'))
    else:
        user_id = session['logged']
        if request.method == 'GET':
            list_invoice = req.select('title', 'date', 'price', 'invoices')
#            return render_template('detail_facture.html', list_invoice = list_invoice)
            response = render_template('detail_facture.html', list_invoice = list_invoice)
        elif request.method == 'POST':
            user_id = session['logged']
            forms.add_invoice(request.form, user_id)
            functions.upload_file(request.files['file'])
            response = redirect(url_for('invoice'))
        else:
            response = "Unknown method"
    return response

#Add flat
@app.route('/flat/', methods=['GET', 'POST'])
def flat():
    """
    vue de la page ajout d'une colocation
    """
    if 'logged' not in session.keys():
#        return redirect(url_for('login'))
        response = redirect(url_for('login'))
    else:
        user_id = session['logged']
        if request.method == 'GET':
             flat_id = req.select('flat_id', 'users', user_id=user_id)[0][0]
             if flat_id:
#                 return render_template('invitation.html')
                 response = render_template('invitation.html')
             else:
#                 return render_template('flat.html')
                 response = render_template('flat.html')
        elif request.method == 'POST':
            if request.form['index_btn'] == 'flat':
                forms.add_flat(request.form, user_id)
                forms.mail_to_friend(request.form)
#                return redirect (url_for('index'))
                response = redirect(url_for('index'))
            elif request.form['index_btn'] == 'person':
                forms.add_person(request.form, user_id)
#                return redirect(url_for('index'))
                response = redirect(url_for('index'))
        else:
#            return "Unknown method"
            response = "Unknown method"
    return response

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

#Invitation ami
@app.route('/invitation/', methods=['GET', 'POST'])
def invitation():
    """
    vue de la page invitation d'un individu à rejoindre la colocation
    """
    if 'logged' not in session.keys():
#        return redirect(url_for('login'))
        response = redirect(url_for('login'))
    else:
        user_id = session['logged']
        if request.method == 'GET':
            response = render_template('invitation.html')
        elif request.method == 'POST':
            send_mail = forms.mail_to_friend(request.form, user_id)
            if send_mail == 0:
#                return render_template('invitation.html', error=True)
                response = render_template('invitation.html', error=True)
            elif send_mail == 1:
#                return render_template('invitation.html', wrong_password=True)
                response = render_template('invitation.html', wrong_password=True)
            else:
#                return redirect(url_for('index'))
                response = redirect(url_for('index'))
        else:
            response = "Unknown method"
    return response

@app.route('/logout/', methods=['GET'])
def logout():
    if session['logged']:
        del session['logged']
    return redirect(url_for('login'))
