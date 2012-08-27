from helper.markov import MarkovChain
import helper.consts as consts


'''
Generate an individual of size num_traits
'''
def genome(corpus):
    """Generate a genome"""
    #duration = ['whole', 'half', 'quarter', 'eighth', '16th']
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
    for indi in range(pop_size):
        #Individual().genome(**{'num_traits' : kargs['num_traits'], 'influencers' : kargs['influencers']})
        yield genome(pop)
'''
Generate a Markov chain
'''
class Markov:
    def markov_pitch(self, corpus):
        nr=1000
        m = self.walk_corpus(corpus)
        print ''.join([next(m) for k in xrange(nr)])
        return self.walk_corpus(corpus)

    def walk_corpus(self, corpus):
        chain = MarkovChain(5)
        chain.add_sequence(corpus)        
        return chain.walk()