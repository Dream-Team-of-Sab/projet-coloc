#!/usr/bin/env python

import psycopg2
import hashlib
from flask import redirect, render_template, session, url_for, request
from app import app
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

#
def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal.
    """
    b_string=string.encode()
    crypted_str=hashlib.sha1(b_string)
    return crypted_str.hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Login view
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Vue de la page de connexion
    """
    if 'logged' in session.keys():
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            conn = psycopg2.connect("host=localhost dbname=app user=postgres password=postgres")
            cur = conn.cursor()
            user_mail_list = [a[0] for a in cur.execute('SELECT email FROM Users').fetchall()]
            if request.form['email'] in user_mail_list:
                pwd = cur.execute('SELECT password FROM Users WHERE email = %s',\
                                (request.form['email'],))\
                                .fetchone()[0]
                if crypted_string(request.form['password']) == pwd:
                    user_id = cur.execute('SELECT id FROM Users WHERE email = %s',\
                                        (request.form['email'],))\
                                        .fetchone()[0]
                    cur.close()
                    conn.close()
                    session['logged'] = user_id
                    return redirect(url_for('index'))
                else:
                    cur.close()
                    conn.close()
                    return render_template('login', error = True)
            else:
                cur.close()
                conn.close()
                return render_template('login', error = True)
        else:
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
        conn = psycopg2.connect("host=localhost dbname=app user=app password=app")
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
                         VALUES (%s, %s, %s, %s)''',\
                         (first_name, last_name, email, crypted_string(password)))

            conn.commit()
            user_id = cur.execute('SELECT id FROM Users WHERE email = %s', (email,)).fetchone()[0]
            session['logged'] = user_id
            cur.close()
            conn.close()
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
            conn = psycopg2.connect("host=localhost dbname=app user=app password=app")
            cur = conn.cursor()
            title = request.form['title']
            date = request.form['date']
            price = request.form['price']
            details = request.form['details']
            cur.execute('''INSERT INTO Invoices (title, date, price, details)
                            VALUES (%s, %s, %s, %s)''', (title, date, price, details)
                       )
            invoice = request.files['file']
            file_name = invoice.filename
            if invoice and allowed_file(invoice.filename):
                file_name = secure_filename(invoice.filename)
                invoice.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            return "Unknown method"

