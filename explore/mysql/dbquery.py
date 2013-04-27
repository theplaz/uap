#Run a query on the db

import db

db.create_orig_db_conn();

db.orig_cur.execute("SELECT COUNT(*) FROM  fingerprint;")
data = db.orig_cur.fetchall()
print data

db.close_orig_db_conn();