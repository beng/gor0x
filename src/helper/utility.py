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

def extract_traits(corpus, traits=[]):
    """Check if the listed traits are in the corpus.
    if they are then add them to the list and return it""" 
    # very poor implementation -- fix later just get it
    # working for the time being!
    if traits:
        trait_list = []
        for stream in corpus:
            for element in stream.elements:
                if type(element) in traits:
                #if type(element) == music21.note.Note:
                    trait_list.append({"note": str(element.nameWithOctave)})
        #return ''.join(trait_list)
        return trait_list
    else:
        return None

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