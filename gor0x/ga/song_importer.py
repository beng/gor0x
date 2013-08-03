import os
import inspect
import sys

from model import Cache
from chromosome import MidiObject

PATH = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
songs = []
cache = Cache(prefix='corpus', db=10)


def get_midi_files(path='assets/midi'):
    for root, dirs, files in os.walk(PATH(path)):
        if dirs:
            artists = dirs

        if files:
            songs.append(files)

    return zip(artists, songs)


def generate_song_obj(files):
    for artist, songs in files.items():
        for song in songs:
            song = song.replace('.mid', "")
            midiobj = MidiObject(artist=artist, title=song)
            midiobj.corpus = midiobj.from_midi()
            cache.hmset(song, midiobj.__dict__)
            print midiobj.__dict__
            print "#"*100
            print cache.hmset(song, midiobj.__dict__)


def objectify(keys):
    '''
    Transform a list of keys into a list of object instances
    '''
    # Get all the model types in this module
    types = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))

    # Split the keys into typename, name
    # keys = [x.split(':', 1) for x in keys]

    # Lookup and instantiate each object

    # objects = [types[typename](name) for typename, name in keys]
    return objects



# files = dict((k, v) for k, v in get_midi_files())
# print generate_song_obj(files)
# x = cache.hmget("winter_allegro", "_corpus")
keys = cache.hkeys("winter_allegro")
# import ast
print objectify(keys)
# y = ast.literal_eval(x[0])
# x = cache.hget("vivaldi", "winter_allegro")
# print h
# print x


# for k, v in files.items():
#     for song in v:
#         print k, song
#         cache.hset(k, song.replace('.mid', ""), 'fejfiweo')
