#!/usr/bin/env python
'''Create database'''
# -*- coding: utf-8 -*-

from psycopg2 import connect
from random import randint
from datetime import datetime
from db import req
from app import functions


# SQL requests
FLATS_TABLE_CREATE = '''
		CREATE TABLE IF NOT EXISTS flats
		(flat_id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		address VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL);
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
		price NUMERIC(1000, 2) NOT NULL,
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

db = connect('host=db dbname=api_flat_dev user=dev password=youwillneverguess')
cur = db.cursor()
for sql_ins in table_list:
    cur.execute(sql_ins)
    db.commit()
    db.rollback()
db.close()

# Mocks creation
Us_name_list = {1:['Thomas', 'Barbot', 'tom_barbot@hotmail.fr'],\
                2:['Sabrina', 'Tony', 'sabrinatony74@gmail.com'],\
                3:['Maxance', 'Ribeiro', 'ribeiromaxance@gmail.com']}

req.insert('flats', 'name,address,password', 'api flat', '6 rue Rougemont, Paris', 'demo')
print('Flat data generated')

for a in Us_name_list.keys():
    password = 'uwillneverguess'
    req.insert('users', 'first_name,last_name,email,password,flat_id',\
                         Us_name_list[a][0],\
                         Us_name_list[a][1],\
                         Us_name_list[a][2],\
                         functions.crypted_string(password),\
                         1)
print('Users data generated')

Us_id_list = [a[0] for a in req.select('user_id', 'users')]
for b in range (randint(4, 15)):
    user_id = Us_id_list[randint(0, len(Us_id_list)-1)]
    user_n = req.select('first_name', 'last_name', 'users')[0]
    title = user_n[0]+'_'+user_n[1]+' invoice'
    price = randint(30, 600)
    prorata = False
    str_date = str(randint(1, 30))+'/08/2019'
    date = datetime.strptime(str_date, "%d/%m/%Y")
    details = 'details details details'
    req.insert('invoices', 'title,price,prorata,date,details,user_id', title, price, prorata, date, details, user_id)
print('Invoices data generated')

for c in Us_id_list:
    date_stock =list()
    for d in range (randint(10, 30)):
        str_date = str(randint(1, 30))+'/08/2019'
        date = datetime.strptime(str_date, "%d/%m/%Y")
        while date in date_stock:
            str_date = str(randint(1, 30))+'/08/2019'
            date = datetime.strptime(str_date, "%d/%m/%Y")
        date_stock.append(date)
        number = randint(1, 3)
        req.insert('meals', 'date,number,user_id', date, number, c)
print('Meals data generated')
