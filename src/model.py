import web
from pymongo import Connection

# random variables
host = 'localhost'
port = 9999
db_name = 'community'

connection = Connection(host, port)
db = connection[db_name]

########################################################
# Population Collection
########################################################
pop_coll = db['pop_coll']

def pop_save_population(information):
    """Information is a dictionary containing
    individual id, artist, song, note, duration, fitness"""
    try:
        pop_coll.save(information)
    except TypeError:
        raise 'Variable is not of type dictionary.'

def pop_find_individual(indi_id):
    try:
        #return pop_coll.find()
        pass
    except TypeError:
        print 'Arguments of improper type'

########################################################
# Music Collection
########################################################

# music collection specific variables
music_coll = db['music_collection']

def music_save_traits(information):
    """Insert the extracted information about the midi
    file into the music collection.

    Information is a dictionary containing the artist, song, 
    and traits"""
    
    try:
        music_coll.save(information)
    except TypeError:
        raise 'Variable is not of type dictionary.'

def print_info():
    for i in music_coll.find({'artist': 'Vivaldi'}):
        print i

def music_find_trait(artist, song, trait):
    return music_coll.find({'artist': artist, 'song': song, trait: {"$type": 2}})