from music21 import *
import os
import fnmatch

'''
parses a midi file for the pitch and octave

p = path
od = output directory

CAN CHANGE note.Note to chord.Chord to get a list of chords! but then need
'''

def parse(p):
	path = p
	pattern = '*.mid'
	name = ''
	for root, dirs, files in os.walk(path):
		for fname in fnmatch.filter(files,pattern):
			if 'top100_' in fname:			
				song_name = fname.replace('top100_', '')
				song_name = song_name.replace('.mid', '')
			else:
				song_name = fname.replace('.mid', '')
			print 'Parsing Song :: ', song_name
			wf = open(root+'/'+song_name+'.txt', 'w')
			stream = converter.parse(root+'/'+fname)
			idx = 0
			for i in stream:
				for d in i.elements:					
					if type(d) == note.Note:
						if idx == 0:
							wf.write(d.nameWithOctave)
						else:
							wf.write(' ')
							wf.write(d.nameWithOctave)
						print d.nameWithOctave
						idx += 1
						#wf.write(d.duration.type)
			wf.close()

path = './midi_info/'
parse(path)