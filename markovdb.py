import pprint
import datetime
import random
import math
import datetime
import config
import db

def get_states():
    db.cur.execute("SELECT DISTINCT browser FROM "+config.TABLE_NAME+";")
    records = conn.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    return result

def get_pairs():
    result = []
    for i in range(1, 500):
        db.cur.execute("SELECT * FROM "+config.TABLE_NAME+" WHERE userid = "+str(i), str(i))
        record = cur.fetchall()
        result.append(record)
    return result

def get_pairs_browser():
    result = []
    for i in range(1, 500):
        db.cur.execute("SELECT * FROM "+config.TABLE_NAME+" WHERE userid = "+str(i), str(i))
        record = cur.fetchall()
        if len(record) >= 2:
            t = record[0][2], record[len(record)-1][2]
            result.append(t)
    return result

def print_all_data():
    db.cur.execute("SELECT * FROM "+config.TABLE_NAME+";")
    records = conn.fetchall()
    pprint.pprint(records)

