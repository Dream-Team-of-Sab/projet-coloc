from psycopg2 import connect

class Database:
    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

    def __conn__(self):
        self._db = connect("host={} dbname={} user={} password={}".format(self.host, self.dbname, self.user, self.password))
        return self._db

    @staticmethod
    def __cursor__(db):
        cur = db.cursor()
        return cur

    @staticmethod
    def __close__(db, save=True):
        if save:
            db.commit()
        db.rollback()
        db.close()
