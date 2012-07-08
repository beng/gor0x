import sys
from markov import markov
import individual
import random

"""
initial population
    -supply either artist name or 2 songs 
    -select subset of pitches from each song OR if artist supplied, take 2 random subsets of pitch file of length num_traits
        -EXPERIMENT WITH -- when getting pitches, do i want to select a subset of same pitches (e.g. [C# C# C# C# C#]or do i want diversity?) 
    -take euclidean distance between 2 subsets -- this becomes the fitness comparator
    -build markov model with the traits selected above

fitness
    -sum([euclidean distance individual and parent_1], [euclidean distance between individual and parent_2]    
    -winners of round =  30%similar, 30%X middle, and 60% different children depending on desired number of children.this will be useful to ensure that the population doesnt converge 
    -use case:
        the 2 songs supplied on the cmd line are "billy joel - we didnt start the fire" and "jay-z - hard knock life". 
        take the euclidean distance between those 2 songs and use that to compare against the SUM of the euclidean distance between the child and billy joel, and the euclidean distance between the child and jay-z.     

implement opts, args = getopt.getopt to allow flags and args 
	e.g. python music.py -a <artist> -s1 <song_1> -s2 <song_2>

TODO: modify markov chain to take in a list of pitches instead of a file -- [ [melody_1], ... , [melody_n] ]

TODO: if size of song_file, i.e. number of pitches in the file is LESS THAN NUM_TRAITS then set NUM_TRAITS EQUAL to the total number of pitches in the file (e.g. big poppa has 50 pitches, NUM_TRAITS = 100, set NUM_TRAITS=50)
"""

PITCH_DIR = './pitches/pitches_'
NUM_TRAITS = 4
POP_SIZE = 2
NUM_GEN = 5
DURATION = ['whole', 'half', 'quarter', 'eighth', '16th']

def subset(song):
	if len(song) < NUM_TRAITS:
		NUM_TRAITS = len(song)
			
	start = random.randint(0, ((len(song) - NUM_TRAITS) + 1))
	end = start + NUM_TRAITS
	return song[start:end]

def individual(m):
	# returns tuple -- ([pitches], duration)
	return (m.generate_music(NUM_TRAITS), random.choice(DURATION))

def population(m):
	return [individual(m) for i in range(POP_SIZE)]

def run(artist):
	# create markov object
	m = markov(open(PITCH_DIR + artist + '.txt'))	
	pop = population(m)
	print pop,'\n'


run('biggie')
