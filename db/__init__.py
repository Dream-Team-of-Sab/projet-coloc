from psycopg2 import sql, connect

class Database:
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.dbname = kwargs['dbname']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self._db = connect("host={} dbname={} user={} password={}".format(self.host,  self.dbname, self.user, self.password))

    def __cursor__(self):
        if  self._db.closed :
            self._db = connect("host={} dbname={} user={} password={}".format(self.host,  self.dbname, self.user, self.password))
        return self._db.cursor()

    def __hangup__(self, commit=True):
        if  self._db.closed :
            self._db = connect("host={} dbname={} user={} password={}".format(self.host,  self.dbname, self.user, self.password))
        if commit:
            self._db.commit()
        self._db.rollback()
        self._db.close()

    @staticmethod
    def insert(db, *args, **kwargs):
        """
        Inserts a new row into db object using a dynamic SQL request.
        Simple inserts are done using only args:

        Old way :
        >> cur = db.cursor()
        >> cur.execute("INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)", ('Thomas', 'Barbot', 'foo@bar'))
        >> db.commit()
        >> db.rollback()

        New way :
        >> db.insert('users', 'first_name, last_name, email', 'foo', 'bar', 'foo@bar')

        Inserts with conditions (where) are done using kwargs :

        Old way :
        >> cur = db.cursor()
        >> cur.execute("INSERT INTO users (first_name, last_name, email)
                        SELECT %s, %s, %s WHERE NOT EXISTS
                        (SELECT * FROM users WHERE email = %s)",\
                        ('Thomas', 'Barbot', 'foo@bar', 'foo@bar'))
        >> db.commit()
        >> db.rollback()

        New way :
        >> db.insert('users', 'first_name, last_name, email', 'Thomas', 'Barbot', 'foo@bar', email='foo@bar')

        In both case, table name is always the FIRST args.
        """
        table=args[0]
        values = dict()
        elmts_list = list(zip(args[1].split(","), args[2:]))
        for elmts in elmts_list:
            values.update({elmts[0] : elmts[-1]})
        if not kwargs:
            query = sql.SQL("INSERT INTO {} ({}) VALUES({})")\
                    .format(sql.Identifier(table),\
                            sql.SQL(",").join(map(sql.Identifier, [a.strip() for a in args[1].split(",")])),\
                            sql.SQL(",").join(map(lambda x : sql.Placeholder(name=x), [a.strip() for a in args[1].split(",")])))
        if kwargs:
            l_kwargs_keys = list(kwargs.keys())
            query = sql.SQL("INSERT INTO {} ({}) SELECT {} WHERE NOT EXISTS (SELECT * FROM {} WHERE {} = {})")\
                    .format(sql.Identifier(table),\
                            sql.SQL(",").join(map(sql.Identifier, [a.strip() for a in args[1].split(",")])),\
                            sql.SQL(",").join(map(lambda x : sql.Placeholder(name=x), [a.strip() for a in args[1].split(",")])),\
                            sql.Identifier(table),\
                            sql.Identifier(str(l_kwargs_keys[0])),\
                            sql.Placeholder(name=str(l_kwargs_keys[0])))
            values.update({str(l_kwargs_keys[0]): kwargs[l_kwargs_keys[0]]})
        db.__cursor__().execute(query, values)
        db.__hangup__()

    @staticmethod
    def select(db, *args, **kwargs):
        """
        Selects row(s) of db object using a dynamic SQL request.
        Simple selects are done using only args:

        Old way :
        >> cur = db.cursor()
        >> cur.execute("SELECT id FROM users").fetchall()
        >> db.rollback()

        New way :
        >> db.select('id', 'users')

        Selects with conditions (where) are done using kwargs :

        Old way :

        >> cur = db.cursor()
        >> cur.execute("SELECT id FROM users WHERE email = foo@bar").fetchall()
        >> db.rollback()

        New way :

        >> db.select('id', 'users', email = 'foo@bar')

        In both case, table name is always the LAST args. This function returns
        a list of selected rows, each row being a tuple of item(s) of selected
        column(s).
        """
        table = args[-1]
        query = sql.SQL("SELECT {} FROM {}")\
                .format(sql.SQL(",").join(map(sql.Identifier, args[:-1])),\
                        sql.Identifier(table))
        if kwargs:
            l_kwargs_keys = list(kwargs.keys())
            new_qry = sql.SQL("{} WHERE ({} = {})")\
                      .format(query,\
                              sql.Identifier(str(l_kwargs_keys[0])),\
                              sql.Placeholder(name=str(l_kwargs_keys[0])))
            query = new_qry
            sel = db.__cursor__().execute(query,{str(l_kwargs_keys[0]): kwargs[l_kwargs_keys[0]]})
        else:
            sel = db.__cursor__().execute(query)
        if sel:
            res = sel.fetchall()
        else:
            res = []
        db.__hangup__(commit=False)
        return res

    @staticmethod
    def update(db, *args, **kwargs):
        """
        Updates elements of an existing row into db object using a dynamic SQL request.
        Updates are done using both args and kwargs:

        Old way :
        >> cur = db.cursor()
        >> cur.execute("UPDATE users SET email= %s WHERE user_id= %s)", ('foo@bar', user_id))
        >> db.commit()
        >> db.rollback()

        New way :
        >> db.update('users',  email='foo@bar', user_id=user_id)

        Table name is always the FIRST args.
        """
        table=args[0]
        l_kwargs_keys = list(kwargs.keys())
        values = dict()
        query = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")\
                .format(sql.Identifier(table),\
                        sql.Identifier(str(l_kwargs_keys[0])),\
                        sql.Placeholder(name=str(l_kwargs_keys[0])),\
                        sql.Identifier(str(l_kwargs_keys[1])),\
                        sql.Placeholder(name=str(l_kwargs_keys[1])))
        for x in l_kwargs_keys:
            values.update({str(x): kwargs[x]})
        db.__cursor__().execute(query, values)
        db.__hangup__()

    @staticmethod
    def create(db, req):
        """
        Execute SQL requests given as args (used for table creation)
        """
        db.__cursor__().execute(req)
        db.__hangup__()
