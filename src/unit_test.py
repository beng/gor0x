"""
Random shit in here for testing random shit -- don't ask questions
"""

import sys
import ga
from music21 import *
import helper.consts as consts
import helper.midi_parser as midi_parser
import helper.utility as utility

def type_cast():
    convert = utility.type_cast('1', int)

def trait_extraction(traits=[note.Note, note.Rest]):
    utility.extract_traits(utility.extract_corpus(consts.name), traits)

def spawn_new_midi():
    corpus = midi_parser.extract_traits(converter.parse(consts.name))
    pre_gen = utility.find_item(corpus, 'pitch', 'duration')
    
    pop = []

    for indi in pre_gen:
        pop.append(indi[0].values()[0])
    
    # population to string
    pop = utility.to_string(pop)

    # get markov chain of population
    new_pop = ga.genome(pop,10,5)
    print new_pop

def main(args):
    if 'spawn_new_midi' in args:
        spawn_new_midi()
    if 'trait_extraction' in args:
        trait_extraction()
    if 'type_cast' in args:
        type_cast()

def usage():
    print "python markov_test <type> <pop_size> <# traits> <influencers>"

if __name__ == '__main__':
    """
    if len(sys.argv) != 5:
        usage()
    else:
        main(sys.argv)
    """
    main(sys.argv)