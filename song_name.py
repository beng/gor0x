import os
import fnmatch

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
