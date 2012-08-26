import itertools

""""
Different utility functions
"""
########################################################
# Strings
########################################################
def msg(*args): 
    """Print out message with variables
    Usage: msg('text',variable,...)"""
    return "".join(str(x) for x in args)


########################################################
# Dictionary
########################################################
def find_item(info, *args):
    """Usage: utility.find_item(info, 'chord'):
    info = list of dictionaries containing song traits
    args = the requested traits"""
    for i in info:
        print 'in first loop, iteration: ',i
        for k,v in i.iteritems():
            print 'checking k,v in iteration: ', i
            if k in args:
                yield {k:v},

