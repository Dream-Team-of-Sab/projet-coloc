#!/usr/bin/env python
'''Mocks for dev and tests'''
# -*- coding: utf-8 -*-

import psycopg2
from functions import crypted_string

# Mocks
FLAT_MOCK_INSERT = ['''
		INSERT INTO flats
		(name, address)
		SELECT %s, %s
		WHERE NOT EXISTS (SELECT * FROM users WHERE id=%s)''',\
		('dt_flat', '6, rue de Rougemont, 75000, Paris, France', 1)]

USER_A_MOCK_INSERT = ['''
		INSERT INTO users
		(first_name, last_name, email, password, id_flat)
		SELECT %s, %s, %s, %s, %s 
		WHERE NOT EXISTS (SELECT * FROM users WHERE id= %s)''',\
		('a', 'a', 'a_mail@foo.bar', crypted_string('foofoobarbar'), 1, 1)]

USER_B_MOCK_INSERT = ['''
		INSERT INTO users
		(first_name, last_name, email, password, id_flat)
		SELECT %s, %s, %s, %s, %s 
		WHERE NOT EXISTS (SELECT * FROM users WHERE id= %s)''',\
		('b', 'b', 'b_mail@foo.bar', crypted_string('foofoobarbar'), 1, 2)]

USER_C_MOCK_INSERT = ['''
		INSERT INTO users
		(first_name, last_name, email, password, id_flat)
		SELECT %s, %s, %s, %s, %s 
		WHERE NOT EXISTS (SELECT * FROM users WHERE id= %s)''',\
		('c', 'c', 'c_mail@foo.bar', crypted_string('foofoobarbar'), 1, 3)]

USER_D_MOCK_INSERT = ['''
		INSERT INTO users
		(first_name, last_name, email, password, id_flat)
		SELECT %s, %s, %s, %s, %s 
		WHERE NOT EXISTS (SELECT * FROM users WHERE id= %s)''',\
		('d', 'd', 'd_mail@foo.bar', crypted_string('foofoobarbar'), 1, 4)]

INVOICE_MOCK_INSERT =['''
		INSERT INTO invoices
		(title, price, prorata, date, details, id_user)
		SELECT %s, %s, %s, %s, %s, %s
		WHERE NOT EXISTS (SELECT * FROM invoices WHERE id = %s)''',\
		('foo', 111.11, 'yes', '01/01/01', 'foo bar foo bar foo bar', 1, 1)]

# Database connexion
conn = psycopg2.connect("host=db dbname=api_flat_dev user=dev password=youwillneverguess")
cur = conn.cursor()

# Mocks creation
for sql_ins in [FLATS_MOCK_INSERT, USERS_MOCK_INSERT, INVOICES_MOCK_INSERT]:
    cur.execute(sql_ins[0], sql_ins[1])
    conn.commit()
    conn.rollback()

# Generate mocks meals


# Closing database
conn.close()
