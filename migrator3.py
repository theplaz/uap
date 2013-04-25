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
numrows = int(db.cur.rowcount)



#for i in range(numrows):
for i in range(1):
    migration = db.cur.fetchone()
    print migration
    #cookie_id migration[0]
    #visit_from migration[1]
    #visit_to migration[2]
    #fonts_added migration[3]
    #fonts_removed migration[4]
    
    #SELECT all the software about this migration
    db.cur.execute("SELECT * FROM `software` WHERE visit_id = %s;", migration[1])
    softwares1 = db.cur.fetchall()
    db.cur.execute("SELECT * FROM `software` WHERE visit_id = %s;", migration[2])
    softwares2 = db.cur.fetchall()
    
    #for each software we are looking at
    for software in software_types:
         
        #locate it in the bundle
        #find what version it is
        
        #insert #(x0=a AND x1=b)
        db.cur.execute("INSERT INTO migration_total (type, name, version1, version2, count) "+
                                                     "VALUES (%s, %s, %s, %s, 1) "+
                                                     "ON DUPLICATE KEY UPDATE count=count+1;",
                                                     (type, name, version1, version2));
    
        #insert #(x1=b)
        db.cur.execute("INSERT INTO software_total (type, name, version, count) "+
                                                     "VALUES (%s, %s, %s, 1) "+
                                                     "ON DUPLICATE KEY UPDATE count=count+1;",
                                                     (type, name, version));
        
db.conn.commit()
db.close_db_conn()
db.close_orig_db_conn()