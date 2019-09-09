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

USER_MOCK_INSERT = ['''
		INSERT INTO users
		(first_name, last_name, email, password, id_flat)
		SELECT %s, %s, %s, %s, %s 
		WHERE NOT EXISTS (SELECT * FROM users WHERE id= %s)''',\
		('foo', 'bar', 'foo@bar', crypted_string('foofoobarbar'), 1, 1)]


INVOICE_MOCK_INSERT =['''
		INSERT INTO invoices
		(title, price, prorata, date, details, id_user)
		SELECT %s, %s, %s, %s, %s, %s
		WHERE NOT EXISTS (SELECT * FROM invoices WHERE id = %s)''',\
		('foo', 111.11, 'yes', '01/01/01', 'foo bar foo bar foo bar', 1, 1)]

# Database connexion
conn = psycopg2.connect("host=db dbname=api_flat_dev password=youwilneverguess")
cur = conn.cursor()

# Mocks creation
for sql_ins in [FLATS_TABLE_CREATE, USERS_TABLE_CREATE, INVOICES_TABLE_CREATE, MEALS_TABLE_CREATE]:
    cur.execute(sql_ins[0], sql_ins[1])
    conn.commit()
    conn.rollback()

# Closing database
conn.close()
