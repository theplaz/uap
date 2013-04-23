import db
import pprint

db.create_cur()
records = db.get_states()
pprint.pprint(records)
records = db.get_pairs_browser()
pprint.pprint(records)

db.close_db()