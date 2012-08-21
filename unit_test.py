import sys
import ga

def spawn_pop(**kargs):    
    return ga.Spawn().create_pool(**info)

def main(args):
    if 'spawn_pop' in args[1]:
        info = {'pop_size':args[2], 'num_traits':args[3], 'influencers':args[4]}
        spawn_pop(**info)    

def usage():
    print "python markov_test <type> <pop_size> <# traits> <influencers>"

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
    else:
        main(sys.argv)