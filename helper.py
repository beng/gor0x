import individual
from markov import markov

"""
utility functions
"""

def spawn_pop(artist,size):
	"""spawn the initial population"""
	m = markov(open('./static/pitches/pitches_' + str(artist) + '.txt'))
	print 'individual.genome :: ', individual.genome(m,int(size))
