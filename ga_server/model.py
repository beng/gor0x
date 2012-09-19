import web
from pymongo import Connection

# random variables
host = 'localhost'
port = 9999
db_name = 'community'

connection = Connection(host, port)
db = connection[db_name]

########################################################
# Various Parameters Collection
########################################################
params = db['params']

def params_clear_conn():
    params.remove()

def params_save(init):
    params.save(init)

def params_max_gen():
    return params.find_one()

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

def pop_find_individual(id):
    return pop_coll.find_one({'individual': id})

def pop_find_all():
    return [indi for indi in pop_coll.find()]

def pop_update_user_note(spec,user_note):
    pop_coll.update(spec,user_note)

def pop_update_indi(indi_id, note):
    pop_coll.update({"indi_id": indi_id}, {"$set": {"note": note}})

def pop_update_indi_fitness(indi_id, score):
    pop_coll.update({"indi_id": indi_id}, {"$set": {"fitness": score}})

def pop_max_indi(generation):
    """get max indi of current generation"""
    return pop_coll.find({"generation": generation}, limit=1).sort("indi_id",-1)

def pop_current_generation(indi_id):
    return pop_coll.find_one({"indi_id":indi_id})

def pop_find_trait(indi_id, t_id):
    return pop_coll.find_one({"indi_id": indi_id, "trait_id": t_id})

def pop_update_trait(f, n):
    pop_coll.update(f,n)

def pop_population_by_generation(current_generation):
    """Used for tournament selection"""
    return [individual for individual in pop_coll.find({"generation":current_generation, "trait_id":0})]