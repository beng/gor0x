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
import ga

urls = (
    '/', 'Index',
    '/save_midi/(.+)/(.+)', 'SaveMidi',
    '/load_traits/(.+)/(.+)', 'LoadTraits',
    '/markov/(.+)/(.+)/(.+)/(.+)', 'Markov',)

render = web.template.render('templates/', base='layout')
title = "Melody Composer"

########################################################
# Return JSON file containing traits
########################################################
class Index():
    def GET(self):
        return "Hello"

########################################################
# Return JSON file containing traits
########################################################
class LoadTraits():
    def GET(self, artist, song):
        artist = artist.capitalize()
        fp = utility.to_path(consts.pitch_dir, artist, song, 'txt')
        data = utility.load_text(fp)

########################################################
# Save MIDI to Server
########################################################
class SaveMidi():
    def GET(self, artist, song):
        """Export MIDI file to specified filetype"""

        # convert to stream
        artist = artist.capitalize()
        fp = utility.to_path(consts.midi_dir, artist, song, 'mid')
        stream = utility.extract_corpus(fp)

        # extract notes
        trait_list = utility.extract_traits(stream, [music21.note.Note])

        # write to file
        extension = 'json'
        filepath = utility.to_path(consts.pitch_dir, artist, song, extension)
        utility.write_file(filepath, extension, trait_list)
        
        web.ctx.status = '200 OK'
        return 'explicit 200'

########################################################
# Generate Markov Chain
########################################################
class Markov:
    """Return json of Markov chain"""

    def GET(self, size, nodes, artist, song):
        """Return a Markov chain for the specified artist and song"""
        artist = artist.capitalize()
        extension = 'json'
        filepath = utility.to_path(consts.pitch_dir, artist, song, extension)
        data = utility.load_file(filepath, extension)
        mc_pop = ''

        for trait in data:
            # append to string
            print utility.dict_to_list(trait)
            #mc_pop.append(utility.list_to_string(utility.dict_to_list(trait)))
        #print mc_pop
        #pool = ga.genome(data, size=int(size), nodes=int(nodes))
        return data
        #return pool

        #web.header('Content-Type', 'application/json')
        #return json.dumps({artist : pool, 'settings' : {'size' : size, 'nodes' : nodes}})

########################################################
# Run Web Server
########################################################
if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run()
