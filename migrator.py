import db
db.create_db_conn()
db.create_orig_db_conn()

#load all existing visits
db.orig_cur.execute("SELECT id, cookie_id, signature, ip, ip34, timestamp FROM cookies;")
numrows = int(db.orig_cur.rowcount)
#id is visit[0]
#cookie_id is visit[1]
#signature is visit[2]
#ip is visit[3]
#ip34 is visit[4]
#timestamp is visit[5]


for i in range(numrows):
    visit = db.orig_cur.fetchone()
    print visit
    
    #get the fingerprint info
    db.orig_cur.execute("SELECT * FROM fingerprint WHERE signature = '"+row[2]+"';")
    fingerprint = db.orig_cur.fetchone()
    
    #load into new table
    #drop count = fingerprint[8]
    db.cur.execute("INSERT INTO fingerprint (id, cookie_id, js, cookie_enabled, user_agent, http_accept, plugins, fonts, timezone, video, "+
                                                 "signature, supercookies,ua_h, ft_h, ha_h, pi_h, ip, ip34, timestamp) "+
                                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (visit[0], visit[1], fingerprint[0], fingerprint[1], fingerprint[2], fingerprint[3], fingerprint[4], fingerprint[5],
                        fingerprint[6], fingerprint[7], fingerprint[9], fingerprint[9], fingerprint[10], fingerprint[11], fingerprint[12], fingerprint[13], 
                        fingerprint[14], visit[3], visit[4], visit[5]));
                        
    print 'added visit: '+str(visit[0])
    
    
    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()