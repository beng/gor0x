"""
@author   Ben Gelb
@email    beg5670@gmail.com
@website  http://github.com/beng
  
slowly refactoring to get rid of extra things. 
adding in interactive fitness to with jQuery
"""

import web
import model 
import random
import song_name
from markov import markov
from music21 import *

import select
import crossover

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

    init_form = web.form.Form(
                            web.form.Textbox('num_traits', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Number of Traits: '),
                            web.form.Textbox('pop_size', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Population Size: '),
                            web.form.Textbox('num_gen', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Number of Generations: '),
                            web.form.Dropdown('markov_selection', [i for i in song_selection]),
                            )

    setting_form = web.form.Form(
                                web.form.Dropdown('selection_type', [('roulette', 'Roulette Wheel'), ('tournament', 'Tournament')]),
                                web.form.Textbox('elitism', description='Elitism:'),
                                web.form.Textbox('crossover_points', description='Number of Crossover Points:'),
                                web.form.Textbox('mutation_rate', description='Mutation Rate:'),
                                )
   
    def GET(self):
        # clear table
        model.clear_tables()
        
        title = 'Melody Composer'
        init_f = self.init_form()
        sf = self.setting_form()
        
        return render.index(title, init_f, sf)

    def POST(self):
        init_f = self.init_form()
        
        if not self.init_form.validates():
            return render.index(init_f) 
        else:
            fp = web.input()       
            print fp.selection_type    
            model.insert_param(fp.num_traits, fp.pop_size, fp.num_gen)
            #raise web.seeother('/spawn_pop')
            spawn_pop().init(fp.markov_selection)

#===============================================================================   
# FITNESS
#===============================================================================           
class fitness():
    fitness_form = web.form.Form(
                             web.form.Textbox('rating', description='Rating:'),
                             web.form.Textbox('indi_id'),
    )
    
    def GET(self, indi):
        title = 'Fitness'
        ff = self.fitness_form()
        ff.indi_id.set_value(indi)
        song_name = self.convert_midi(self.create_pheno(indi), indi)
        l = model.get_num_indi(0)[0].id
        cur_gen = model.get_cur_gen(indi)
        all_indi = model.get_all_indi_id_by_gen(cur_gen)
        song_names = []
        for i in all_indi:
            song_names += [self.convert_midi(self.create_pheno(i.indi_id), i.indi_id)]
        return render.fitness(title, ff, song_name, l)
    
    def POST(self, indi):
        post = web.input()
        print post.fv
        model.insert_fitness(indi, post.fv)
        
        # check to see what to do next
        helper().check(int(indi))

#===============================================================================
# HELPER
#===============================================================================   
class helper():
    """
    the oracle; this controller decides the fate of where the ga goes next
    """
    def check(self, indi): 
        # is the individual that was just evaluated the last in the generation?
        if int(indi) == model.get_max_indi_id_by_gen(model.get_cur_gen(int(indi))):
            # check if termination requirements are met
            if model.get_cur_gen(indi) >= model.get_max_num_gen():
                # they are, end ga
                raise web.seeother('/terminate')
            else:
                # they are not, move onto selection
                select().select(int(indi))
        # are there more to evaluate?
        elif int(indi) <= model.get_max_indi_id_by_gen(model.get_cur_gen(int(indi))):
            raise web.seeother('/fitness/' + str(int(indi) + 1))
        # just in case exit condition
        else:
            raise web.seeother('/terminate')       

#===============================================================================
# TERMINATE
#===============================================================================   
class terminate():
    def GET(self):
        title = 'Terminate'
        return render.terminate(title)  

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


