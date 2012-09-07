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

def pop_clear_conn():
    pop_coll.remove()

def pop_save_individual(information):
    """Information is a dictionary containing
    individual id, artist, song, note, duration, fitness"""
    try:
        pop_coll.save(information)
    except TypeError:
        print 'Variable is not of type dictionary.'

def pop_find_individual(indi_id):
    try:
        return pop_coll.find({'indi_id': indi_id})
    except TypeError:
        print 'Arguments of improper type'

def pop_find_all():
    try:
        return [indi for indi in pop_coll.find()]
    except TypeError:
        print 'Arguments of improper type'