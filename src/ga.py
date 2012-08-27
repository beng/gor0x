from helper.markov import MarkovChain
import helper.consts as consts


'''
Generate an individual (genome) from the given corpus
'''
def genome(corpus):
    """Generate a genome"""    
    return [Markov().markov_pitch(corpus)]

'''
Take a dictionary containing the 
desired population size, number of traits,
and influencers and return an initial
population
'''

def create_pool(pop_size, pop):
    """Create an initial population based 
    on the Markov chain"""
    pop = []
    for indi in range(pop_size):
        #Individual().genome(**{'num_traits' : kargs['num_traits'], 'influencers' : kargs['influencers']})
        #pop.append(genome(pop))
        yield genome(pop)
    #return pop
'''
Generate a Markov chain
'''
class Markov:
    def markov_pitch(self, corpus):
        nr=1000
        m = self.walk_corpus(corpus)        
        #print ''.join([next(m) for k in xrange(nr)])
        ret = [''.join([next(m) for k in xrange(nr)])]
        print ret
        return m
        #yield self.walk_corpus(corpus)

    def walk_corpus(self, corpus):
        chain = MarkovChain(5)
        chain.add_sequence(corpus)        
        return chain.walk()