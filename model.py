import web

dbn = 'sqlite'
db = '/Users/pwzoii/Sites/db/community.db'
db = web.database(dbn=dbn, db=db)

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