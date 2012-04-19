import random
import crossover
import select
import individual
from markov import markov


"""
have already started porting each of the genetic operators to individual files, HOWEVER
have yet to test what i ported over there are probably a significant amount of errors

1. test what i wrote
2. combine into index controller
"""

class test_case():
    def run(self, num_traits, pop_size, num_gen, influencer):
        m = markov(open('static/pitches/pitches_' + influencer + '.txt'))
        pop = individual.genome(m,num_traits)
        
             
        print 'population is ',pop
        # crossover
        p1 = random.choice(pop)
        p2 = random.choice(pop)
        child = crossover.mate(p1,p2, num_traits)        
        print 'p1 is ',p1
        print 'p2 is ',p2
        print 'child is ',child        
        
        # select
        #print select.helper(1,pop,4)
            
    
t = test_case()
t.run(4,2,5,'haydn')
