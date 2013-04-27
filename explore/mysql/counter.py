import db

db.create_db_conn()

#load all software versions
db.cur.execute("SELECT tag, COUNT(*)"+
"FROM ("+
    "SELECT type AS tag "+
    "UNION ALL "+
    "SELECT name AS tag "+
    "UNION ALL "+
    "SELECT version AS tag "+
") AS X (tag) "+
"GROUP BY tag "+
"ORDER BY COUNT(*) DESC")
rows = db.cur.fetchall()
#untested

for software in rows:
    print software

db.conn.commit()
db.close_db_conn()
