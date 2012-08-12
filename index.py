"""
@author   Ben G
@email    beg5670@gmail.com
@website  http://github.com/beng
  
this is a genetic algorithm that composes melodies. 
"""

import web
import random

import model
import song_name
import select
import crossover
import individual
import tournament
from markov import markov

from music21 import *

urls = (
        '/', 'index',
        '/fitness/(.*)', 'fitness',
        '/terminate', 'terminate',     
        )

render = web.template.render('templates/', base='layout')

#===============================================================================
# INDEX
#===============================================================================
class index():
    """
    this controller is used to:
        GET:
            -display 2 forms for the GA setup parameters
        POST:
            -retrieve form information
            -save to db
            -redirect to spawn_pop
    """
    song_selection = list(song_name.parse_name('static/pitches/'))

    ga_settings = web.form.Form(
        web.form.Textbox('num_traits', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Number of Traits: '),
        web.form.Textbox('pop_size', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Population Size: '),
        web.form.Textbox('num_gen', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Number of Generations: '),
        web.form.Dropdown('markov_selection', [song for song in song_selection]),
        web.form.Dropdown('selection_type', [('roulette', 'Roulette Wheel'), ('tournament', 'Tournament')]),
        web.form.Textbox('elitism', description='Elitism:'),
        web.form.Textbox('crossover_points', description='Number of Crossover Points:'),
        web.form.Textbox('mutation_rate', description='Mutation Rate:'),)
   
    def GET(self):
        # clear table
        model.clear_tables()
        
        title = 'Melody Composer'
        form = self.ga_settings()
        
        return render.index(title, form)

    def POST(self):
        form = self.ga_settings()
        
        if not form.validates():
            return render.index(form) 
        else:
            pd = web.input()
            params = dict(
                num_traits=pd.num_traits,
                pop_size=pd.pop_size,
                num_gen=pd.num_gen,)
            model.insert('init_param', params)                

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


