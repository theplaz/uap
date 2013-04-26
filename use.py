import array
import numpy as np
import pprint
import db

db.create_db_conn()

#do the naive bayes classifier

 #load all software times software
db.cur.execute("SELECT DISTINCT type, name FROM `software`;")
software_types = db.cur.fetchall()

#load all existing visits
db.cur.execute("SELECT * FROM visit;")
visits_from = db.cur.fetchall()

#get input row
def find_original_visit(visit_to):
    best_visit_id = None
    best_visit_value = float(0)
    
    #for each row in the db
    for visit_from in visits_from:
        print visit_from
        
        visit_from_P_value = float(1)
        
        #can skip P(x0=A) since all have this
        
        #for each software version
        for software in software_types:
            type = software[0]
            name = software[1]
            
            #look up version1 and version2 for this software
            db.cur.execute("SELECT version FROM software WHERE type = %s AND name = %s AND visit_id = %s LIMIT 1;", (type, name, visit_from[0]))
            softwares1 = db.cur.fetchone()
            #print softwares1
            if softwares1 is None:
                version1 = 'none'
            else:
                version1 = softwares1[0]
            
            db.cur.execute("SELECT version FROM software WHERE type = %s AND name = %s AND visit_id = %s LIMIT 1;", (type, name, visit_to[0]))
            softwares2 = db.cur.fetchone()
            #print softwares2
            if softwares2 is None:
                version2 = 'none'
            else:
                version2 = softwares2[0]
            
            #select Markov(x0 = a AND x1 = b)
            db.cur.execute("SELECT Pba, Pba_laplace FROM markov_estimates WHERE type = %s AND name = %s AND version1 = %s AND version2 = %s", (type, name, version1, version2));
            estimate = db.cur.fetchone()
            print estimate
            if estimate is None:
                #must look up manual
                
                #look up software total #(x1=b)
                db.cur.execute("SELECT count FROM software_total WHERE type = %s AND name = %s AND version = %s;", (type, name, version2));
                software_total = db.cur.fetchone()
                count_Pa = software_total[0]
                print count_Pa
                
                #look up # of states for that software
                db.cur.execute("SELECT COUNT(*) FROM software_total WHERE type = %s AND name = %s", (type, name));
                states = db.cur.fetchone()
                count_states = states[0]
                print count_states
                
                Pba_laplace = 1 / float((count_Pa + count_states))
                print Pba_laplace
            else:
                Pba_laplace = estimate[1]
            
            visit_from_P_value *= Pba_laplace
        
        #font check
        
        #any other ones?
        
        print visit_from_P_value
        #check if it is best
        if visit_from_P_value > best_visit_value:
            best_visit_id = visit_from[0]
            best_visit_value = visit_from_P_value
            print "we have a new winner"
            print best_visit_value
            
    print "the winner is:"
    print best_visit_id
    print "with prob"
    print visit_from_P_value
    return [best_visit_id, visit_from_P_value]
