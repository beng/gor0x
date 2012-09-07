"""
REST Server used to store and return various traits of
MIDI files
"""

import music21

import json

import web
import helper.consts as consts
import helper.utility as utility
import ga
import model

urls = (
    '/save_midi/(.+)/(.+)', 'SaveMidi',
    '/load_traits/(.+)/(.+)', 'LoadTraits',
    '/markov/(.+)/(.+)/(.+)/(.+)', 'Markov',
    '/spawn_pop/(.+)/(.+)/(.+)/(.+)', 'SpawnPopulation',)

render = web.template.render('templates/', base='layout')
title = "REST Server"

########################################################
# Return Population of X individuals and Y traits each
########################################################
class SpawnPopulation():
    """Use Markov chain to spawn the initial population for the
    requested artist, song, size, and nodes"""

    def GET(self, artist, song, num_indi, num_traits, size, nodes):
        """Experiment with using the same Markov chain pool 
        on the entire initial population VS regenerating a 
        markov chain for each individual

        Also experiment with the nodes and size values with above"""

        num_indi = int(num_indi)
        num_traits = int(num_traits)
        population = Markov().GET(int(size), int(nodes), artist, song)
        min = 0
        max = len(population)
        new_population = []

        for ni in range(num_indi):
            current_gen = 0
            for nt in range(num_traits):
                start, stop = utility.random_sampling(min, max, num_traits)
                trait = {
                    'generation': current_gen,
                    'indi_id': ni,
                    'trait_id': nt,
                    'artist': artist,
                    'song': song,
                    'note': population[start:stop]}
                new_population.append(trait)
            current_gen += 1

        return json.dumps(new_population)

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

        # extract notes, returns generator
        trait_dict = utility.extract_traits(stream, [music21.note.Note])

        # add notes to music collection in mongodb
        for items in trait_dict:
            items.update({'artist': artist, 'song': song})
            model.music_save_traits(items)

        web.ctx.status = '200 OK'
        return 'explicit 200'

########################################################
# Generate Markov Chain
########################################################
class Markov():
    """Return json of Markov chain"""

    def GET(self, size, nodes, artist, song):
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

########################################################
# Run Web Server
########################################################
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
