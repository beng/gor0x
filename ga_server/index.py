import web
import json
import ast
import model
import ga

from pyevolve import G1DList
from pyevolve import GSimpleGA

urls = (
        '/', 'Index',
        '/population/(.*)', 'Population',
        '/fitness/(.+)', 'Fitness',)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())
title = 'GA Server'

class Index:
    def GET(self):
        # clear population collection
        model.pop_clear_conn()

        # call REST server for a list of available artists
        br = web.Browser()
        br.open('http://localhost:8000/q/artist') # make dynamic later
        songs = json.loads(br.get_text())
        return render.index(title, songs)

    def POST(self):
        """
        TODO add validation to make sure only integers are allowed
        TODO bounds checking on mc_size and mc_nodes!
        """
        pd = web.input()
        song = 'winter_allegro'
        population_info = {
            'artist': pd.influencer,
            'song': song,   # MAKE DYNAMIC LATER!
            'num_indi': pd.pop_size,
            'num_traits': pd.num_traits,
            'num_gen': pd.num_gen,
            'size': pd.mc_size,
            'nodes': pd.mc_nodes,
        }

        #return ga.init_ga(population_info)
        population = GA().spawn_population(population_info)
        
        # have to save each individual because population is a list
        # and mongo won't let you save a list as the collection
        for individual in population:    
            model.pop_save_individual(individual)

        raise web.seeother('/fitness/0')

class Fitness:
    def GET(self, id):
        individual = model.pop_find_individual(int(id))
        return render.fitness(title, individual, id)
    
    def POST(self, id,):
        """A new request will be received for each {note,duration}"""
        pd = web.input()

        # save input to mongo
        

class GA:
    def spawn_population(self, population_info):
        # parameters for calling the server
        root = 'http://localhost:8000/q/spawn_pop/'
        params = [population_info['artist'], population_info['song'], population_info['num_indi'], population_info['num_traits'], population_info['size'], population_info['nodes']]
        params = root +'/'.join(params)
        br = web.Browser()
        br.open(params)
        traits = json.loads(br.get_text())

        # add content to population collection
        # for trait in traits:
        #     model.pop_save_individual(trait)
        return traits

    def crossover():
        pass

    def select():
        pass

    def mutate():
        pass

    def terminate():
        pass

    def fitness():
        pass

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run() 


