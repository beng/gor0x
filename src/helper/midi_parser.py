from music21 import *
import os
import fnmatch
import consts

def extract_traits(stream): 
	"""Extract requested traits from midi file
	TODO: modify to take traits as attributes"""
    traits = []
    for i in stream:
        for d in i.elements:
            if type(d) == note.Note:
                traits += [(d.nameWithOctave, d.duration.type)]
            if type(d) == chord.Chord:
                traits += [(d.pitches, d.duration.type)]
    return traits

extract(converter.parse(consts.name))

"""
extract traits -> markov chain -> generate pop
"""



### IGNORE EVERYTHING BELOW -- TESTING!
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

#path = './midi_info/'
#parse(path)

def parse_file():
	#print consts.name
	s = converter.parse(consts.name)
	print get_parts(s)
	#return s
	#print s.show('text')
	#print s.parts.show('text')
	# n1 = note.Note('e4')
	# n1.duration.type = 'whole'
	# n2 = note.Note('d4')
	# n2.duration.type = 'whole'
	# m1 = stream.Measure()
	# m2 = stream.Measure()
	# m1.append(n1)
	# m2.append(n2)
	# partLower = stream.Part()
	# partLower.append(m1)
	# partLower.append(m2)
	# partLower.show('text')
	# print '----------------'
	# data1 = [('g4', 'quarter'), ('a4', 'quarter'), ('b4', 'quarter'), ('c#5', 'quarter')]
	# data2 = [('d5', 'whole')]
	# data = [data1, data2]
	# partUpper = stream.Part()
	# for mData in data:
	# 	m = stream.Measure()
	# 	for pitchName, durType in mData:
	# 		n = note.Note(pitchName)
	# 		n.duration.type = durType
	# 		m.append(n)
	# partUpper.append(m)
	# partUpper.show('text')
	# print '----------------'
	# sCadence = stream.Score()
	# sCadence.insert(0, partUpper)
	# sCadence.insert(0, partLower)
	# sCadence.show('text')
	# print '----------------'
	# print sCadence
	# return partUpper

def export(mfile):
	#mf = mfile.midiFile
	mf = midi.translate.streamToMidiFile(mfile)
	name = 'song.mid'
	mf.open(consts.midi_dir + name, 'wb')
	mf.write()
	mf.close() 
