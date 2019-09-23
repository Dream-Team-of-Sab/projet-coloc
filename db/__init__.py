import psycopg2

db = psycopg2.connect("host=10.5.0.7 dbname=api_flat_dev user=dev password=youwillneverguess")

from db import req
