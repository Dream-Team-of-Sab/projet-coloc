from flask import Flask
from db import Database
from appConfig import Config, file_to_dict

conf = Config(paramDict=file_to_dict('conf.txt'))
app = Flask(__name__)
db = Database("db", "api_flat_dev", "dev", "youwillneverguess")
app.secret_key = conf.param('flask_secret_key')

from app import routes
from app import functions
