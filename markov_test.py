from helper import Markov
import sys
import ga

def generate_markov(**kargs):
    """Generate Markov Chain for requested influencer"""
    return Markov().markov_pitch(**kargs)

def generate_indi(**kargs):
    ga.genome(**kargs)

def main(args):
    if 'markov' in args[1]:
        generate_markov(**{"num_traits" : args[2], "influencers" : args[3]})
    if 'indi' in args[1]:


def usage():
    print "python markov_test <# traits> <influencer>"

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    else:
        main(sys.argv)