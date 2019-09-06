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

def sel_pwd(form):
    cur = db.cursor()
    pwd = cur.execute('SELECT password FROM Users WHERE email = ?',\
                      (form['email'],)).fetchone()[0]
    return pwd
