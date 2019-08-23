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
	id_paying_user INTEGER,
	    FOREIGN KEY (id_paying_user)
	    REFERENCES Users (id)
    );
    '''
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS MEALS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number FLOAT NOT NULL,
        id_eating_user INTEGER,
	    FOREIGN KEY (id_eating_user)
	    REFERENCES Users (id)
    );
    '''
)

#Sauvegarde des changements
conn.commit()
#Fermeture connexion
c= conn.close()
