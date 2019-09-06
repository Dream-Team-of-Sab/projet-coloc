#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db

def user_email(*args):
    if len(args) == 0:
        cur = db.cursor()
        email_list = [a[0] for a in cur.execute('SELECT email FROM Users').fetchall()]
        return email_list

def user_id(email):
    cur = db.cursor()
    user_id = cur.execute('SELECT id FROM Users WHERE email = ?',\
    (email,)).fetchone()[0]
    return user_id

def invoice_id(form, id_user):
    cur = db.cursor()
    invoice_id = cur.execute('''SELECT id FROM Invoices
                             WHERE (title = ?
                             AND date = ?
                             AND price = ?
                             AND details = ?
                             AND id_paying_user = ?)''', (form['title'], form['date'], form['price'], form['details'], id_user)).fetchone()[0]
    return invoice_id

def sel_pwd(form, id_user):
    cur = db.cursor()
    pwd = cur.execute('SELECT password FROM Users WHERE email = ?',\
                      (form['email'],)).fetchone()[0]
    return pwd
