import psycopg2
import pprint
import datetime
import random
import math
import datetime

def create_cur():
  if 'cur' not in globals():
      global conn
      conn = psycopg2.connect("host='localhost' dbname='test' user='postgres' password='foo'")
      global cur
      cur = conn.cursor()
  return cur

def get_states():
    cur.execute("SELECT DISTINCT browser FROM testdata2")
    records = cur.fetchall()
    return records

def get_pairs():
    result = []
    for i in range(1, 500):
        cur.execute("SELECT * FROM testdata2 WHERE userid = "+str(i), str(i))
        record = cur.fetchall()
        result.append(record)
    return result

def get_pairs_browser():
    result = []
    for i in range(1, 500):
        cur.execute("SELECT * FROM testdata2 WHERE userid = "+str(i), str(i))
        record = cur.fetchall()
        user = []
        for row in record:
            user.append(row[2])
        result.append(user)
    return result

def create_db():
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
        
        cur.execute("INSERT INTO testdata2 (browser, date, userid) VALUES (%s, %s, %s)", (browser[0], date.strftime("%m/%d/%y"), str(userid)))

def print_all_data():
    cur.execute("SELECT * FROM testdata2;")
    records = cur.fetchall()
    pprint.pprint(records)

def close_db():
    conn.commit()
    cur.close()
    conn.close()