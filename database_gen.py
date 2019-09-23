#!/usr/bin/env python
'''Create database'''
# -*- coding: utf-8 -*-

from db import db

# SQL requests
FLATS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS flats
		(id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		address VARCHAR(255) NOT NULL);
		'''

USERS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS users
		(id SERIAL PRIMARY KEY,
		first_name VARCHAR(255) NOT NULL,
		last_name VARCHAR(255) NOT NULL,
		email VARCHAR(255) UNIQUE NOT NULL,
		password VARCHAR(255) NOT NULL,
		id_flat INTEGER,
			FOREIGN KEY (id_flat)
			REFERENCES flats (id));
		'''

INVOICES_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS invoices
		(id SERIAL PRIMARY KEY,
		title VARCHAR(255) NOT NULL,
		price DECIMAL NOT NULL,
		prorata VARCHAR(5) UNIQUE NOT NULL,
		date DATE NOT NULL,
		details VARCHAR(255) NOT NULL,
		file_path VARCHAR(255),
		id_user INTEGER NOT NULL,
			FOREIGN KEY (id_user)
			REFERENCES users (id));
		'''

MEALS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS meals
		(id SERIAL PRIMARY KEY,
		date DATE NOT NULL,
		number INTEGER NOT NULL,
		id_user INTEGER NOT NULL,
			FOREIGN KEY (id_user)
			REFERENCES users (id));
		'''

# Tables creation
table_list = [FLATS_TABLE_CREATE, USERS_TABLE_CREATE, INVOICES_TABLE_CREATE, MEALS_TABLE_CREATE]

cur = db.cursor()
for sql_ins in table_list:
    cur.execute(sql_ins)
    db.commit()
    db.rollback()

# Closing database
db.close()