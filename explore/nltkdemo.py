import nltk
import pprint


labelled_sequences, tag_set, symbols = nltk.tag.hmm.load_pos(1)
pprint.pprint(labelled_sequences)
pprint.pprint(tag_set)
pprint.pprint(symbols)


#print nltk.tag.hmm.demo_pos()