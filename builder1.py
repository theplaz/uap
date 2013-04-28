"""
This is the first step in the process to build the Markov model.

In this file, we count the number of occurrences of each software.

This could be combined with migrator.py, but I wanted to keep migrator and builder separate.

Rerun Allowed: No

Reset: TRUNCATE software_total tables

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import db
import re
import config

db.create_db_conn()

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

#load all software versions
db.orig_cur.execute("SELECT type, browser, version FROM software LIMIT "+str(int(start))+", "+str(int(num_records))+";")
software_instances = db.orig_cur.fetchall()

for software_instance in software_instances:
    print software_instance
    software_instance_type = software_instance[0]
    software_instance_name = software_instance[1]
    software_instance_version = software_instance[2]
    
    #insert #(x1=b)
    db.cur.execute("INSERT INTO software_total (type, name, version, count) "+
                   "VALUES (%s, %s, %s, 1) "+
                   "ON DUPLICATE KEY UPDATE count=count+1;",
                   (software_instance_type, software_instance_name, software_instance_version));
    
db.conn.commit()
db.close_db_conn()