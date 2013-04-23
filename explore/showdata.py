import psycopg2
import random
import math
import datetime
import pprint

conn = psycopg2.connect("host='localhost' dbname='test' user='postgres' password='foo'")
cur = conn.cursor()

cur.execute("SELECT * FROM testdata WHERE browser = 'Firefox 19.0.0' ORDER BY date;")
records = cur.fetchall()
pprint.pprint(records)

conn.commit()
cur.close()
conn.close()