"""
This is the third step in the process to build the Markov model.

In this file, we generate the Markov probability rows, but populating the 'markov_estimate' table.
We do that by scanning over all migration_totals.
We generate simple probability as well as the probability with Laplace smoothing.

We precompute this to speed up the actual Bayes estimate.  (In my test 10 sec, not 12 sec)

Rerun Allowed: Yes

Reset: TRUNCATE markov_estimate table

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import sys
import db
import re
import config

db.create_db_conn()

#pagination
if len(sys.argv) == 3:
    start = sys.argv[1]
    num_records = sys.argv[2]
elif len(sys.argv) == 2:
    start = sys.argv[1]
    num_records = config.LARGE_NUM
else:
    start = 0
    num_records = config.LARGE_NUM

#select migration totals
db.cur.execute("SELECT * FROM migration_total LIMIT "+str(int(start))+", "+str(int(num_records))+";")
migration_pairs = db.cur.fetchall()

i = 0
row_total = len(migration_pairs)
print row_total
for migration_pair in migration_pairs:
    #print migration_pair
    type = migration_pair[0]
    name = migration_pair[1]
    version1 = migration_pair[2]
    version2 = migration_pair[3]
    count_PbANDb = migration_pair[4]
    #print count_PbANDb
    
    #look up software total #(x1=b)
    db.cur.execute("SELECT count FROM software_total WHERE type = %s AND name = %s AND version = %s;", (type, name, version2));
    software_total = db.cur.fetchone()
    count_Pb = software_total[0]
    #print count_Pb
    
    #look up # of states for that software
    db.cur.execute("SELECT COUNT(*) FROM software_total WHERE type = %s AND name = %s", (type, name));
    states = db.cur.fetchone()
    count_states = states[0]
    #print count_states
    
    Pba = count_PbANDb / float(count_Pb)
    #print Pba
    
    Pba_laplace = (count_PbANDb + 1) / float((count_Pb + count_states))
    #print Pba_laplace
    
    #insert
    db.cur.execute("INSERT INTO markov_estimates (type, name, version1, version2, Pba, Pba_laplace) "+
                                                     "VALUES (%s, %s, %s, %s, %s, %s) "+
                                                     "ON DUPLICATE KEY UPDATE Pba = %s, Pba_laplace = %s;",
                                                     (type, name, version1, version2, Pba, Pba_laplace, Pba, Pba_laplace));
    i += 1
    print "inserted into markov estimates: "+type+" "+name+" "+version1+" "+version2+" Prob: "+str(Pba)+" LaPlace Prob:"+str(Pba_laplace)
    print "done builder3 "+str(i)+" of "+str(row_total)
    
db.conn.commit()
db.close_db_conn()