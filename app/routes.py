
import flask as fl
import hashlib
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

#cryptage des données
def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal.
    """
    b_string=string.encode() 
    crypted_str=hashlib.sha1(b_string) 
    return crypted_str.hexdigest() 


@app.route('/' , methods=['GET', 'POST'])
def accueil():
    if 'logged' in fl.session.keys():
        return fl.redirect('/' + crypted_string(str(fl.session['logged']))+'/')
    else:
        return render_template('login.html')


#vue de la page login
@app.route('/login.html/', methods=['GET', 'POST'])
def login():
    """
    Vue de la page de connexion
    """
    if 'logged' in fl.session.keys():
        return fl.redirect('/'+crypted_string(str(fl.session['logged']))+'/')
    else:
        if fl.request.method == 'GET':
            return fl.render_template('login.html')

        elif request.method == 'POST':
            conn = sqlite3.connect('db.db')
            c = conn.cursor()
            user_mail_list = [a[0] for a in c.execute('SELECT email FROM Users').fetchall()]                                                                                    
            if request.form['email'] in user_mail_list:
                pwd = c.execute('SELECT password FROM Users WHERE email = ?', (request.form['email'],)).fetchone()[0]
                if crypted_string(request.form['password']) == pwd:
                    user_id = c.execute('SELECT id_user FROM Users WHERE email = ?', (request.form['email'],)).fetchone()[0]
                    conn.close()
                    fl.session['logged'] = user_id
                    return fl.redirect('/'+crypted_string(str(user_id))+'/')
                else:
                    conn.close()
                    return fl.render_template('index.html', error = True)
            else:
                conn.close()
                return fl.render_template('index.html', error = True)
        else:
            return 'Unknown method'

#vue de la page sign
@app.route('/sign.html/', methods=['GET', 'POST'])        
def sign():
    """
    Vue de la page de inscription
    """
    if fl.request.method == 'GET':
        return fl.render_template('sign.html') 

    elif fl.request.method == 'POST':
        conn = sqlite3.connect('db.db') 
        c = conn.cursor()

        email_list = c.execute('SELECT email FROM Users').fetchone() 
        if fl.request.form['email'] in email_list : 
            conn.close() 
            return fl.render_template('sign.html', existing_email = True) 
        else:
            first_name = fl.request.form['first_name'] 
            last_name = fl.request.form['last_name']
            email = fl.request.form['email']
            password = fl.request.form['password']
            c.execute('''INSERT INTO Users (first_name, last_name, email, password)
                            VALUES (?, ?, ?, ?)''', (first_name, last_name, email, crypted_string(password))) 

            conn.commit()
            user_id = c.execute('SELECT id_user FROM Users WHERE email = ?', (email,)).fetchone()[0]
            fl.session['logged'] = user_id
            c = conn.close() 
            return fl.redirect('/'+ crypted_string(str(user_id)) +'/')
    else:
        return "Unknown method"

#vue de la page index
@app.route('/index.html/', methods=['GET', 'POST'])        
def index():
    """
    Vue de la page d'accueil
    """
    if fl.request.method == 'GET':
        return fl.render_template('index.html') 

 

   
if __name__ == "__main__":                     
    app.run(host = '0.0.0.0', debug = True)  
