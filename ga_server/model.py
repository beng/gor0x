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
    pop_coll.save(information)

def pop_find_individual(indi_id):
    return pop_coll.find({'indi_id': indi_id})

def pop_find_all():
    return [indi for indi in pop_coll.find()]
