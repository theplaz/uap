"""
This is the database library file for my UAP Panopticlick Migration project.

In this file, I set up connections with the databases and have some library functions to make db calls through.

We have 2 databases:
-the original EFF database
-my new migration-tuned database

I use a new database because I want to be able to make special queries quickly.
The database has not been particualrly optimized for performance; instead I keep steps seperate to help with debugging.

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

import MySQLdb as mdb
import sys
import config

##### Basic Methods #####
def create_db_conn():
  if 'conn' not in globals():
      global conn
      conn = mdb.connect(config.DB_SERVER, config.DB_USER, config.DB_PASS, config.DB_NAME)
      global cur
      cur = conn.cursor()
      cur.execute("USE "+config.DB_NAME+";")
  return cur

def create_orig_db_conn():
  if 'orig_conn' not in globals():
      global orig_conn
      orig_conn = mdb.connect(config.ORIG_DB_SERVER, config.ORIG_DB_USER, config.ORIG_DB_PASS, config.ORIG_DB_NAME)
      global orig_cur
      orig_cur = orig_conn.cursor()
      orig_cur.execute("USE "+config.ORIG_DB_NAME+";")
  return orig_cur

def close_db_conn():
    cur.close()
    conn.close()

def close_orig_db_conn():
    orig_conn.close()
    orig_cur.close()
    
###### Specific Methods #####
def add_software(visit_id, cookie_id, type, name, version):
    """Insert a software version record into the 'software' table"""
    cur.execute("INSERT IGNORE INTO software (visit_id, cookie_id, type, name, version) "+
                    "VALUES (%s, %s, %s, %s, %s)", 
                    (visit_id, cookie_id, type, name, version));
    #print 'added '+type+': '+name+' @ '+version+''