#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psycopg2 import sql
from db import db

def sel_data(*args, **kwargs):
    cur = db.cursor()
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
        cur.execute(query,{str(l_kwargs_keys[0]): kwargs[l_kwargs_keys[0]]})
    else:
        cur.execute(query)
    sel = cur.fetchall()
    db.rollback()
    return sel

def ins_data(*args, **kwargs):
    cur = db.cursor()
    table=args[0]
    values = dict()
    elmts_list = list(zip(args[1].split(","), args[2:]))
    for elmts in elmts_list:
        values.update({elmts[0] : elmts[-1]})
    if not kwargs:
        query = sql.SQL("INSERT INTO {} ({}) VALUES({})")\
                .format(sql.Identifier(table),\
                        sql.SQL(",").join(map(sql.Identifier, args[1].split(","))),\
                        sql.SQL(",").join(map(lambda x : sql.Placeholder(name=x), args[1].split(","))))
    if kwargs:
        l_kwargs_keys = list(kwargs.keys())
        query = sql.SQL("INSERT INTO {} ({}) SELECT {} WHERE NOT EXISTS (SELECT * FROM {} WHERE {} = {})")\
                .format(sql.Identifier(table),\
                        sql.SQL(",").join(map(sql.Identifier, args[1].split(","))),\
                        sql.SQL(",").join(map(lambda x : sql.Placeholder(name=x), args[1].split(","))),\
                        sql.Identifier(table),\
                        sql.Identifier(str(l_kwargs_keys[0])),\
                        sql.Placeholder(name=str(l_kwargs_keys[0])))
        values.update({str(l_kwargs_keys[0]): kwargs[l_kwargs_keys[0]]})
    cur.execute(query, values)
    db.commit()
    db.rollback()
