import web
import sqlite3

dbn = 'sqlite'
db = '/Users/pwzoii/Sites/db/community.db'
db = web.database(dbn=dbn, db=db)

def clear_tables():
    db.query("delete from song_2")
    db.query("delete from init_param")

def insert(table, params):
    db.insert(table, **params)