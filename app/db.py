import sqlite3

#Ouverture connexion
conn = sqlite3.connect('db.db')
c = conn.cursor()

c.execute ( 
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
c.execute (
    '''
    CREATE TABLE IF NOT EXISTS Colocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL
    );
    '''
)
c.execute (
    '''
    CREATE TABLE IF NOT EXISTS Invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        price DECIMAL NOT NULL,
	type BOOL NOT NULL,

	date DATE NOT NULL,
	type BOOL NOT NULL,
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
c.execute('''INSERT INTO Users (first_name, last_name, email, password) SELECT ?, ?, ? , ? 
         WHERE NOT EXISTS (SELECT ? FROM users WHERE email = ?)'''\
       ,('Admin', 'Admin', 'maxanceribeiro@live.fr', crypted_string('072330STM'), 'maxanceribeiro@live.fr', 'maxanceribeiro@live.fr'))

#Sauvegarde des changements
conn.commit()
#Fermeture connexion
c= conn.close()
