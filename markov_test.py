from helper import Markov
import sys

def generate_markov(**kargs):
    """Generate Markov Chain for requested influencer"""
    return Markov().markov_pitch(**kargs)

def main(args):
    generate_markov(**{"num_traits" : args[1], "influencers" : args[2]})

def usage():
    print "python markov_test <# traits> <influencer>"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        main(sys.argv)