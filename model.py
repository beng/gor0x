import web
import sqlite3

db_path = 'C:\\xampp\\htdocs\\database\\community.db'
db_type = 'sqlite'
db = web.database(dbn=db_type, db=db_path)

def select_query(q,vars=None):
    try:
        return db.query(q,vars)
    except Error:
        return 'Error, man! Focus!'

def insert_query(q,vars=None):
    db.query(q,vars)
    
def clear_tables(tbl):
	# should work, havent tested this yet though
	for i in tbl:
		db.query("delete from ",i)
	
	#db.query("delete from song_2")
	#db.query("delete from child")
    #db.query("delete from init_param")