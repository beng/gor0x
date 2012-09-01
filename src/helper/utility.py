""""
Different utility functions
"""

import json
import music21
import itertools

########################################################
# MIDI Stuff
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
            if type(element) == music21.note.Note:
                trait_list.append(' ' + str(element.nameWithOctave))
    return ''.join(trait_list)

########################################################
# String Stuff
########################################################
def to_path(dir, artist, song, ext):
    """Return string representing file path"""
    return dir + artist + '/' + song + '.' + ext

########################################################
# IO Stuff
########################################################
def load_json(fp):
    with open(fp, 'rb') as tfp:
        data = json.load(tfp)
    return data

def write_json(fp, data):
    with open(fp, 'wb') as tfp:
        json.dump(data, tfp)

def write_text(fp, data):
    with open(fp, 'wb') as tfp:
        tfp.write(data)

def load_text(fp):
    with open(fp, 'rb') as tfp:
        data = tfp.read()
    return data