from helper.markov import MarkovChain
import helper.consts as consts

"""
@TODO rules must be formatted as:
        {"trait" : numeric_value, ...}
        Only equivalents right now,
        e.g. duration_type : 50,
                chord : 10,
                pitch : 10
"""

def genome(corpus, size, nodes):
    """Generate a genome
    default parameters, can override when calling functions"""
    return Markov().markov_pitch(corpus, size, nodes)

class Markov:
    """Generate a Markov chain"""
    def markov_pitch(self, corpus, size, nodes):
        """Nodes = number of previous nodes to remember"""
        m = self.walk_corpus(corpus, nodes)
        return [''.join([next(m) for k in xrange(size)])]

    def walk_corpus(self, corpus, nodes):
        chain = MarkovChain(nodes)
        chain.add_sequence(corpus)
        return chain.walk()

