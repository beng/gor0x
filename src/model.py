import web
from pymongo import Connection

"""
BSON Structure:
    { artist: song,
      id: {
            note: note.pitch,
            duration: duration.type,
      }
    }

E.g. { "Antonio Vivaldi": "Winter Allegro",
        0: {
             "note": "C#4",
             "duration": "quarter",
        }
     }
"""

host = 'localhost'
port = 9999
db_name = 'community'

connection = Connection(host, port)
db = connection[db_name]
music_coll = db['music_collection']

def add_music(name, song):
    music_coll.insert({name: song})

def find_all_music():
    return music_coll.find_one()

add_music('Vivaldi', 'Winter Allegro')
print find_all_music()
