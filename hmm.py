import nltk
import array
import numpy as np
import db

db.create_cur()

symbols = db.get_states()
states = db.get_states()

model = nltk.tag.HiddenMarkovModelTrainer(symbols=symbols, states=states)
print model

seq = db.get_pairs_browser()
print seq
tagger = model.train_supervised(seq)
print tagger

nltk.tag.load_pos(1)

for test in [['Firefox 18.0.0', 'Firefox 18.0.1']]:

  sequence = [(t, None) for t in test]

  print('Testing with state sequence', test)
  print('probability =', tagger.probability(sequence))
  print('tagging =    ', tagger.tag([word for (word,tag) in sequence]))
  print('p(tagged) =  ', tagger.probability(sequence))
  print('H =          ', tagger.entropy(sequence))
  print('H_exh =      ', tagger._exhaustive_entropy(sequence))
  print('H(point) =   ', tagger.point_entropy(sequence))
  print('H_exh(point)=', tagger._exhaustive_point_entropy(sequence))

'''
def pd(values, samples):
  d = {}
  for value, item in zip(values, samples):
    d[item] = value
  return DictionaryProbDist(d)

def cpd(array, conditions, samples):
  d = {}
  for values, condition in zip(array, conditions):
    d[condition] = pd(values, samples)
  return DictionaryConditionalProbDist(d)

A = array([[0.6, 0.2, 0.2], [0.5, 0.3, 0.2], [0.4, 0.1, 0.5]], np.float64)
A = cpd(A, states, states)
B = array([[0.7, 0.1, 0.2], [0.1, 0.6, 0.3], [0.3, 0.3, 0.4]], np.float64)
B = cpd(B, states, symbols)
pi = array([0.5, 0.2, 0.3], np.float64)
pi = pd(pi, states)

model = HiddenMarkovModelTagger(symbols=symbols, states=states,
                          transitions=A, outputs=B, priors=pi)

print('Testing', model)

for test in [['up', 'up'], ['up', 'down', 'up'],
              ['down'] * 5, ['unchanged'] * 5 + ['up']]:

  sequence = [(t, None) for t in test]

  print('Testing with state sequence', test)
  print('probability =', model.probability(sequence))
  print('tagging =    ', model.tag([word for (word,tag) in sequence]))
  print('p(tagged) =  ', model.probability(sequence))
  print('H =          ', model.entropy(sequence))
  print('H_exh =      ', model._exhaustive_entropy(sequence))
  print('H(point) =   ', model.point_entropy(sequence))
  print('H_exh(point)=', model._exhaustive_point_entropy(sequence))
  print()
'''
  
db.close_db()