#!/usr/bin/env python
'''Mocks for dev and tests'''
# -*- coding: utf-8 -*-

import psycopg2
from functions import crypted_string

# Mocks
FLAT_MOCK_INSERT = '''
		INSERT_INTO flat (id, name, address)
		SELECT 1, 'DT_FLAT', '6, rue de Rougemont, 75000, Paris, France'
		WHERE NOT EXISTS
		(SELECT * FROM flat WHERE id = 1)
		'''

USER_MOCK_INSERT = '''
 INSERT INTO users (id, first_name, last_name, email, password, flat_id)
 SELECT 1, foo, bar, foo@bar, {}, 1
 WHERE NOT EXISTS
 (SELECT * FROM users WHERE id = 1)
 '''.format(functions.crypted_string('youwillneverguess')


INVOICE_MOCK_INSERT = '''
 INSERT INTO invoices (id, title, price, prorata, date, details, file_path, id_user)
 SELECT 1, loyer, 29.99, yes, 01/01/01, details, app/templates/uploads/01_01_01_01_01.jpg, 1
 WHERE NOT EXISTS
 (SELECT * FROM users WHERE id = 1)
 '''

# Database connexion
conn = psycopg2.connect("host=db dbname=api_flat_dev password=youwilneverguess")
cur = conn.cursor()

# Mocks creation
for sql_ins in [FLATS_TABLE_CREATE, USERS_TABLE_CREATE, INVOICES_TABLE_CREATE, MEALS_TABLE_CREATE]:
    cur.execute(sql_ins)
    conn.commit()
    cur.rollback()

# Closing database
conn.close()
