""""
Different utility functions
"""

import music21
import itertools

########################################################
# MIDI
########################################################
def extract_corpus(song):
    """Convert midi file into json object)"""
    return music21.converter.parse(song)

def extract_traits(corpus, traits=[music21.note.Note]):
    """Duration will always be included for the time being!
    Everything is casted to string because JSON throws an error
    otherwise"""
    # @TODO add what to do with wrong traits!
    # @TODO decide if i want to use a generator instead

    trait_list = []
    for stream in corpus:
        for element in stream.elements:
            if type(element) in traits:
                if type(element) == music21.note.Rest:
                    trait_list.append({str(type(element)) : "rest", "duration" : element.duration.type})
                else:
                    trait_list.append({str(type(element)) : str(element.pitches), "duration" : element.duration.type})

    return trait_list

def save_traits(fn, loc, traits):
    print 'traits ', traits
    open(loc + fn + '.json', 'wb').write(traits)

########################################################
# Strings
########################################################
def msg(*args):
    """Print out message with variables
    Usage: msg('text',variable,...)"""
    return "".join(str(x) for x in args)

def to_string(items):
    return ' '.join([item for item in items])

########################################################
# Dictionary
########################################################
def find_item(info, *args):
    """Usage: utility.find_item(info, 'chord',...):
    info = list of dictionaries containing song traits
    args = the requested traits"""
    for i in info:
        #print 'in first loop, iteration: '
        for k,v in i.iteritems():
            #print 'checking k,v in iteration: '
            if k in args:
                yield {k:v},

