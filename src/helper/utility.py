""""
Different utility functions
"""

import json
import music21
import itertools

########################################################
# MIDI
########################################################
def extract_corpus(song):
    """Convert midi file into json object)"""
    return music21.converter.parse(song)

def extract_traits(corpus):
    # very poor implementation -- fix later just get it
    # working for the time being!
    trait_list = []
    for stream in corpus:
        for element in stream.elements:
            if type(element) == music21.note.Rest:                
                trait_list.append({"Rest" : "rest", "duration" : element.duration.type})
            elif type(element) == music21.note.Note:
                trait_list.append({"Note" : str(element.pitches), "duration" : element.duration.type})
            elif type(element) == music21.chord.Chord:
                trait_list.append({"Chord" : str(element.pitches), "duration" : element.duration.type})
    return trait_list

def load_json(fp):
    with open(fp, 'rb') as tfp:
        data = json.load(tfp)
    return data

def write_json(fp, data):
    with open(fp, 'wb') as tfp:
        json.dump(data, tfp)

########################################################
# String Stuff
########################################################
def to_path(dir, artist, song, ext):
    """Return string representing file path"""
    return dir + artist + '/' + song + '.' + ext