from __future__ import with_statement
import sys
from markov import markov
import random
import math
from music21 import *

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele

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

"""

PITCH_DIR = './pitches/pitches_'
NUM_TRAITS = 100
POP_SIZE = 2
NUM_GEN = 5
DURATION = ['whole', 'half', 'quarter', 'eighth', '16th']

def euclid_distance(song1, song2):
	# len(song_1) == len(song_2)
	val = 0
	for i in range(len(song1)):
		val += math.sqrt((pitch.Pitch(song1[i]).midi - int(pitch.Pitch(song2[i]).midi)) ** 2)
	#return [math.sqrt((pitch.Pitch(song1[i]).midi - pitch.Pitch(song2[i]).midi) ** 2) for i in range(len(song1))]
	return val

def mutate():
	# use markov.get_next_pitches() to generate new pitches for individual
	pass

def subset(song):
	nt =  5000	# how big the markov chain should be
	if len(song) < nt:
		nt = len(song)
	start = random.randint(0, ((len(song) - nt) + 1))
	end = start + nt
	return song[start:end]

def parse_songs(songs):
	'''
	supply list of files --
	for each file,
		read in the pitches 
		store in influencer list
	'''
	data = []
	for song in songs:
		with open("./midi_info/"+song,"r") as f: 
			pitches = [elem for elem in f.read().split('\n') if elem] 
			for pitch in pitches: 
				data.append(pitch.split())
	return data

def individual(m):
	# returns tuple -- ([pitches], duration)
	return (m.generate_music(NUM_TRAITS), random.choice(DURATION))

def eval_func(chromosome):
	s = create_pheno(chromosome)	
	#convert_midi(s)
	#rnd = random.randint(0,100)
	#score = 0.0    
	#print 'genome list: ', chromosome.genomeList
	#print 'influ tri : ', influencer_traits
	# iterate over the chromosome	

	#for value in chromosome:
	#	print 'value ', value
	#	print 'influ trait : ', influencer_traits[0][influencer_traits[0].index(value)]
	#	if value not in influencer_traits[0][influencer_traits[0].index(value)]:
		#if value == "A2":
		#if value not in influencer_traits[0].index(value):
	#		score += rnd
	
	#return score
	#euclid_distance(influencer_traits, ch)
	#s = create_pheno(chromosome)
	#p = analysis.discrete.Ambitus()
	#convert_midi(s)
	p = analysis.discrete.KrumhanslSchmuckler()
	fit = p.process(s)[0][2] * 1/(random.randint(1,10))
	#print "fit :: ", fit
	return fit 
	#print 'fitness : ', p.process(s)[0][2]
	#return p.process(s)[0][2]
	#return random.randint(0,100)

def population(m):
	return [individual(m) for i in range(POP_SIZE)]

ben_ed = 0
influencer_traits = []
def run(influencers):
	data = parse_songs(influencers)		
	subset_data = []
	for d in data:
		subset_data += [subset(d)]
	#ed = euclid_distance(subset_data[0], subset_data[1])
	#ben_ed = ed
	print 'subset data :: ', subset_data,'\n'
	#print 'ED :: ', ed
	pitch_data = [item for sublist in subset_data for item in sublist]
	influencer_traits.append(pitch_data)
	print 'pitch data :: ', pitch_data, '\n'
	m = markov(pitch_data)
	markov_music = m.generate_music(NUM_TRAITS)
	orig_mm = markov_music
	print 'm MUSIC : : ', markov_music,'\n'

		# Genome instance
	setOfAlleles = GAllele.GAlleles()
	#for i in xrange(11):
	#    a = GAllele.GAlleleRange(0, i)
	#    setOfAlleles.add(a)
	for i in xrange(len(markov_music)):
		a = GAllele.GAlleleList(markov_music)
		setOfAlleles.add(a)

	#for i in markov_music:
	   # You can even add an object to the list
		#a = GAllele.GAlleleList(['a','b', 'xxx', 666, 0])
	#	a = GAllele.GAlleleList([i])
	#	print ' I :: ', i
	#	setOfAlleles.add(a)	
	genome = G1DList.G1DList(len(markov_music))
	#genome = G1DList.G1DList(len(markov_music))
	genome.setParams(allele=setOfAlleles)

	# The evaluator function (objective function)
	genome.evaluator.set(eval_func)
	genome.mutator.set(Mutators.G1DListMutatorAllele)
	genome.initializator.set(Initializators.G1DListInitializatorAllele)

	# Genetic Algorithm Instance
	ga = GSimpleGA.GSimpleGA(genome)
	ga.selector.set(Selectors.GRouletteWheel)
	ga.setGenerations(1000)

	# Do the evolution, with stats dump
	# frequency of 10 generations
	ga.evolve(freq_stats=100)

	# Best individual
	print ga.bestIndividual()
	print "orig markov music :: ", markov_music
	best_indi =  ga.bestIndividual()[:]
	convert_midi(create_pheno(best_indi))

def to_list(q):
		''' 
		currently use this and not map(str,q) because it is easier to read and
		cleaner looking to parse the traits while using a forloop than to use
		a single line functional approach
		'''
		ret = []
		for i in q:
			ret += [(i.pitch, i.duration)]
		return ret
	
def create_pheno(gene):
	'''
	converts the individuals pitch, accidental, octave, and rhythm to a music stream
	using the music21 library. the music stream is then used to create a midi file
	'''
	#gene = to_list(indi)
	partupper = stream.Part()
	m = stream.Measure()
	for _note in gene:
		#print "note    :", _note
		#print "duration    :", _duration
		n = note.Note(_note)
		n.duration.type = "eighth"
		m.append(n)
	partupper.append(m)    
	return partupper

def convert_midi(mfile):
	'''
	mfile is a musicstream which is exported to as midi format
	'''
	mf = mfile.midiFile
	dir = './melodies/'
	name =  str(random.randint(0,5000))+'song.mid'
	mf.open(dir+name, 'wb')
	mf.write()
	mf.close()
	return name
		




# KEEP TO ONLY 2 SONGS FOR NOW -- EUCLID DISTANCE ONLY MADE TO WORK FOR 2 SONGS !!!
influencers = ['pitches_beatles.txt', 'pitches_essenFolksong.txt']
run(influencers)
