import db
import re

db.create_db_conn()
db.create_orig_db_conn()

#count migrations

#select software
db.cur.execute("SELECT DISTINCT type, name FROM `software`;")
software_types = db.cur.fetchall()
print software_types

#load all existing migrations
db.cur.execute("SELECT * FROM migration;")
migrations = db.cur.fetchall()


for migration in migrations:
    print migration
    #cookie_id migration[0]
    #visit_from migration[1]
    #visit_to migration[2]
    #fonts_added migration[3]
    #fonts_removed migration[4]
    
    #SELECT all the software about this migration
    db.cur.execute("SELECT * FROM `software` WHERE visit_id = %s;", migration[1])
    softwares1 = db.cur.fetchall()
    print softwares1
    print '---'
    db.cur.execute("SELECT * FROM `software` WHERE visit_id = %s;", migration[2])
    softwares2 = db.cur.fetchall()
    print softwares2
    
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
                print 'found1'
                print software1
                software_version1 = software1[4]
                break
            
        software_version2 = 'None'
        for software2 in softwares2:
            if software2[2] == software_type and software2[3] == software_name:
                print 'found2'
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
        
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()