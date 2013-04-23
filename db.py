import MySQLdb as mdb
import sys
import config

def create_db_conn():
  if 'conn' not in globals():
      global conn
      conn = mdb.connect(config.DB_SERVER, config.DB_USER, config.DB_PASS, config.TABLE_NAME)
      global cur
      cur = conn.cursor()
  return cur

def close_db_conn():
    conn.close()
