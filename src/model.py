import web
from pymongo import Connection

"""
BSON Structure:
    { artist: value,
      song: value,
      id: {
            note: note.pitch,
            duration: duration.type,
      }
    }
"""

# random variables
host = 'localhost'
port = 9999
db_name = 'community'

connection = Connection(host, port)
db = connection[db_name]

########################################################
# Music Collection
########################################################

# music collection specific variables
music_coll = db['music_collection']

def insert_info(information):
    """Insert the extracted information about the midi
    file into the music collection.

    Information is a dictionary containing the artist, song, 
    and traits"""
    music_coll.save(information)

def print_info():
    for i in music_coll.find({'artist': 'Vivaldi'}):
        print i