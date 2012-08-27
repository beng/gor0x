import sys
import ga
from music21 import *
import helper.consts as consts
import helper.midi_parser as midi_parser
import helper.utility as utility

def spawn_new_midi():
    corpus = midi_parser.extract_traits(converter.parse(consts.name))
    #for c in corpus:
        #print 'corpus :', c
    # requested traits
    pre_gen = utility.find_item(corpus, 'pitch', 'duration')
    
    pop = []

    for indi in pre_gen:
        print indi[0].values()   # returns the string value of the trait
        pop.append(indi[0].values()[0])
    
    # population to string
    pop = utility.to_string(pop)
    print '------------'
    print 'POP TO STRING'
    print '------------'
    print pop
    print '------------'
    print '------------'
    
    new_pop = ga.create_pool(1,pop)
    num_rounds = 1000
    #print ''.join([next(new_pop) for k in xrange(num_rounds)])
    for i in new_pop:
        print i

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