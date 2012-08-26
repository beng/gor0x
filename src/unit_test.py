import sys
import ga
from music21 import *
import helper.consts as consts
import helper.midi_parser as midi_parser

def spawn_new_midi():
    print midi_parser.extract_traits(converter.parse(consts.name)))

def spawn_pop(**kargs):    
    return ga.Spawn().create_pool(**info)

def main(args):
    if 'spawn_new_midi' in args:
        spawn_new_midi()
    if 'create_stream' in args:
        create_stream()
    if 'create_midi_stream' in args:
        create_midi_stream()
    #if 'spawn_pop' in args[1]:
        #info = {'pop_size':args[2], 'num_traits':args[3], 'influencers':args[4]}
    #    spawn_pop(**info)    

def create_midi_stream():
    req_traits = ['notes', 'chords']
    
    for i in xrange(extract(create_stream(), req_traits)):
        print i


def create_stream():
    """Return json object representing midi file"""
    yield list(*(converter.parse(consts.name)))

def test(stream=None):
    stream = converter.parse()

def extract(stream):
    ret = {}
    for i in stream:
        for d in i.elements:
            if type(d) == chord.Chord:
                ret['chord'] = d.nameWithOctave
            if type(d) == note.Note:
                ret['note'] = d.nameWithOctave
        
    #return [('trait', trait.[arg for arg in args]) for trait in stream]

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