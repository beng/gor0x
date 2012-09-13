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
        '/fitness', 'Fitness',)

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

        return ga.init_ga(population_info)

class Fitness:
    def GET(self):
        traits = ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4']
        return render.fitness(title, traits)
    
    def POST(self):
        score = 10

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run() 


