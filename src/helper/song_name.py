import os
import fnmatch

'''
this class goes through the specified path and 
extracts the artist name from the pitch_artistname.txt file
so the artist names can be dynamically loaded into the 
markov selection dropdown on the index page
'''
def parse_name(p):
    path = p
    pattern = '*.txt'
    ret = []
    
    for root, dirs, files in os.walk(path):
        for fname in fnmatch.filter(files,pattern):
            # truncating "pitches_" and ".txt" 
            # from "pitches_artistName.txt"
            ret += [fname[8:len(fname)-4]]
    return ret
