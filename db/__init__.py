import sqlite3

db = sqlite3.connect('db/api_flat.db', check_same_thread=False)

from db import req
