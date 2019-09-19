#!/usr/bin/env python
'''Create database'''
# -*- coding: utf-8 -*-

from db import Database

# SQL requests
FLATS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS flats
		(flat_id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		address VARCHAR(255) NOT NULL);
		'''

USERS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS users
		(user_id SERIAL PRIMARY KEY,
		first_name VARCHAR(255) NOT NULL,
		last_name VARCHAR(255) NOT NULL,
		email VARCHAR(255) UNIQUE NOT NULL,
		password VARCHAR(255) NOT NULL,
		flat_id INTEGER,
			FOREIGN KEY (flat_id)
			REFERENCES flats (flat_id));
		'''

INVOICES_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS invoices
		(invoice_id SERIAL PRIMARY KEY,
		title VARCHAR(255) NOT NULL,
		price DECIMAL NOT NULL,
		prorata BOOLEAN NOT NULL,
		date DATE NOT NULL,
		details VARCHAR(255) NOT NULL,
		file_name VARCHAR(255),
		user_id INTEGER NOT NULL,
			FOREIGN KEY (user_id)
			REFERENCES users (user_id));
		'''

MEALS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS meals
		(meal_id SERIAL PRIMARY KEY,
		date DATE NOT NULL,
		number INTEGER NOT NULL,
		user_id INTEGER NOT NULL,
			FOREIGN KEY (user_id)
			REFERENCES users (user_id));
		'''

# Tables creation
table_list = [FLATS_TABLE_CREATE, USERS_TABLE_CREATE, INVOICES_TABLE_CREATE, MEALS_TABLE_CREATE]

db = Database(host='db', dbname='api_flat_dev', user='dev', password='youwillneverguess')
for sql_ins in table_list:
    db.create(sql_ins)
