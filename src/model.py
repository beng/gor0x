import web
from pymongo import Connection

"""
Fuck it. Shit ain't even used anymore.
"""

host = 'localhost'
port = '9999'
db_name = 'community'

connection = Connection(host, port)
db = connection[db_name]
music_coll = db['music_collection']

