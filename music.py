from __future__ import with_statement
import sys
from markov import markov
import random
import math

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
NUM_TRAITS = 50
POP_SIZE = 2
NUM_GEN = 5
DURATION = ['whole', 'half', 'quarter', 'eighth', '16th']

midi_mapping = {
	'C0' : 0,
	'C#0' : 1,
	'D0' : 2,
	'D#0' : 3,
	'E0' : 4,
	'F0' : 5,
	'F#0' : 6,
	'G0' : 7,
	'G#0' : 8,
	'A0' : 9,
	'A#0' : 10,
	'B0' : 11,
	'C1' : 12,
	'C#1' : 13,
	'D1' : 14,
	'D#1' : 15,
	'E1' : 16,
	'F1' : 17,
	'F#1' : 18,
	'G1' : 19,
	'G#1' : 20,
	'A1' : 21,
	'A#1' : 22,
	'B1' : 23,
	'C2' : 24,
	'C#2' : 25,
	'D2' : 26,
	'D#2' : 27,
	'E2' : 28,
	'F2' : 29,
	'F#2' : 30,
	'G2' : 31,
	'G#2' : 32,
	'A2' : 33,
	'A#2' : 34,
	'B2' : 35,
	'C3' : 36,
	'C#3' : 37,
	'D3' : 38,
	'D#3' : 39,
	'E3' : 40,
	'F3' : 41,
	'F#3' : 42,
	'G3' : 43,
	'G#3' : 44,
	'A3' : 45,
	'A#3' : 46,
	'B3' : 47,
	'C4' : 48,
	'C#4' : 49,
	'D4' : 50,
	'D#4' : 51,
	'E4' : 52,
	'F4' : 53,
	'F#4' : 54,
	'G4' : 55,
	'G#4' : 56,
	'A4' : 57,
	'A#4' : 58,
	'B4' : 59,
	'C5' : 60,
	'C#5' : 61,
	'D5' : 62,
	'D#5' : 63,
	'E5' : 64,
	'F5' : 65,
	'F#5' : 66,
	'G5' : 67,
	'G#5' : 68,
	'A5' : 69,
	'A#5' : 70,
	'B5' : 71,
	'C6' : 72,
	'C#6' : 73,
	'D6' : 74,
	'D#6' : 75,
	'E6' : 76,
	'F6' : 77,
	'F#6' : 78,
	'G6' : 79,
	'G#6' : 80,
	'A6' : 81,
	'A#6' : 82,
	'B6' : 83,
	'C7' : 84,
	'C#7' : 85,
	'D7' : 86,
	'D#7' : 87,
	'E7' : 88,
	'F7' : 89,
	'F#7' : 90,
	'G7' : 91,
	'G#7' : 92,
	'A7' : 93,
	'A#7' : 94,
	'B7' : 95,
	'C8' : 96,
	'C#8' : 97,
	'D8' : 98,
	'D#8' : 99,
	'E8' : 100,
	'F8' : 101,
	'F#8' : 102,
	'G8' : 103,
	'G#8' : 104,
	'A8' : 105,
	'A#8' : 106,
	'B8' : 107,
	'C9' : 108,
	'C#9' : 109,
	'D9' : 110,
	'D#9' : 111,
	'E9' : 112,
	'F9' : 113,
	'F#9' : 114,
	'G9' : 115,
	'G#9' : 116,
	'A9' : 117,
	'A#9' : 118,
	'B9' : 119,
	'C10' : 120,
	'C#10' : 121,
	'D10' : 122,
	'D#10' : 123,
	'E10' : 124,
	'F10' : 125,
	'F#10' : 126,
	'G10' : 127,
}

def euclid_distance(song1, song2):
	return [math.sqrt((song1[i] - song2[i]) ** 2) for i in range(NUM_TRAITS)]

def mutate():
	# use markov.get_next_pitches() to generate new pitches for individual
	pass

def subset(song):
	nt = NUM_TRAITS
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

def population(m):
	return [individual(m) for i in range(POP_SIZE)]

def run(influencers):
	data = parse_songs(influencers)
	ed = euclid_distance(data[0], data[1])
	print 'ED :: ', ed
	subset_data = []
	for d in data:
		subset_data += [subset(d)]

	print 'subset data :: ', subset_data,'\n'

	pitch_data = [item for sublist in subset_data for item in sublist]
	print 'pitch data :: ', pitch_data, '\n'
	m = markov(pitch_data)
	markov_music = m.generate_music(NUM_TRAITS)
	print 'm MUSIC : : ', markov_music,'\n'


# KEEP TO ONLY 2 SONGS FOR NOW -- EUCLID DISTANCE ONLY MADE TO WORK FOR 2 SONGS !!!
influencers = ['I_Aint_Mad_Atcha.txt', 'Nothing_To_Lose.txt']
run(influencers)
