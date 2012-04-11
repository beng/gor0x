import web
import sqlite3

dbn = 'sqlite'
db = 'C:\\xampp\\htdocs\\database\\community.db'
db = web.database(dbn=dbn, db=db)

def clear_tables():
    db.query("delete from song_2")
    db.query("delete from init_param")
    
def get_max_indi_id():
    return db.query("select max(indi_id) as mid from song_2")[0].mid

def get_trait_id(id):
    var=dict(id=id)
    return db.query("select id as tid from song_2 where indi_id=$id",vars=var)

def get_max_gen():
    return db.query("select max(generation) as gen from song_2")[0].gen

def get_cur_gen(indi):
    try:
        var=dict(indi_id=indi)
        return db.select('song_2', what='generation', where='indi_id=$indi_id', vars=var)[0].generation
    except IndexError:
        return None
    
def get_max_indi_id_by_gen(gen):
    try:
        var = dict(gen=gen)
        return db.query("select max(indi_id) as mid from song_2 where generation=$gen",var)[0].mid
    except IndexError:
        return None
    
def get_num_traits():
    try:
        return db.select('init_param', what="num_traits")[0].num_traits
    except IndexError:
        return None
    
def get_pop_size():
    try:
        return db.select('init_param', what='pop_size')[0].pop_size
    except IndexError:
        return None
    
def get_max_num_gen():
    try:
        return db.select('init_param', what='num_gen')[0].num_gen
    except IndexError:
        return None

def get_indi_traits(indi_id):
    try:
        var = dict(indi_id=int(indi_id))
        return db.select('song_2', what='pitch,duration', where='indi_id=$indi_id', vars=var)
    except IndexError:
        return None
        
def get_num_indi(gen):
    try:
        var=dict(gen=gen)
        return db.query("select count(distinct(indi_id)) as id from song_2 where generation=$gen", var)
    except IndexError:
        return None
    
def get_all_indi_id_by_gen(gen):
    try:
        var = dict(gen=gen)
        return db.query("select distinct(indi_id), fitness from song_2 where generation=$gen",vars=var)
    except IndexError:
        return None

def get_all_info_for_indi(id):
    try:
        return db.select('song_2', what='id,indi_id,generation,fitness,pitch,duration', where='indi_id=$id', vars=locals())
    except IndexError:
        return None

def get_all_indis():
    try:
        return db.query("select distinct(indi_id) from song_2 ")
    except IndexError:
        return None
    
def insert_trait(id,g,p,d):
    db.insert('song_2', indi_id=id, generation=g, pitch=p, duration=d)
    
def insert_fitness(id, val):
    var = dict(indi_id=int(id))
    db.update('song_2', where='indi_id=$indi_id', fitness=val, vars=var)
    
def insert_param(nt,ps,ng):
    db.insert('init_param', num_traits=nt, pop_size=ps, num_gen=ng)

