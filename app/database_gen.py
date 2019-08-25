import sqlite3
from functions import crypted_string

#Ouverture connexion
conn = sqlite3.connect('app_database.db')
c = conn.cursor()

c.execute( 
    '''
    CREATE TABLE IF NOT EXISTS Users (
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
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Colocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL
    );
    '''
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
	date DATE NOT NULL,
        number FLOAT NOT NULL,
        id_eating_user INTEGER,
	    FOREIGN KEY (id_eating_user)
	    REFERENCES Users (id)
    );
    '''
)

#Ajout compte admin
admin = ('Admin', 'Admin', 'maxanceribeiro@live.fr', crypted_string('072330STM'), 1,'maxanceribeiro@live.fr','maxanceribeiro@live.fr')

c.execute('''INSERT INTO Users (first_name, last_name, email, password, id_colocation)
             SELECT ?, ?, ?, ?, ?
             WHERE NOT EXISTS (SELECT ? FROM users WHERE email = ?)''', admin)
## Mocks 
#Ajout colocation
coloc= ('Coloc', '6 rue de Rougemont, 75000, Paris, France')

c.execute('''INSERT INTO Colocations (name, address) VALUES (?, ?)''', coloc)

#Ajout fausse facture
invoice =('498412', 29.99, True, '01/01/01', 'details', '1')

c.execute('''INSERT INTO Invoices (title, price, type, date, details, id_paying_user)
             VALUES (?, ?, ?, ?, ?, ?)''', invoice)

##

#Sauvegarde des changements
conn.commit()
#Fermeture connexion
c= conn.close()
