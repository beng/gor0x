"""
@author   Ben G
@email    beg5670@gmail.com
@website  http://github.com/beng

this is a genetic algorithm that composes melodies.
"""

import music21

import json

import web

import models.midi_info as mim
import helper.consts as consts
import helper.utility as utility

urls = (
    '/save_midi/(.+)/(.+)', 'SaveMidi',)

render = web.template.render('templates/', base='layout')
title = "Melody Composer"

########################################################
# Save MIDI to DB
########################################################
class SaveMidi():
    def GET(self, artist, song):
        """Export MIDI file to JSON"""

        # convert to stream
        artist = artist.capitalize()
        fp = utility.to_path(consts.midi_dir, artist, song, 'mid')
        stream = utility.extract_corpus(fp)

        # extract chord, pitch, rest, and duration from stream
        trait_list = utility.extract_traits(stream)

        # write to JSON file
        with open(consts.pitch_dir + artist + '_' + song + '.json', 'wb') as tfp:
            json.dump(trait_list, tfp)
        
        web.ctx.status = '200 OK'
        return 'explicit 200'
        
        
########################################################
# Run Web Server
########################################################
if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run()
