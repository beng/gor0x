import random

def genome(m, size):
    # m = markov object
    duration = ['whole', 'half', 'quarter', 'eighth', '16th']
    return [m.generate_music(size) for i in xrange(size), random.choice(duration)]

