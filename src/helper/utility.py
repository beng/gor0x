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

def extract_traits(corpus, influencer, traits=[]):
    """Duration will always be included for the time being!
    Everything is casted to string because JSON throws an error
    otherwise"""    
    if not traits:
        return {}   
    else:
        trait_list = {"influencer" : influencer, "info" : []}
        for stream in corpus:
            for element in stream.elements:
                if type(element) in traits:
                    if type(element) == music21.note.Rest:
                        trait_list['info'].append({"Rest" : "rest", "duration" : element.duration.type})
                    else:
                        trait_list['info'].append({str(type(element)) : str(element.pitches), "duration" : element.duration.type})
        return trait_list

def save_traits(fn, loc, traits):
    with open(loc + fn + '.json', 'wb') as fp:
        json.dump(traits, fp)

def load_traits(fn, loc):
    with open(loc + fn + '.json', 'rb') as fp:
        traits = json.load(fp)
        #print traits
        print type(traits)
        return traits

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
# def find_item(info, *args):
#     """Usage: utility.find_item(info, 'chord',...):
#     info = list of dictionaries containing song traits
#     args = the requested traits"""
#     for i in info:
#         #print 'in first loop, iteration: '
#         for k,v in i.iteritems():
#             #print 'checking k,v in iteration: '
#             if k in args:
#                 yield {k:v},

# def find_item(info, *args):
#     for k,v in info.items():
#         if k in args[0]:
#             for i in v:
#                 print i.keys()
#                 if i in args[1:]:
#                     print i
#                 #print i[args[1:]]

