"""
This is the fourth step in the process to build the Markov model.

In this file, we generate the Markov probability rows, but populating the 'markov_estimate' table.
We do that by scanning over all migration_totals.
We generate simple probability as well as the probability with Laplace smoothing.

Rerun Allowed: Yes

Reset: TRUNCATE markov_estimate table

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import db
import re
import config

db.create_db_conn()
db.create_orig_db_conn()

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
print migration_pairs

#for i in range(numrows):
for migration_pair in migration_pairs:
    type = migration_pair[0]
    name = migration_pair[1]
    version1 = migration_pair[2]
    version2 = migration_pair[3]
    count_PaANDb = migration_pair[4]
    print count_PaANDb
    
    #look up software total #(x1=b)
    db.cur.execute("SELECT count FROM software_total WHERE type = %s AND name = %s AND version = %s;", (type, name, version2));
    software_total = db.cur.fetchone()
    count_Pa = software_total[0]
    print count_Pa
    
    #look up # of states for that software
    db.cur.execute("SELECT COUNT(*) FROM software_total WHERE type = %s AND name = %s", (type, name));
    states = db.cur.fetchone()
    count_states = states[0]
    print count_states
    
    Pba = float(1)
    Pba_laplace = float(1)
    
    Pba = count_PaANDb / float(count_Pa)
    Pba_laplace = (count_PaANDb + 1) / float((count_Pa + count_states))
    
    print Pba
    print Pba_laplace
    
    #insert
    db.cur.execute("INSERT INTO markov_estimates (type, name, version1, version2, Pba, Pba_laplace) "+
                                                     "VALUES (%s, %s, %s, %s, %s, %s) "+
                                                     "ON DUPLICATE KEY UPDATE Pba = %s, Pba_laplace = %s;",
                                                     (type, name, version1, version2, Pba, Pba_laplace, Pba, Pba_laplace));
    print "inserted into markov estimates: "+type+" "+name+" "+version1+" "+version2+" Prob: "+str(Pba)+" LaPlace Prob:"+str(Pba_laplace)
    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()