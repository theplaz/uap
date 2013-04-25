import db
import re

db.create_db_conn()
db.create_orig_db_conn()

#process fingerprints aka visits

#load all existing visits
db.orig_cur.execute("SELECT id, cookie_id, signature, ip, ip34, timestamp FROM cookies;")
numrows = int(db.orig_cur.rowcount)
#id is visit[0]
#cookie_id is visit[1]
#signature is visit[2]
#ip is visit[3]
#ip34 is visit[4]
#timestamp is visit[5]

#for i in range(numrows):
for i in range(1):
    visit = db.orig_cur.fetchone()
    print visit
    print visit[2].strip()
    
    #get the fingerprint info
    db.orig_cur.execute("SELECT * FROM fingerprint WHERE signature = %s;", visit[2].strip())
    fingerprint = db.orig_cur.fetchone()
    print fingerprint
    print visit
    
    #load into new table
    #drop count = fingerprint[8]
    db.cur.execute("INSERT INTO visit (id, cookie_id, js, cookie_enabled, user_agent, http_accept, plugins, fonts, timezone, video, "+
                                                 "signature, supercookies, ua_h, ft_h, ha_h, pi_h, ip, ip34, timestamp) "+
                                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (visit[0], visit[1], fingerprint[0], fingerprint[1], fingerprint[2], fingerprint[3], fingerprint[4], fingerprint[5],
                        fingerprint[6], fingerprint[7], fingerprint[9], fingerprint[10], fingerprint[11], fingerprint[12], fingerprint[13],
                        fingerprint[14], visit[3], visit[4], visit[5]));
                        
    print 'added visit: '+str(visit[0])
    
    
    #load software version table
    #load user agent = fingerprint[2]
    print fingerprint[2]
    useragent_raw = fingerprint[2].replace('(',';').replace(')',';').split(';')
    useragent = []
    for agent in useragent_raw:
        print agent.strip()
        if agent != '':
            useragent.append(agent.strip())
    print useragent
    
    #match browsers
        #insert into software table
    
    #look at plugins = fingerprint[4]
    #print fingerprint[4]
    plugins = re.split("Plugin [0-9]+\:", fingerprint[4])
    for plugin in plugins:
        print '--'
        plugin = plugin.strip()
        print plugin
        parts = plugin.split(';')
        #print parts
        #split name and version info out
        #name is part[0]
        #name version is part[1]
        if len(parts) > 2:
            print parts[0].strip()
            print parts[1].strip()
            #TODO: pull out version #
            #load into software table
        else:
            print 'error'
            print parts
            

    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()