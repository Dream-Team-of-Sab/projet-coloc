
import flask as fl
import hashlib
from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

#vue de la page login
@app.route('/login.html/')
def login():
    #if 'logged' in fl.session.keys():
        #return fl.redirect('/' + crypted_string(str(fl.session['logged']))+'/')
    #else:
    return render_template('login.html')

#vue de la page sign
@app.route('/sign.html/')        
def sign():
    return render_template('sign.html')


#vue de la page index
@app.route('/index.html/')        
def index():
    return render_template('index.html')

if __name__ == "__main__":                     
    app.run(host = 'localhost', debug = True)  