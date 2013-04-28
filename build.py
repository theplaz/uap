"""
This file runs all of the other builder files

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import os
import math
import sys
import db
import re
import config

db.create_db_conn()
db.create_orig_db_conn()

##### Clear db ####
db.cur.execute("TRUNCATE `font_total`;")
db.cur.execute("TRUNCATE `markov_estimates`;")
db.cur.execute("TRUNCATE `migration`;")
db.cur.execute("TRUNCATE `migration_total`;")
db.cur.execute("TRUNCATE `software`;")
db.cur.execute("TRUNCATE `software_total`;")
db.cur.execute("TRUNCATE `tested`;")
db.cur.execute("TRUNCATE `visit`;")
db.conn.commit()


##### migrator.py ####
#get number of rows in old visit table
db.orig_cur.execute("SELECT COUNT(*) FROM cookies;")
count = db.orig_cur.fetchone()
count = count[0]
print count
rounds = int(math.ceil(count/float(config.ROWS_PER_RUN)))
print rounds

for i in range(rounds):
    round = i * config.ROWS_PER_RUN
    print "python migrator.py "+str(round)+" "+str(config.ROWS_PER_RUN)
    os.system("python migrator.py "+str(round)+" "+str(config.ROWS_PER_RUN))
    
##### builder1.py ####
db.cur.execute("SELECT COUNT(*) FROM software;")
count = db.cur.fetchone()
count = count[0]
print count
rounds = int(math.ceil(count/float(config.ROWS_PER_RUN)))
print rounds

for i in range(rounds):
    round = i * config.ROWS_PER_RUN
    print "python builder1.py "+str(round)+" "+str(config.ROWS_PER_RUN)
    os.system("python builder1.py "+str(round)+" "+str(config.ROWS_PER_RUN))

##### builder2.py ####
db.cur.execute("SELECT COUNT(DISTINCT cookie_id) FROM visit;")
count = db.cur.fetchone()
count = count[0]
print count
rounds = int(math.ceil(count/float(config.ROWS_PER_RUN)))
print rounds

for i in range(rounds):
    round = i * config.ROWS_PER_RUN
    print "python builder2.py "+str(round)+" "+str(config.ROWS_PER_RUN)
    os.system("python builder2.py "+str(round)+" "+str(config.ROWS_PER_RUN))
    
##### builder3.py ####
db.cur.execute("SELECT COUNT(*) FROM migration WHERE train = 1;")
count = db.cur.fetchone()
count = count[0]
print count
rounds = int(math.ceil(count/float(config.ROWS_PER_RUN)))
print rounds

for i in range(rounds):
    round = i * config.ROWS_PER_RUN
    print "python builder3.py "+str(round)+" "+str(config.ROWS_PER_RUN)
    os.system("python builder3.py "+str(round)+" "+str(config.ROWS_PER_RUN))

##### builder4.py ####
db.cur.execute("SELECT COUNT(*) FROM migration_total;")
count = db.cur.fetchone()
count = count[0]
print count
rounds = int(math.ceil(count/float(config.ROWS_PER_RUN)))
print rounds

for i in range(rounds):
    round = i * config.ROWS_PER_RUN
    print "python builder4.py "+str(round)+" "+str(config.ROWS_PER_RUN)
    os.system("python builder4.py "+str(round)+" "+str(config.ROWS_PER_RUN))
    
    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()