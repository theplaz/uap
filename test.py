"""
This is the function that runs the test script.

It loads rows to test on and then tries to find the most likely row

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""


import array
import numpy as np
import pprint
import db
import use
import sys
import config
import time

db.create_db_conn()

global_start_time = time.time()

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

#set variables
correct = 0
incorrect = 0
tested = 0

#get rows to test on
db.cur.execute("SELECT * FROM migration WHERE train = 0 LIMIT "+str(int(start))+", "+str(int(num_records))+";")
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
    
    start_time = time.time()
    
    [result_visit_id, prob] = use.find_original_visit(visit_to)
    
    end_time = time.time()
    duration = end_time - start_time
    
    #check if result is correct
    print '-------'
    print "for user: "+str(cookie_id)
    print "for current visit#: "+str(visit_to_id)
    print "we wanted visit#: "+str(visit_from_id)
    print "we got visit#: "+str(result_visit_id)
    print "with prob: "+str(prob)
    print "Elapsed time was %g seconds" % (duration)
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
    db.cur.execute("INSERT INTO tested (migration_id, result_visit_id, correct, prob, time) "+
                                                     "VALUES (%s, %s, %s, %s, %s) "+
                                                     "ON DUPLICATE KEY UPDATE result_visit_id = %s, correct = %s, prob = %s, time = %s;",
                                                     (migration_id, result_visit_id, correct_bit, prob, duration, result_visit_id, correct_bit, prob, duration));
    
global_end_time = time.time()
print 'at the end:'
print 'correct: '+str(correct)
print 'incorrect: '+str(incorrect)
print 'tested: '+str(tested)
print "Elapsed time was %g seconds" % (global_end_time - global_start_time)


db.conn.commit()
db.close_db_conn()