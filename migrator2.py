import db
import re

db.create_db_conn()
db.create_orig_db_conn()

#process users aka migrations

#load all existing visits
db.orig_cur.execute("SELECT DISTINCT cookie_id FROM cookies;")
numrows = int(db.orig_cur.rowcount)


#for i in range(numrows):
for i in range(1):
    user = db.orig_cur.fetchone()
    print user[0].strip()
    
    if user[0].strip() != "no cookies":
    
        db.cur.execute("SELECT * FROM visit WHERE cookie_id = %s;", user[0].strip())
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
                        
                        
                        #count fonts added
                        #TODO
                        fonts_added = 0
                        
                        #count fonts removed
                        #TODO
                        fonts_removed = 0
                        
                        #insert into table
                        db.cur.execute("INSERT INTO migration (cookie_id, visit_from, visit_to, fonts_added, fonts_removed) "+
                                                     "VALUES (%s, %s, %s, %s, %s)", 
                           (user[0].strip(), fingerprint1[0], fingerprint2[0], fonts_added, fonts_removed));
                            
                        print 'added migration for user: '+str(user[0])
                    else:
                        print 'less than an hour'
                i+=1

    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()