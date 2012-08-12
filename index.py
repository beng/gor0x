"""
@author   Ben Gelb
@email    beg5670@gmail.com
@website  http://github.com/beng
  
this is a genetic algorithm that composes melodies. 

initial population:
it builds a markov model to spawn the initial population to a) slightly reduce the search space,
and b) act as an influencer. the user has the ability to select <i>x</i> different artists, <i>y</i> different songs, and/or <i>z</i> different genres, where each 
of these items is a midi file. i have written a midi parser, which extracts the melody(pitch, duration) from the midi file(s) and stores it into a text file, which
is then processed by the markov model.

fitness:
for the time being, i am leaving this as an interactive fitness function (i.e. the user has to rate the each song), but i have added some witchcraft to 
reduce the amount of work the user needs to do. i also have plans for adding a neural network to act as an auto-rater. the current rating system uses 
jquery to add interaction to the listening part of the application. the user can move the pitches around to modify the melody to his/her liking. the euclidean distance is used to calculate the fitness value.

selection:
rates are adjustable by the user on the front-end
in addition to roulette wheel and tournament selection, i have added gender based-selection, which mimics rules of human society for mating. i have plans
on adding grouping for clustering purposes where groups are friends and family.

crossover:
n-point crossover. rates are adjustable by the user on the front-end.

mutation:
rates are adjustable by the user on the front-end.

termination:
rates are adjustable by the user on the front-end.

technology:
python
    web.py
html/css/jquery
sql

if you have any questions and/or comments please feel free to contact me.
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



        
class fitness():
    fitness_form = web.form.Form(
                             web.form.Textbox('rating', description='Rating:'),
                             web.form.Textbox('indi_id'),
                             )
    
    def to_list(self, q):
        ''' 
        currently use this and not map(str,q) because it is easier to read and
        cleaner looking to parse the traits while using a forloop than to use
        a single line functional approach
        '''
        ret = []
        for i in q:
            ret += [(i.pitch, i.duration)]
        return ret
    
    def create_pheno(self, indi):
        '''
        converts the individuals pitch, accidental, octave, and rhythm to a music stream
        using the music21 library. the music stream is then used to create a midi file
        '''
        gene = self.to_list(model.get_indi_traits(indi))
        partupper = stream.Part()
        m = stream.Measure()
        for _note, _duration in gene:
            print "note    :", _note
            print "duration    :", _duration
            n = note.Note(_note)
            n.duration.type = _duration
            m.append(n)
        partupper.append(m)    
        return partupper
    
    def convert_midi(self, mfile, indi_id):
        '''
        mfile is a musicstream which is exported to as midi format
        '''
        mf = mfile.midiFile
        name = str(indi_id) + 'song.mid'
        mf.open('static/' + name, 'wb')
        mf.write()
        mf.close()
        return name
    
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
"""
the oracle; this controller decides the fate of where the ga goes next
"""
#===============================================================================   
class helper():
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


class terminate():
    def GET(self):
        title = 'Terminate'
        return render.terminate(title)        
if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


