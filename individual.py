import random
import markov

def individual(m, size):
    duration = ['whole', 'half', 'quarter', 'eighth', '16th']
    return m.generate_music(size)

def population(m, size):
	return [individual(m,size) for i in range(size)]