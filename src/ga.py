from helper.markov import MarkovChain
import helper.consts as consts


'''
Generate an individual of size num_traits
'''
class Individual:    
    def genome(self, **kargs):
        """Generate a genome"""
        #duration = ['whole', 'half', 'quarter', 'eighth', '16th']
        return [Markov().markov_pitch(**kargs)]

'''
Take a dictionary containing the 
desired population size, number of traits,
and influencers and return an initial
population
'''
class Spawn:
    def create_pool(self, **kargs):
        """Create an initial population based 
        on the Markov chain"""
        for indi in range(kargs['pop_size']):
            Individual().genome(**{'num_traits' : kargs['num_traits'], 'influencers' : kargs['influencers']})

'''
Generate a Markov chain
'''
class Markov:
    def markov_pitch(self,**kargs):        
        if ('num_traits' and 'influencers') in kargs:
            nr = int(kargs['num_traits'])
            m = self.walk_corpus(consts.pitch_dir + kargs['influencers'] + '.txt')
            print ' '.join([next(m) for k in xrange(nr)])

    def walk_corpus(self, fname):
        with open(fname, 'r') as f:
            words = f.read().split()
        chain = MarkovChain(5)
        chain.add_sequence(words)
        return chain.walk()

