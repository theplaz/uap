import array
import numpy as np
import pprint
import db
import markovdb
import markov

db.create_db_conn()

#do the naive bayes classifier

#get input row


#load all software times software
db.cur.execute("SELECT DISTINCT type, name FROM `software`;")
software_types = db.cur.fetchall()
print software_types

#load all existing migrations
db.cur.execute("SELECT * FROM fingerprint;")
numrows = int(db.cur.rowcount)

best_row = null
best_value = float(0)

#for each row in the db
#for i in range(numrows):
for i in range(1):
    fingerprint = db.cur.fetchone()
    print fingerprint
    
    row_value = float(1)
    
    #can skip P(x0=A) since all have this
    
    #for each software version
    for software in software_types:
        #select Markov(x0 = a AND x1 = b)
        
        db.cur.execute("SELECT Pb|a, Pb|a_laplace FROM markov_estimates WHERE type = %s AND name = %s AND version1 = %s AND version2 = %s", type, name, version1, version2);
        estimates = db.cur.fetchone()
        
        row_value *= estimates[1]
    
    print row_value
    #check if it is best
    if row_value > best_value:
        best_row = fingerprint
        best_value = row_value
        print "we have a new winner"
        print best_value
        
print "the winner is:"
print fingerprint

db.close_db_conn()