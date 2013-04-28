"""
This is the second step in the process to build the Markov model.

In this file, we create migration records.  A migration is an ordered pair of two visits a -> b made by the same user.
A unique user has the same cookie_id which is present among multiple visits (aka fingerprints).

We make make a migration for each ordered pair of visits by a user.

For example, if a visitor visits the site 3 times, which we call a, b,  and c, the following migrations are created:
a -> b
b -> c

We only make a migration if the visits were > 1 hour apart.

We also calculate the number of fonts added and removed between rows here.

We save the migrations in the new db 'migration' table.

Rerun Allowed: Yes

Reset: TRUNCATE migration tables

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import sys
import db
import re
import config
import random
import fontscompare

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

#load all unique users (cookies)
db.cur.execute("SELECT DISTINCT cookie_id FROM visit LIMIT "+str(int(start))+", "+str(int(num_records))+";")
users = db.cur.fetchall()

i = 0
row_total = len(users)
for user in users:
    cookie_id = user[0].strip()
    print 'looking at '+str(cookie_id)
    
    if cookie_id == "no cookie":
        print "no cookie, so skip"
        pass
    else:
        db.cur.execute("SELECT id, fonts, timestamp FROM visit WHERE cookie_id = %s ORDER BY timestamp ASC;", user[0].strip())
        fingerprints = db.cur.fetchall()
        print len(fingerprints)
        
        #save pairs where time > 1 hr
        if len(fingerprints) == 1: #if == 1 then just skip (visitor only came once)
            print "only one fingerprint, skip"
            pass
        else:
            j = 0
            for fingerprint1 in fingerprints:
                if j <= len(fingerprints) - 2:
                    fingerprint2 = fingerprints[j+1]
                    print 'compare '+str(fingerprint1[0])+' '+str(fingerprint2[0])
                    if (fingerprint2[2] - fingerprint1[2]) < (60*60): #if less than 1 hour
                        print 'less than an hour, so skip'
                        pass
                    else:
                        
                        #calculate fonts
                        [fonts_added, fonts_removed] = fontscompare.fontscompare(fingerprint1[1], fingerprint2[1])
                        
                        #train or test set?
                        rand = random.randint(1,4)
                        if rand <= 3:
                            train = 1
                        else:
                            train = 0
                        
                        #insert migration into table
                        db.cur.execute("INSERT IGNORE INTO migration (cookie_id, visit_from, visit_to, fonts_added, fonts_removed, train) "+
                                                     "VALUES (%s, %s, %s, %s, %s, %s)",
                           (cookie_id, fingerprint1[0], fingerprint2[0], fonts_added, fonts_removed, train));
                        print 'added migration for user: '+str(cookie_id)
                j+=1
    i += 1
    print "done builder3 "+str(i)+" of "+str(row_total)
    
db.conn.commit()
db.close_db_conn()