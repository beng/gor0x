from music21 import *
import os
import fnmatch

'''
parses a midi file for the pitch and octave

p = path
od = output directory
'''
def parse(p,od):
    path = p
    pattern = '*.mid'
    name = ''
    for root, dirs, files in os.walk(path):
        for fname in fnmatch.filter(files,pattern):        
            #print(os.path.join(root,fname))
            name = root.replace('/Users/pwzoii/Sites/ga/v10/midi/', '')
            wf = open(od+'pitches_'+name+'.txt', 'a')
            stream = converter.parse(root+'/'+fname)
            for i in stream:
                for d in i.elements:
                    if type(d) == note.Note:
                        print d.nameWithOctave
                        wf.write(d.nameWithOctave)
                        #wf.write(d.duration.type)
                        wf.write(' ')
            wf.write('\n')
            
            

od='/Users/pwzoii/Desktop/'
path = '/Users/pwzoii/Sites/ga/v10/midi/'
parse(path,od)

    