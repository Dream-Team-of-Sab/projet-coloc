from flask import Flask
from db import Database

app = Flask(__name__)
db = Database(host='db', dbname='api_flat_dev', user='dev', password='youwillneverguess')
app.secret_key = 'bc7466e0f98a79cee6389aac5130e2fe4b75e03e'

from app import routes
from app import functions
