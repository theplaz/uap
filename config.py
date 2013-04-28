"""
This is the config file.

Author: Michael Plasmeier http://theplaz.com
Date: April 2013
License: CC-BY-SA-NC 2.5
"""

##### Original (EFF) Database #####
#Note: only need SELECT access
ORIG_DB_SERVER = 'localhost'
ORIG_DB_USER = 'panopticlick'
ORIG_DB_PASS = 'panopticlick'
ORIG_DB_NAME = 'panopticlick_orig'

##### New Migration-Tuned Database #####
#Need SELECT, INSERT, UPDATE access
DB_SERVER = 'localhost'
DB_USER = 'panopticlick'
DB_PASS = 'panopticlick'
DB_NAME = 'panopticlick'

##### Other #####
ROWS_PER_RUN = 1000
LARGE_NUM = 18446744073709551615 #Must be larger than # of rows in any table