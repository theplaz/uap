#test out rows

import array
import numpy as np
import pprint
import db
import use

db.create_db_conn()

#set variables
correct = 0
incorrect = 0
tested = 0

#get rows to test on
db.cur.execute("SELECT * FROM migration WHERE train = 0;")
migrations = db.cur.fetchall()

for migration in migrations:
    print migration
    migration_id = migration[0]
    cookie_id = migration[1]
    visit_from_id = migration[2]
    visit_to_id = migration[3]
    fonts_added = migration[4]
    fonts_removed = migration[5]
    
    #get row 2
    #load all software times software
    db.cur.execute("SELECT * FROM visit WHERE id = %s LIMIT 1;", visit_to_id)
    visit_to = db.cur.fetchall()
    visit_to = visit_to[0]
    print visit_to
    
    [result_visit_id, prob] = use.find_original_visit(visit_to)
    
    #check if result is correct
    print '-------'
    print "for user: "+str(cookie_id)
    print "for current visit#: "+str(visit_to_id)
    print "we wanted visit#: "+str(visit_from_id)
    print "we got visit#: "+str(result_visit_id)
    print "with prob: "+str(prob)
    #perhaps print the rows
    #print_visit(visit_to_id)
    #print_visit(visit_from_id)
    
    if visit_from_id == result_visit_id:
        correct += 1
        correct_bit = 1
        print "correct"
    else:
        incorrect += 1
        correct_bit = 0
        print "incorrect"
    tested += 1
    
    #insert
    db.cur.execute("INSERT INTO tested (migration_id, result_visit_id, correct, prob) "+
                                                     "VALUES (%s, %s, %s, %s) "+
                                                     "ON DUPLICATE KEY UPDATE result_visit_id = %s, correct = %s, prob = %s;",
                                                     (migration_id, result_visit_id, correct_bit, prob, result_visit_id, correct_bit, prob));
    db.conn.commit()
    db.close_db_conn()
    exit()

db.close_db_conn()