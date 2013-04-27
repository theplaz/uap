#import the example text file from pde

import db

f = open('fingerprint-eg.txt', 'r')

db.create_orig_db_conn()

for line in f:
    #print line
    
    if line == '*************************** 1. row ***************************\r\n':
        #do nothing
        row = {}
        print 'row 1'
    elif line[:10] == '**********':
        #submit
        print row
        try:
           db.orig_cur.execute("INSERT INTO fingerprint (js, cookie_enabled, user_agent, http_accept, plugins, fonts, timezone, video, signature, count, supercookies,"+
                                                 "ua_h, ft_h, ha_h, pi_h) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (row['js'], row['cookie_enabled'], row['user_agent'], row['http_accept'], row['plugins'], row['fonts'], row['timezone'], 
                        row['video'], row['signature'], row['count'], row['supercookies'], row['ua_h'], row['ft_h'], row['ha_h'], row['pi_h']));
           row = {}
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    else:
        #add to dataset
        colon = line.find(':')
        first = line[:colon]
        first = first.strip()
        last = line[colon+2:]
        last = last.strip()
        #print first
        #print last
        row[first] = last
        
        
db.orig_conn.commit()
db.close_orig_db_conn()