import MySQLdb as mdb
import sys
import config

def create_db_conn():
  if 'conn' not in globals():
      global conn
      conn = mdb.connect(config.DB_SERVER, config.DB_USER, config.DB_PASS, config.DB_NAME)
      global cur
      cur = conn.cursor()
  return cur

def create_orig_db_conn():
  if 'orig_conn' not in globals():
      global orig_conn
      orig_conn = mdb.connect(config.ORIG_DB_SERVER, config.ORIG_DB_USER, config.ORIG_DB_PASS, config.ORIG_DB_NAME)
      global orig_cur
      orig_cur = orig_conn.cursor()
  return orig_cur

def close_db_conn():
    cur.close()
    conn.close()

def close_orig_db_conn():
    orig_conn.close()
    orig_cur.close()