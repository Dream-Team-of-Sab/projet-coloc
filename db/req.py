#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db

def user_email(*args):
    if len(args) == 0:
        cur = db.cursor()
        cur.execute('SELECT email FROM users')
        email_list = [a[0] for a in cur.fetchall()]
        db.rollback
        return email_list

def user_id(email):
    cur = db.cursor()
    cur.execute('SELECT id FROM users WHERE email = %s', (email,))
    user_id = cur.fetchall()[0][0]
    db.rollback()
    return user_id

def sel_pwd(form):
    cur = db.cursor()
    execute('SELECT password FROM users WHERE email = %s',(form['email'],))
    pwd = cur.fetchall()[0][0]
    db.rollback()
    return pwd
