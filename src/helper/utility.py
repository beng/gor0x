""""
Different utility functions
"""

import json
import music21
import itertools
#import src.model

########################################################
# MIDI Stuff
########################################################
def extract_corpus(song):
    """Convert midi file into json object)"""
    return music21.converter.parse(song)

def extract_traits(corpus, traits=[]):
    """Check if the listed traits are in the corpus.
    if they are then add them to the list and return it""" 
    # very poor implementation -- fix later just get it
    # working for the time being!
    if traits:
        idx = 0 # hack for testing
        for stream in corpus:
            for element in stream.elements:
                if type(element) in traits:
                    yield({
                        "id": str(idx),
                        "note": str(element.nameWithOctave),
                        "duration": str(element.duration.type)})
                    idx += 1

########################################################
# Random Stuff
########################################################
def to_path(dir, artist, song, ext):
    """Return string representing file path"""
    # fix to optional so i can put other things
    return dir + artist + '/' + song + '.' + ext

def dict_to_string(trait):
    """Convert dictionary to string for
    sending to Markov chain"""
    
    return ' '.join(v for k,v in trait.items())

########################################################
# IO Stuff
########################################################
def write_file(filepath, extension, data):
    """Write to json or txt file"""
    with open(filepath, 'wb') as fp:
        if 'json' in extension:
            json.dump(data, fp)
        else:
            fp.write(data)

def load_file(filepath, extension):
    with open(filepath, 'rb') as fp:
        if 'json' in extension:
            data = json.load(fp)
            return data
        else:
            data = fp.read()
            return data