"""
import video-game midis to mongo collection
"""
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import model
import consts
import utility
import music21

files_in_dir = os.listdir(consts.midi_dir+'/Video_game')

artist = 'Video_game'
song = ''
for f in files_in_dir:
    if '.DS_Store' not in f:
        song = f[:len(f)-4] # omit .mid
        stream = utility.extract_corpus(consts.midi_dir+'/Video_game/'+f)
        trait_dict = utility.extract_traits(stream, [music21.note.Note])        
        for items in trait_dict:            
            items.update({'artist': artist, 'song': song})
            print 'items : ', items
            model.music_save_traits(items)