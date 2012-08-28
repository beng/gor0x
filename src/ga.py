from helper.markov import MarkovChain
import helper.consts as consts


def genome(corpus, *args):
    """Generate a genome
    *args MAY contain size and nodes"""
    if len(args) > 0:
        return Markov().markov_pitch(corpus, size, nodes)

    return Markov().markov_pitch(corpus)

class Markov:
    """Generate a Markov chain"""

    def markov_pitch(self, corpus, size=5000, nodes=5):
        """Nodes = number of previous nodes to remember"""    
        m = self.walk_corpus(corpus, nodes)
        return [''.join([next(m) for k in xrange(size)])]

    def walk_corpus(self, corpus, nodes):
        chain = MarkovChain(nodes)
        chain.add_sequence(corpus)        
        return chain.walk()