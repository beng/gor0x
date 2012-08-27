import sys
import ga
from music21 import *
import helper.consts as consts
import helper.midi_parser as midi_parser
import helper.utility as utility

def spawn_new_midi():
    corpus = midi_parser.extract_traits(converter.parse(consts.name))
    pre_gen = utility.find_item(corpus, 'pitch', 'duration')
    
    pop = []

    for indi in pre_gen:
        pop.append(indi[0].values()[0])
    
    # population to string
    pop = utility.to_string(pop)

    # get markov chain of population
    new_pop = ga.genome(pop)
    print new_pop

def main(args):
    if 'spawn_new_midi' in args:
        spawn_new_midi()

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