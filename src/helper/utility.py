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
    # @TODO add what to do with wrong traits!
    trait_list = []

    for i in corpus:        
        for d in i.elements:
            if type(d) == music21.note.Note:    
                trait_list.append({"pitch" : str(d.nameWithOctave), "duration" : str(d.duration.type)})
            elif type(d) == music21.chord.Chord:                
                trait_list.append({"chords" : str(d.pitches), "duration" : str(d.duration.type)})

    return trait_list
    
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

