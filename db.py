import _mysql
import sys
import config

con = None

try:

    con = _mysql.connect(config.ORIG_DB_SERVER, config.ORIG_DB_USER, config.ORIG_DB_PASS, config.ORIG_TABLE_NAME)
        
    con.query("SELECT VERSION()")
    result = con.use_result()
    
    print "MySQL version: %s" % \
        result.fetch_row()[0]
    
except _mysql.Error, e:
    
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if con:
        con.close()