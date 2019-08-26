import sqlite3

# Class Database (wrapper)
# PLusieurs méthodes (fonctions) telles que open(), insert() ou close() que l'on pourra appeler dans d'autres fichiers Python


class Database:
    
    '''
    classe Database avec 2 caractéristiques
    conn = connector
    c = cursor

    parametres 
    name = nom de la base de donnée
    On peut directement rentrer le nom de la base de donnée
    cela activera la fonction open() (voir plus bas)
    
    '''

    def __init__(self, name=None):  

	'''
	Construction de l'objet avec un kwarg (name)
	name = nom de la base de donnée

	''' 

        if not name:

	    self.conn = None
            self.c = None

        if name:
            self.open(name)


    def open(self, name):
    
	'''
	Ouverture et connexion de la database
	name = nom de la base de donnée

	'''
    
        try:
            self.conn = sqlite3.connect(name);
            self.c = self.conn.c()
        
        except sqlite3.Error as err:
            print("Error connecting to database")


    def close(self, name):

	'''
	Enregistrement (commit) et fermeture de la database
	name = nom de la base de donnée

	'''

        if self.conn:
            self.conn.commit()
	    self.c.close()
	    self.conn.close()

	return "{0} closed".format(name)

    def insert(self, name, table, columns, data)

	'''
	Requête SQL pour ajouter un élément dans la base de donnée 
	name = nom de la base de donnée
	table = table dans laquelle on va insérer une valeur ; 
	columns = attribut de la table que l'on va ajouter
	data = valeur à ajouter
	
	'''
	self.open(name)

	requete = "INSERT INTO {0} ({1}) VALUES ({2});".format(table, columns, data)
	self.c.execute(requete)

	self.close(name)
	

    def __repr__(self, name, table):
       
        """
        Retourne une liste de toutes les colonnes d'une table dans un tuple
	name = nom de la base de données
	table = table dont on veut afficher les éléments 
        """
	self.open(name)        

	requete = self.c.execute('SELECT * FROM {1}'.format(self.table))
        return str(requete.fetchall())
       
	self.close(name)
