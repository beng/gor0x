import web
import model 
import random
from markov import markov

urls = (
        '/', 'index',
        )

render = web.template.render('templates/', base='layout')


#===============================================================================
# INDEX
"""
this controller is used to:
    GET:
        -display 2 forms for the GA setup parameters
    POST:
        -retrieve form information
        -save to db
        -redirect to spawn_pop
"""
#===============================================================================
class index():
    init_form = web.form.Form(
                            web.form.Textbox('num_traits', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Number of Traits: '),
                            web.form.Textbox('pop_size', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Population Size: '),
                            web.form.Textbox('num_gen', web.form.notnull, web.form.regexp('^-?\d+$', 'Not a number.'), description='Number of Generations: '),
                            web.form.Dropdown('markov_selection', ['beatles', 'beethovan', 'bach', 'handel', 'essenFolksong', 'haydn', 'josquin']),
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
# SPAWN POP
"""
this controller is used to:
   -spawn an initial population based on the user defined values
   -pitch and octave selected from markov chain
   -duration randomly selected from list
   
TODO:
    -add duration to markov chain
"""
#===============================================================================    
class spawn_pop():
    def init(self, artist):
        self.markov = markov(open('./static/pitches/pitches_' + artist + '.txt'))
        tmp_pitch = self.markov_pitch()
        duration = [ 'whole', 'half', 'quarter', 'eighth', '16th']
        indi_id = 0
        generation = 0
        
        for i in range(0, model.get_pop_size()):
            tmp_pitch = self.markov_pitch()
            dur = random.choice(duration)
            for j in range(0, model.get_num_traits()):
                self.create_trait(indi_id, generation, tmp_pitch[j], dur)
            indi_id += 1
        
        raise web.seeother('/fitness/0')
    
    def markov_pitch(self):
        return self.markov.generate_music(model.get_num_traits())            
    
    def create_trait(self, indi_id, generation, pitch, duration):
        model.insert_trait(indi_id, generation, pitch, duration)

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


