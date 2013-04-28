"""
This is the first step in the process to import the EFF database into my database.

In this file, we load all of the visits (from the 'cookies' and 'fingerprint' EFF tables) into a single 'fingerprint' table in my new migration-tuned db.
We also load user_agent's software, lang, timezone; as well as plugin software versions into the 'software' table.

Rerun Allowed: Not sure (?)

Reset: TRUNCATE 'visit' and 'fingerprint' tables

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import config
import db
import re
import sys

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

#load all existing visits
db.orig_cur.execute("SELECT id, cookie_id, signature, ip, ip34, timestamp FROM cookies LIMIT "+str(int(start))+", "+str(int(num_records))+";")
visits = db.orig_cur.fetchall()

for visit in visits:
    if visit != None:
        print visit[2].strip()
        visit_id = visit[0]
        cookie_id = visit[1].strip()
        signature = visit[2].strip()
        ip = visit[3]
        ip34 = visit[4]
        timestamp = visit[5]
    
        
        #get the fingerprint info
        db.orig_cur.execute("SELECT * FROM fingerprint WHERE signature = %s;", visit[2].strip())
        fingerprint = db.orig_cur.fetchone()
        print fingerprint
        fingerprint_user_agent = fingerprint[2]
        fingerprint_plugins = fingerprint[4]
        print visit
        
        
        #load into new table
        #drop count = fingerprint[8]
        db.cur.execute("INSERT IGNORE INTO visit (id, cookie_id, js, cookie_enabled, user_agent, http_accept, plugins, fonts, timezone, video, "+
                                                     "signature, supercookies, ua_h, ft_h, ha_h, pi_h, ip, ip34, timestamp) "+
                                                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (visit_id, cookie_id, fingerprint[0], fingerprint[1], fingerprint[2], fingerprint[3], fingerprint[4], fingerprint[5],
                            fingerprint[6], fingerprint[7], fingerprint[9], fingerprint[10], fingerprint[11], fingerprint[12], fingerprint[13],
                            fingerprint[14], ip, ip34, timestamp));
                            
        print 'added visit: '+str(visit_id)
        
        
        #load software version table
        
        #load user agent
        print fingerprint_user_agent
        fingerprint_user_agent = fingerprint_user_agent.replace('(',';').replace(')',';').split(';')
        user_agent = []
        for agent in fingerprint_user_agent:
            print agent.strip()
            if agent != '':
                user_agent.append(agent.strip())
        print user_agent
        
        for agent in user_agent:
            #match browsers
            #(this is so ugly!)
            #(if we don't have all, not a big problem)
            if 'Firefox' in agent:
                db.add_software(visit[0], visit[1], 'browser', 'Firefox', agent)
            elif 'Safari' in agent: #must go first
               db.add_software(visit[0], visit[1], 'browser', 'Safari', agent)
            elif 'Chrome' in agent:
                db.add_software(visit[0], visit[1], 'browser', 'Chrome', agent)
            elif 'MSIE' in agent:
                db.add_software(visit[0], visit[1], 'browser', 'MSIE', agent)
            elif 'Opera' in agent:
                db.add_software(visit[0], visit[1], 'browser', 'Opera', agent)
                
                
            #match os
            if 'Windows' in agent:
                    db.add_software(visit[0], visit[1], 'os', 'Windows', agent)
            elif 'Mac OS X' in agent:
                    db.add_software(visit[0], visit[1], 'os', 'Mac OS X', agent)
            elif 'Linux' in agent:
                    db.add_software(visit[0], visit[1], 'os', 'Linux', agent)
            elif 'Ubuntu' in agent:
                    db.add_software(visit[0], visit[1], 'os', 'Ubuntu', agent)
            
            #match lang
            #(is there any automated way to do this?)
            langs = ['en-us', 'en-gb', 'en', 'de-de', 'de'] #more restrictive first
            for lang in langs:
                if lang in agent.lower():
                        db.add_software(visit[0], visit[1], 'lang', 'lang', lang)
                        break
                    
            #look at certain other user-agent visible plugins
            if '.NET CLR' in agent:
                db.add_software(visit[0], visit[1], 'ua_plugin', '.NET CLR', agent)
            if 'OfficeLiveConnector' in agent:
                db.add_software(visit[0], visit[1], 'ua_plugin', 'OfficeLiveConnector', agent)
            if 'OfficeLivePatch' in agent:
                db.add_software(visit[0], visit[1], 'ua_plugin', 'OfficeLivePatch', agent)
        
        #look at plugins
        #print fingerprint_plugins
        fingerprint_plugins = re.split("Plugin [0-9]+\:", fingerprint_plugins)
        for plugin in fingerprint_plugins:
            #print '--'
            plugin = plugin.strip()
            parts = plugin.split(';')
            #split name and version info out
            if len(parts) > 2:
                name = parts[0].strip()
                version = parts[1].strip() #this really should be version, but EFF didn't store version #!
                #print name
                #print version
                
                #load into software table
                db.add_software(visit[0], visit[1], 'plugin', name, version)
            else:
                print 'error'
                print parts
    
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()