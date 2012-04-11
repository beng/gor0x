import web
import model 
import random
from markov import markov
from music21 import *
urls = (
        '/', 'index',
        '/fitness/(.*)', 'fitness',
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

class fitness():
    fitness_form = web.form.Form(
                             web.form.Textbox('rating', description='Rating:'),
                             web.form.Textbox('indi_id'),
                             )
    
    def to_list(self, q):
        ret = []
        for i in q:
            ret += [(i.pitch, i.duration)]
        return ret
    
    def create_pheno(self, indi):
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
        
if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


