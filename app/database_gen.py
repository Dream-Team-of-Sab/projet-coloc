#!/usr/bin/env python
'''Create database'''
# -*- coding: utf-8 -*-

import psycopg2
from functions import crypted_string

#Ouverture connexion
CONN = psycopg2.connect("host=localhost dbname=app user=app password=app")
CUR = CONN.cursor()

CUR.execute(
    '''
    CREATE TABLE IF NOT EXISTS Colocations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL
    );
    '''
)
CUR.execute( 
    '''
    CREATE TABLE IF NOT EXISTS Users (
    	id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
	id_colocation INTEGER,
	    FOREIGN KEY (id_colocation)
       	REFERENCES Colocations (id) 
    );
    '''
)
CUR.execute(
    '''
    CREATE TABLE IF NOT EXISTS Invoices (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        price DECIMAL NOT NULL,
	type BOOL NOT NULL,
	date DATE NOT NULL,
	details VARCHAR(255) NOT NULL,
	id_paying_user INTEGER,
	    FOREIGN KEY (id_paying_user)
	    REFERENCES Users (id)
    );
    '''
)
CUR.execute(
    '''
    CREATE TABLE IF NOT EXISTS Meals (
        id SERIAL PRIMARY KEY,
	date DATE NOT NULL,
        number FLOAT NOT NULL,
        id_eating_user INTEGER,
	    FOREIGN KEY (id_eating_user)
	    REFERENCES Users (id)
    );
    '''
)
#Ajout colocation
COLOC = ('Coloc', '6 rue de Rougemont, 75000, Paris, France')
CUR.execute('''INSERT INTO Colocations (name, address) VALUES (%s, %s)''', COLOC)

#Ajout compte admin
ADMIN = ('Admin', 'Admin', 'maxanceribeiro@live.fr', crypted_string('072330STM'), 1)
# ('maxanceribeiro@live.fr', 'maxanceribeiro@live.fr')

CUR.execute('''INSERT INTO Users (first_name, last_name, email, password, id_colocation)
VALUES (%s, %s, %s, %s, %s)''', ADMIN) 
# WHERE NOT EXISTS (SELECT %s FROM Users WHERE email = %s)''', admin)

#Ajout fausse facture
INVOICE = ('Loyer', 29.99, True, '01/01/01', 'details', '1')
CUR.execute('''INSERT INTO Invoices (title, price, type, date, details, id_paying_user)
VALUES (%s, %s, %s, %s, %s, %s)''', INVOICE)

#Sauvegarde des changements
CONN.commit()
#Fermeture connexion
CUR.close()
CONN.close()
