import psycopg2
import random
import math
import datetime
import pprint

conn = psycopg2.connect("host='localhost' dbname='test' user='postgres' password='foo'")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS testdata2 (id serial PRIMARY KEY, date TIMESTAMP, browser VARCHAR, userid INT);")
    
broswers = [['Firefox 18.0.0', datetime.date(2013, 1, 8)],
            ['Firefox 18.0.1', datetime.date(2013, 1, 18)],
            ['Firefox 18.0.2', datetime.date(2013, 2, 5)],
            ['Firefox 19.0.0', datetime.date(2013, 2, 19)],
            ['Firefox 19.0.1', datetime.date(2013, 2, 27)],
            ['Firefox 19.0.2', datetime.date(2013, 3, 7)],
            ['Firefox 20.0.0', datetime.date(2013, 4, 2)]]
    
    
for i in range(1000):
    browser = broswers[random.randint(0,len(broswers)-1)]
    print browser
    dateadd = random.expovariate(5)*100
    print dateadd
    dateadd = datetime.timedelta(days=dateadd)
    print dateadd
    date = browser[1] + dateadd
    print "date"
    print date
    print type(date)
    userid = random.randint(1,500)


cur.execute("SELECT * FROM testdata;")
records = cur.fetchall()
pprint.pprint(records)

conn.commit()
cur.close()
conn.close()