import web

dbn = 'sqlite'
midi_db = '/home/fus-ion/Documents/github/melody_composer_public/db/midi_info.db'
midi_db = web.database(dbn=dbn, db=midi_db)

def insert(table, **kargs):
    """Return ID of record"""
    return midi_db.insert(table, **kargs)
