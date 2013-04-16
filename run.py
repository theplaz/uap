import db
import array
import numpy as np
import markov
import pprint

db.create_cur()

states = db.get_states()
data = db.get_pairs_browser()

markov = markov.Markov(states, data)

apriori = markov.calc_apriori()
pprint.pprint(apriori)

transition = markov.calc_transition()
pprint.pprint(transition)

final = markov.calc_backwards_prob()
pprint.pprint(final)
  
db.close_db()