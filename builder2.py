"""
This is the second step in the process to build the Markov model.

In this file, we count the number of migrations of each software version.
We do this by scanning the migrations we created in builder2.py.
We also count the number of each number of fonts we've added.

Rerun Allowed: NO!

Reset: TRUNCATE migration_total table

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import sys
import db
import re
import config

db.create_db_conn()

#select software
db.cur.execute("SELECT DISTINCT type, name FROM `software`;")
software_types = db.cur.fetchall()
#print software_types

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

#load all migrations we will use to train from
db.cur.execute("SELECT * FROM migration WHERE train = 1  LIMIT "+str(int(start))+", "+str(int(num_records))+";")
migrations = db.cur.fetchall()

i = 0
row_total = len(migrations)
for migration in migrations:
    #print migration
    migration_id = migration[0]
    cookie_id = migration[1]
    visit_from = migration[2]
    visit_to = migration[3]
    fonts_added = migration[4]
    fonts_removed = migration[5]
    
    #SELECT all the software about this migration
    db.cur.execute("SELECT * FROM `software` WHERE visit_id = %s;", visit_from)
    softwares1 = db.cur.fetchall()
    
    db.cur.execute("SELECT * FROM `software` WHERE visit_id = %s;", visit_to)
    softwares2 = db.cur.fetchall()
    
    #for each software we are looking at
    for software in software_types:
        #print software
        software_type = software[0]
        software_name = software[1]
        
        #locate it in the bundle
        #find what version it is
        software_version1 = 'None'
        for software1 in softwares1:
            if software1[2] == software_type and software1[3] == software_name:
                #print 'found1'
                software_version1 = software1[4]
                break
            
        software_version2 = 'None'
        for software2 in softwares2:
            if software2[2] == software_type and software2[3] == software_name:
                #print 'found2'
                software_version2 = software2[4]
                break
        #print software_version1
        #print software_version2
        
        #insert #(x0=a AND x1=b)
        db.cur.execute("INSERT INTO migration_total (type, name, version1, version2, count) "+
                       "VALUES (%s, %s, %s, %s, 1) "+
                       "ON DUPLICATE KEY UPDATE count=count+1;",
                       (software_type, software_name, software_version1, software_version2));

        #insert #(x1=b)
        db.cur.execute("INSERT INTO software_total (type, name, version, count) "+
                       "VALUES (%s, %s, %s, 1) "+
                       "ON DUPLICATE KEY UPDATE count=count+1;",
                       (software_type, software_name, software_version2));

    #deal with fonts
    db.cur.execute("INSERT INTO font_total (type, number, count) "+
                                                     "VALUES (%s, %s, 1) "+
                                                     "ON DUPLICATE KEY UPDATE count=count+1;",
                                                     ('added', fonts_added));
                                                     
    db.cur.execute("INSERT INTO font_total (type, number, count) "+
                                                     "VALUES (%s, %s, 1) "+
                                                     "ON DUPLICATE KEY UPDATE count=count+1;",
                                                     ('removed', fonts_removed));
    i += 1
    print "done builder2 "+str(i)+" of "+str(row_total)
db.conn.commit()
db.close_db_conn()