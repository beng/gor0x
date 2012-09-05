"""
@author   Ben G

this is a genetic algorithm that composes melodies.
"""

import music21

import json

import web

#import models.midi_info as mim
import helper.consts as consts
import helper.utility as utility
import ga
import model

urls = (
    '/', 'Index',
    '/save_midi/(.+)/(.+)', 'SaveMidi',
    '/load_traits/(.+)/(.+)', 'LoadTraits',
    '/markov/(.+)/(.+)/(.+)/(.+)', 'Markov',
    '/ga/spawn/(.+)/(.+)', 'SpawnPopulation',
    '/ga/fitness', 'Fitness',
    '/interactive', 'Interactive',
    '/mongo', 'MongoTesting',)

render = web.template.render('templates/', base='layout')
title = "Melody Composer"

########################################################
# Test
########################################################
class Index():
    def GET(self):
        return "Hello"

########################################################
# Mongo Testing
########################################################
class MongoTesting():
    def GET(self):
        return model.print_info()

########################################################
# Interactive Testing
########################################################
class Interactive():
    def GET(self):
        artist = 'vivaldi'
        song = 'winter_allegro'
        data = Markov().GET(100, 5, artist, song)
        data = data[0].split()
        return render.interactive(title, data)


########################################################
# Return Population of X individuals and Y traits each
########################################################
class SpawnPopulation():
    def GET(self, num_indi, num_traits):
        # @TODO spawn a population!
        artist = 'vivaldi'
        song = 'winter_allegro'
        data = dict(size=10, nodes=4, artist=artist, song=song)

########################################################
# Save MIDI to Server
########################################################
class SaveMidi():
    def GET(self, artist, song):
        """Export MIDI file to specified filetype
        Checks to see if the requested MIDI file exists
        on my server. If it does, extracts the requested
        traits from it using the music21 library.
        @TODO If it doesn't I need to return an error
        """

        # convert to stream
        artist = artist.capitalize()
        fp = utility.to_path(consts.midi_dir, artist, song, 'mid')
        stream = utility.extract_corpus(fp)

        # extract notes
        trait_dict = utility.extract_traits(stream, [music21.note.Note])

        for items in trait_dict:
            model.insert_info(items)

        web.ctx.status = '200 OK'
        return 'explicit 200'

########################################################
# Generate Markov Chain
########################################################
class Markov():
    """Return json of Markov chain"""

    def GET(self, size, nodes, artist, song):
        """Return a Markov chain for the specified artist and song"""

        artist = artist.capitalize()
        extension = 'json'
        filepath = utility.to_path(consts.pitch_dir, artist, song, extension)

        # create string containing only the value of the traits
        data = utility.load_file(filepath, extension)
        mc_pop = ' '.join(utility.dict_to_string(trait) for trait in data)

        # generate a single individual (genome)
        pool = ga.genome(mc_pop, size=int(size), nodes=int(nodes))

        return pool

########################################################
# Run Web Server
########################################################
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
