from flask import Flask
from db import Database

app = Flask(__name__)
db = Database("10.5.0.6", "api_flat_dev", "dev", "youwillneverguess")
app.secret_key = 'bc7466e0f98a79cee6389aac5130e2fe4b75e03e'

from app import routes
from app import functions
