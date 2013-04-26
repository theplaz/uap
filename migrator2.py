import db
import re
import random
import fontscompare

db.create_db_conn()
db.create_orig_db_conn()

#process users aka migrations

#load all existing visits
db.orig_cur.execute("SELECT DISTINCT cookie_id FROM cookies;")
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