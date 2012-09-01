import web

dbn = 'sqlite'

db = './db/community.db'
db = web.database(dbn=dbn, db=db)

midi_db = './db/midi.db'
midi_db = web.database(dbn=dbn, db=midi_db)

#############################################################
# MIDI DB (SONG META INFO, ETC) 
#############################################################
def m_insert(table, **kargs):
    return midi_db.insert(table, **kargs)

#############################################################
# DB 
#############################################################
def clear_tables():
    db.query("delete from params")
    db.query("delete from song")

def insert(table, kargs):
    return db.insert(table, **kargs)

def get_max_gen():
    q = db.query("SELECT max(generation) as gen FROM song")[0].gen
    return q if q else 0

def get_traits(indi_id):
    return db.select('song', what='trait', vars=indi_id, where='indi_id=$indi_id')