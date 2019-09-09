#!/usr/bin/env python
'''Create database'''
# -*- coding: utf-8 -*-

import psycopg2

# SQL requests
FLATS_TABLE_CREATE = '''
    		CREATE TABLE IF NOT EXISTS flats (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	name VARCHAR(255) NOT NULL,
        	address VARCHAR(255) NOT NULL
    		);
    		'''

USERS_TABLE_CREATE = '''
    		CREATE TABLE IF NOT EXISTS users (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	first_name VARCHAR(255) NOT NULL,
        	last_name VARCHAR(255) NOT NULL,
        	email VARCHAR(255) UNIQUE NOT NULL,
        	password VARCHAR(255) NOT NULL,
        	id_colocation INTEGER,
        	FOREIGN KEY (id_colocation)
        	REFERENCES Colocations (id)
    		);
    		'''

INVOICES_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS invoices (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title VARCHAR(255) NOT NULL,
		price DECIMAL NOT NULL,
		prorata VARCHAR (5) NOT NULL,
		date DATE NOT NULL,
		details VARCHAR(255) NOT NULL,
		file_path VARCHAR(255) , 
		id_user INTEGER NOT NULL,
		FOREIGN KEY (id_paying_user)
		REFERENCES Users (id)
		);
		'''

MEALS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS meals (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		date DATE NOT NULL,
		number INT NOT NULL,
		id_eating_user INTEGER,
		FOREIGN KEY (id_eating_user)
		REFERENCES Users (id)
		);
		'''

# Database connexion
conn = psycopg2.connect("host=db dbname=api_flat_dev password=youwillneverguess")
cur = conn.cursor()

# Tables creation
for sql_ins in [FLATS_TABLE_CREATE, USERS_TABLE_CREATE, INVOICES_TABLE_CREATE, MEALS_TABLE_CREATE]:
    cur.execute(sql_ins)
    conn.commit()
    cur.rollback()

# Closing database
conn.close()
