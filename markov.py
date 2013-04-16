from decimal import *

class Markov:

    def __init__(self, states, data):
        self.states = states
        self.data = data
        
        self.apriori = self.calc_apriori()
        self.transition = self.calc_transition()
        
        
    def _init_dict(self):
        result = dict()
        for state in self.states:
            result[state] = 0
        return result

    def calc_apriori(self):
        result = self._init_dict()
        for state in self.states:
            prob = Decimal(0)
            number = self._count_distinct(state)
            prob = number/float(len(self.data))
            result[state] = prob
        return result

    def _count_distinct(self, state):
        result = 0
        for row in self.data:
            if row[0] == state:
                result += 1
        return result
    
    def calc_transition(self):
        result = self._init_dict()
        for state in self.states:
            result[state] = self._count_to(state)
        return result
        
        
    def _count_to(self, state):
        #init
        result = self._init_dict()
        
        #process
        sum = 0
        for row in self.data:
            if row[0] == state:
                #print row
                result[row[1]] += 1
                sum += 1
                
        #turn to prob
        for item in result.keys():
            result[item] = result[item]/float(sum)
        return result
    
    def calc_backwards_prob(self):
        result = self._init_dict()
        for statei in self.states:
            result[statei] = self._init_dict()
            for statej in self.states:
                result[statei][statej] = (self.transition[statej][statej] * self.apriori[statei])/float(self.apriori[statej])
        return result
                
    