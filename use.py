"""
This is the function that does the actual Nieve Bayes Classification.

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import array
import numpy as np
import pprint
import db
import fontscompare

db.create_db_conn()

#load all software times software
db.cur.execute("SELECT DISTINCT type, name FROM `software`;")
software_types = db.cur.fetchall()

#load all existing visits
db.cur.execute("SELECT * FROM visit;")
visits_from = db.cur.fetchall()

#get input row
def find_original_visit(visit_to):
    '''Does the Naive Bayes classification and returns the most likely row in the database
       Input: a visit_to row as a number-indexed list.  Currently must be a row in the db.
       Outputs: best_visit_id = the row id, visit_from_P_value = the generated P value of that row
    '''
    best_visit_id = None
    best_visit_value = float(0)
    
    #load visit_to software into a local datastore
    db.cur.execute("SELECT type, name, version FROM software WHERE visit_id = %s;", (visit_to[0]))
    softwares2_versions = db.cur.fetchall()
    softwares2 = {}
    for software2 in softwares2_versions:
        type = software2[0]
        name = software2[1]
        version = software2[2]
        index = type+"/"+name
        softwares2[index] = version
    
    #for each row in the db
    for visit_from in visits_from:
        #print visit_from
        
        #skip row if it is our original row
        if visit_from[0] != visit_to[0]:
        
            visit_from_P_value = float(1)
            
            #can skip P(x0=A) since all have this
            
            #for each software type
            for software in software_types:
                type = software[0]
                name = software[1]
                index = type+"/"+name
                
                #look up version1 and version2 for this software
                db.cur.execute("SELECT version FROM software WHERE type = %s AND name = %s AND visit_id = %s LIMIT 1;", (type, name, visit_from[0]))
                softwares1 = db.cur.fetchone()
                if softwares1 is None:
                    version1 = 'none'
                else:
                    version1 = softwares1[0]
                #print version1
                
                if index in softwares2.keys():
                    version2 = softwares2[index]
                else:
                    version2 = 'none'
                #print version2
                
                #select Markov(x0 = a AND x1 = b)
                db.cur.execute("SELECT Pba, Pba_laplace FROM markov_estimates WHERE type = %s AND name = %s AND version1 = %s AND version2 = %s", (type, name, version1, version2));
                estimate = db.cur.fetchone()
                #print estimate
                if estimate is None: #if we've never seen this transition before
                    #must look up manual
                    
                    #look up software total #(x1=b)
                    db.cur.execute("SELECT count FROM software_total WHERE type = %s AND name = %s AND version = %s;", (type, name, version2));
                    software_total = db.cur.fetchone()
                    if software_total is None: #if we've never seen this state before...
                        count_Pa = 0
                    else:
                        count_Pa = software_total[0]
                    #print count_Pa
                    
                    #look up # of states for that software
                    db.cur.execute("SELECT COUNT(*) FROM software_total WHERE type = %s AND name = %s", (type, name));
                    states = db.cur.fetchone()
                    count_states = states[0]
                    #print count_states
                    
                    Pba_laplace = 1 / float((count_Pa + count_states))
                    #print Pba_laplace
                else:
                    Pba_laplace = estimate[1]
                
                visit_from_P_value *= Pba_laplace
            
            #font check
            '''
            #(is this the right way?)
            [fonts_added, fonts_removed] = fontscompare.fontscompare(visit_from[7], visit_to[7])
            
            if fonts_added is not None and fonts_removed is not None:
                #check how popular those fonts are... #(fonts_added b/w rows)/#(rows)
                #counts rows total
                db.cur.execute("SELECT COUNT(*) FROM migration;");
                migration_count = db.cur.fetchone()
                migration_count = migration_count[0]
                print migration_count
                
                #count # rows with that add
                db.cur.execute("SELECT COUNT(*) FROM font_total WHERE type = 'added' AND number = %s;", fonts_added);
                fonts_added_count = db.cur.fetchone()
                fonts_added_count= fonts_added_count[0]
                print fonts_added_count
                
                #count # rows with that removed
                db.cur.execute("SELECT COUNT(*) FROM font_total WHERE type = 'removed' AND number = %s;", fonts_removed);
                fonts_removed_count = db.cur.fetchone()
                fonts_removed_count= fonts_removed_count[0]
                print fonts_removed_count
                
                fonts_added_prob = fonts_added_count / float(migration_count)
                print fonts_added_prob
                visit_from_P_value *= fonts_added_prob
                
                fonts_removed_prob = fonts_removed_count / float(migration_count)
                print fonts_removed_prob
                visit_from_P_value *= fonts_removed_prob
            '''
            
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
