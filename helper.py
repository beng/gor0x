from markov import MarkovChain
import model
import random
import consts
import sys

class Spawn:
    def create_pool(self,**kargs):          
        if ('pop_size' and 'num_traits' and 'influencers') in kargs:
            # slightly messy -- need to clean up
            pitch = Markov.markov_pitch(**kargs)
            for pop in range(0,int(kargs['pop_size'])):
                for trait in range(0,int(kargs['num_traits'])):
                    params = dict(
                        indi_id=pop,
                        generation=0,
                        trait=pitch[trait],
                        duration='half',
                        fitness=0,)
                    model.insert('song',params)

class Markov:
    def markov_pitch(self,**kargs):
        if ('num_traits' and 'influencers') in kargs:
            nr = 5000
            m = self.walk_corpus(consts.pitch_dir + kargs['influencers'] + '.txt')
            print ' '.join([next(m) for k in xrange(nr)])

    def walk_corpus(self, fname):
        with open(fname, 'r') as f:
            words = f.read().split()
        chain = MarkovChain(5)
        chain.add_sequence(words)
        return chain.walk()
