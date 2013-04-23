import array
import numpy as np
import pprint
import db
import markovdb
import markov

db.create_db_conn()

states = markovdb.get_states()
data = markovdb.get_pairs_browser()

markov = markov.Markov(states, data)

final = markov.calc_backwards_prob()
pprint.pprint(final)
  
db.close_db_conn()