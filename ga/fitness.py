from music21 import * # horrible, i know, but very lazy right now!

class ManualFitness:
	def euclid_distance(song1, song2):
		# .midi maps the PitchAccidentalOctave (C#3) to the midi equivalent
		# clean the fuck up ASAP!
		return sum([(math.sqrt((pitch.Pitch(song1[i]).midi - pitch.Pitch(song2[i]).midi)) ** 2) for i in range(len(song1))])