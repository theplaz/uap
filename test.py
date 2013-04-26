import array
import numpy as np
import pprint
import db
import use

db.create_db_conn()

#test out rows

#get rows to test on
db.cur.execute("SELECT * FROM migration WHERE train = 0;")
migrations = db.cur.fetchall()

for migration in migrations:
    print migration
    cookie_id = migration[0]
    visit_from_id = migration[1]
    visit_to_id = migration[2]
    fonts_added = migration[3]
    fonts_removed = migration[4]
    
    #get row 2
    #load all software times software
    db.cur.execute("SELECT * FROM visit WHERE id = %s LIMIT 1;", visit_to_id)
    visit_to = db.cur.fetchall()
    visit_to = visit_to[0]
    print visit_to
    
    result = use.find_original_visit(visit_to)
    
    #check if result is correct
    print result
    exit()

db.close_db_conn()