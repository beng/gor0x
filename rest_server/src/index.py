"""
REST Server used to store and return various traits of
MIDI files
"""

import music21

import json

import inspect

import web
import helper.consts as consts
import helper.utility as utility
import ga
import model

urls = (
    '/q/save_midi/(.+)/(.+)', 'SaveMidi',
    '/q/load_traits/(.+)/(.+)', 'LoadTraits',
    '/q/markov/(.+)/(.+)/(.+)/(.+)', 'Markov',
    '/q/spawn_pop/(.+)/(.+)/(.+)/(.+)/(.+)/(.+)', 'SpawnPopulation',
    '/q/artist', 'QueryArtist',
    '/q/song', 'QuerySong',)

render = web.template.render('templates/', base='layout')
title = "REST Server"

########################################################
# QueryArtist
########################################################
class QueryArtist:
    def GET(self):
        """Return JSON of artists"""
        artist = model.music_find_artist()
        return json.dumps(artist)

########################################################
# QuerySong
########################################################
class QuerySong:
    def GET(self):
        """Return JSON of songs"""
        song = model.music_find_song()
        return json.dumps(song)

########################################################
# SpawnPopulation
########################################################
class SpawnPopulation():
    """Use Markov chain to spawn the initial population for the
    requested artist, song, size, and nodes"""

    #def GET(self, artist, song, num_indi, num_traits, size, nodes):
    def GET(self, *args):
        """Experiment with using the same Markov chain pool
        on the entire initial population VS regenerating a
        markov chain for each individual

        Also experiment with the nodes and size values with above

        @TODO ignore lowercase/uppercase for song and artist"""

        # error checking
        if len(args) != 6:
            raise web.notfound()

        # will try to pop an empty list otherwise
        if int(args[5]) > int(args[4]):
            raise web.notfound()

        # shitty results otherwise
        if int(args[4]) < 50:
            raise web.notfound()

        artist = args[0]
        song = args[1]
        num_indi = int(args[2])
        num_traits = int(args[3])
        population = Markov().GET(artist, song, int(args[4]), int(args[5]))
        min = 0
        max = len(population)
        new_population = []
        #print population
        for ni in range(num_indi):
            start, stop = utility.random_sampling(min, max, num_traits)
            trait = {
                'generation': 0,
                'indi_id': ni,
                'artist': artist,
                'song': song,
                'note': population[start:stop]}
            new_population.append(trait)
            #print trait

        return json.dumps(new_population)

########################################################
# SaveMidi
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

        # extract notes, returns generator
        trait_dict = utility.extract_traits(stream, [music21.note.Note])

        # add notes to music collection in mongodb
        for items in trait_dict:
            print 'items : ', items
            items.update({'artist': artist, 'song': song})
            model.music_save_traits(items)

        web.ctx.status = '200 OK'
        return 'explicit 200'

########################################################
# MarkovChain
########################################################
class Markov():
    """Return json of Markov chain"""

    def GET(self, artist, song, size, nodes):
        """Return a Markov chain for the specified artist and song

        Artist and song have to exactly match
        """

        notes = []
        trait = 'note'
        for item in model.music_find_trait(artist, song, trait):
            notes.append(item[trait])
        notes = ' '.join(notes)

        pool = ga.genome(notes, int(size), int(nodes))

        # convert to list
        pool = pool[0].split()

        # remove first and last element because they might be
        # corrupt
        pool.pop(0)   # first
        pool.pop()    # last

        return pool

def notfound():
    msg = "Sorry, the page you were looking for was not found. There was probably a problem with your query!"
    return web.notfound(render.notfound(title, msg))

########################################################
# Run Web Server
########################################################
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.notfound = notfound
    app.run()
