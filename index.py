import web
import model 
import random
urls = (
        '/', 'index',
        )

render = web.template.render('templates/', base='layout')

_number_of_songs = 5    # how many songs to go through in the entire file, -1 = random amount
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
# MARKOV
"""
this controller is used to:
   create a markov chain based off the user selected artist(s)
   
SMALL PORTION OF CODE TAKEN FROM 
        http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
"""
#===============================================================================
class markov(object):
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.pitches = self.file_to_pitches()
        self.pitches_size = len(self.pitches)
        self.pitch_set = []
        self.database()
        
    def file_to_pitches(self):
        self.open_file.seek(0)
        #data = self.open_file.read()
        data = {}
        data[0] = self.open_file.readline()
        i = 0
        while len(data[i]) != 0:
            i += 1
            data[i] = self.open_file.readline()
        
        if _number_of_songs == -1:
            number_of_songs = random.randint(0, i - 1)
        else:
            number_of_songs = _number_of_songs
        ret_data = []
        n = []
        while number_of_songs > 0:
            n.append(random.choice(range(0, i - 1)))
            for p in data[n[-1]].split():
                ret_data.append(p)
            number_of_songs -= 1
        return ret_data
        
    def triples(self):
        if len(self.pitches) < 3:
            return
    
        for i in range(len(self.pitches) - 2):
            yield (self.pitches[i], self.pitches[i + 1], self.pitches[i + 2])
            
    def database(self):
        for p1, p2, p3 in self.triples():
            if p1 not in self.pitch_set:
                self.pitch_set.append(p1)
            if p2 not in self.pitch_set:
                self.pitch_set.append(p2)
            if p3 not in self.pitch_set:
                self.pitch_set.append(p3)
            key = (p1, p2)
            if key in self.cache:
                self.cache[key].append(p3)
            else:
                self.cache[key] = [p3]
                
    def get_next_pitch(self, p1, p2):
        return random.choice(self.cache[(p1, p2)])
    
    def get_next_pitches(self, p1, p2, size=500):
        n = len(self.cache)
        while ((p1, p2) not in self.cache) and n > 0:
            p2 = random.choice(self.pitch_set)
            n -= 1
        if n == 0:
            (p1, p2) = random.choice(self.cache.keys())
            
        gen_pitches = []
        for i in xrange(size):
            gen_pitches.append(p1)
            p1, p2 = p2, random.choice(self.cache[(p1, p2)])
        gen_pitches.append(p2)
        return gen_pitches
                
    def generate_music(self, size=500):
        seed = random.randint(0, self.pitches_size - 3)
        seed_pitch, next_pitch = self.pitches[seed], self.pitches[seed + 1]
        p1, p2 = seed_pitch, next_pitch
        gen_pitches = []
        for i in xrange(size):
            gen_pitches.append(p1)
            n = len(self.cache)
            while ((p1, p2) not in self.cache) and n > 0:
                p2 = random.choice(self.pitch_set)
                n -= 1
            if n == 0:
                (p1, p2) = random.choice(self.cache.keys())
            p1, p2 = p2, random.choice(self.cache[(p1, p2)])
        gen_pitches.append(p2)
        return gen_pitches
   
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


