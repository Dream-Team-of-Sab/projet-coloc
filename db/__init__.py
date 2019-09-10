import psycopg2

db = psycopg2.connect("host=db dbname=api_flat_dev user=dev password=youwillneverguess")

from db import req
