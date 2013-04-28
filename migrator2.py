"""
This is the second step in the process to import the EFF database into my database.

In this file, we create migrations.  A migration is an ordered pair of two visits a -> b made by the same user.
A unique user has the same cookie_id which is present among multiple visits (fingerprints).

We make make a migration for each ordered pair of visits by a user.

For example, if a visitor visits the site 3 times, which we call a, b,  and c, the following migrations are created:
a -> b
b -> c

We only make a migration if the visits were > 1 hour apart.

We also calculate the number of fonts added and removed between rows here.

We save the migrations in the new db 'migration' table.

Rerun Allowed: I believe so (confirm, add ignore)

Reset: TRUNCATE migration tables

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import db
import re
import config
import random
import fontscompare

db.create_db_conn()
db.create_orig_db_conn()

#pagination
if len(sys.argv) == 3:
    start = sys.argv[1]
    num_records = sys.argv[2]
elif len(sys.argv) == 2:
    start = sys.argv[1]
    num_records = onfig.LARGE_NUM
else:
    start = 0
    num_records = config.LARGE_NUM

#load all unique users (cookies)
db.orig_cur.execute("SELECT DISTINCT cookie_id FROM cookies LIMIT "+str(int(start))+", "+str(int(num_records))+";")
users = db.orig_cur.fetchall()

for user in users:
    print user
    print user[0].strip()
    
    if user[0].strip() != "no cookie":
    
        db.cur.execute("SELECT * FROM visit WHERE cookie_id = %s ORDER BY timestamp ASC;", user[0].strip())
        fingerprints = db.cur.fetchall()
        print len(fingerprints)
        
        #save pairs where time > 1 hr
        if len(fingerprints) > 1: #if == 1 then just skip (visitor only came once)
            i = 0
            for fingerprint1 in fingerprints:
                if i <= len(fingerprints) - 2:
                    fingerprint2 = fingerprints[i+1]
                    print 'compare '+str(fingerprint1[0])+' '+str(fingerprint2[0])
                    print fingerprint1[18]
                    print fingerprint2[18]
                    if (fingerprint2[18] - fingerprint1[18]) > (60*60):
                        
                        #calculate fonts
                        [fonts_added, fonts_removed] = fontscompare.fontscompare(fingerprint1[7], fingerprint2[7])
                        
                        #train or test set?
                        rand = random.randint(1,4)
                        if rand <= 3:
                            train = 1
                        else:
                            train = 0
                        
                        #insert migration into table
                        db.cur.execute("INSERT INTO migration (cookie_id, visit_from, visit_to, fonts_added, fonts_removed, train) "+
                                                     "VALUES (%s, %s, %s, %s, %s, %s)", 
                           (user[0].strip(), fingerprint1[0], fingerprint2[0], fonts_added, fonts_removed, train));
                        print 'added migration for user: '+str(user[0])
                    else:
                        print 'less than an hour'
                i+=1
    else:
        print "no cookie so skip"
    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()