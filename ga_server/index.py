import web
import json
import model
import random
#import ga
import math
import music21

urls = (
        '/', 'Index',
        '/fitness/(.+)', 'Fitness',
        '/save_fitness/(.+)', 'SaveFitness',
        '/terminate', 'Terminate',
        '/test', 'Test',)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())
title = 'GA Server'

class Test:
    def GET(self):
        return render.test(title)
class GA:
    """Miniature genetic algorithm library"""

    def create_population(self, artist, song, num_indi, num_traits, size, nodes):
        root = 'http://localhost:8000/q/spawn_pop/'
        params = root +'/'.join([artist, song, str(num_indi), str(num_traits), str(size), str(nodes)])
        br = web.Browser()
        br.open(params)
        population = json.loads(br.get_text())
        
        return population

    def euclidean_distance(self, song1, song2):
        """The songs are lists of notes converted to their midi value
        @TODO clean this up. it's too messy"""
        try:
            score = 0
            for i in range(len(song1)):
                score += math.sqrt((music21.pitch.Pitch(song1[i]).midi - int(music21.pitch.Pitch(song2[i]).midi)) ** 2)
            return score
        except ValueError:
            raise 'Songs must be the same length!'

    def fate(self,indi_id):
        """Use the individual that was just evaluated to determine
        where we are in the grand scheme of things. How many more individuals
        of the current generation need to be evaluated? Are the termination
        requirements met? Are we ready to move to the next generation? Etc..."""

        indi_id = int(indi_id)
        max_gen = int(model.params_max_gen()['max_gen'])
        current_generation = int(model.pop_current_generation(indi_id)['generation'])
        max_indi = int(model.pop_max_indi(current_generation)[0]['indi_id'])

        if indi_id == max_indi:
            # termination requirements met?
            if current_generation >= max_gen:
                raise web.seeother('/terminate')
            else:
                # current generation over, start mating!
                self.select(current_generation, indi_id)
        elif indi_id <= max_indi:
            raise web.seeother('/fitness/'+str(indi_id+1))
        else:
            raise web.seeother('/terminate')

    def select(self, current_generation, current_indi_id):
        """Selection phase -- right now I've only implemented tournament
        selection. Use current_generation to grab all individuals of 
        previous generation

        @TODO redo this entire method before you get shot
        @TODO redo this entire method before you get shot
        @TODO redo this entire method before you get shot
        @TODO redo this entire method before you get shot
        """
        print 'in selection'
        current_indi_id = int(current_indi_id)
        current_generation = int(current_generation)
        num_rounds = 2
        k = 2
        winner = []
        population = model.pop_population_by_generation(current_generation)

        # get list of winning individuals
        for i in range(num_rounds):
            winner.append(self.tournament(k,population))
        
        max_indi = int(model.pop_max_indi(current_generation)[0]['indi_id'])

        for i in range(model.params_num_indi()['num_indi']):
            # select random winners to be parent
            p1 = random.choice(winner)            
            p2 = random.choice(winner)
            _p1 = []
            _p2 = []
            artist = ''
            song = ''

            # find each parents traits
            for item in model.pop_find_individual(int(p1['indi_id'])):
                artist = item['artist']
                song = item['song']
                _p1.append(item['user_note'])

            for item in model.pop_find_individual(int(p2['indi_id'])):
                _p2.append(item['user_note'])

            # create child among parents
            child1, child2 = self.crossover(_p1,_p2)
            
            # save child
            t_id = 0
            # clean the fuck up
            for i in child1:
                print "max indi loop c1 ", max_indi+1
                information = {
                    "artist": artist,
                    "song": song,
                    "indi_id": max_indi+1, 
                    "trait_id":t_id, 
                    "generation": current_generation+1,
                    "fitness": 0,
                    "note": i,
                    "user_note": i,
                    "duration": 1,}
                t_id += 1
                model.pop_save_individual(information)
            t_id = 0
            for i in child2:
                print "max indi loop c2", max_indi+2
                information = {
                    "artist": artist,
                    "song": song,
                    "indi_id": max_indi+2, 
                    "trait_id":t_id, 
                    "generation": current_generation+1,
                    "fitness": 0,
                    "note": i,
                    "user_note": i,
                    "duration": 1,}
                t_id += 1
                model.pop_save_individual(information)
            max_indi += 2

        raise web.seeother('/fitness/' + str(current_indi_id+1))

    def tournament(self, k, population):
        """Tournament Selection

        k = subset size
    
        1. a random subset of size, k, from the given generation is extracted 
        2. sort the pool by fitness value
        3. return the winner, the individual with the highest fitness value"""

        # find k best individuals in population
        pool = []
        for i in range(k):
            individual = random.choice(population)
            print "INDIVIDUAL ", individual
            if individual not in pool:
                pool.append(individual)

        # select individual with the highest fitness score
        winner = sorted(pool, key=lambda x: -x['fitness'])[0]

        return winner
    
    def crossover(self, parent1, parent2):
        """Parents are a list of notes!

        @TODO make sure that the child is the same length
        as the parents otherwise will have problems with
        euclidean distance"""

        print 'in crossover'
        try:
            split = random.randint(1, len(parent1))
            return parent1[:split] + parent2[split:], parent2[:split] + parent1[split:]
        except ValueError:
            raise "Parents aren't the same length!"

    def create_pheno(self, indi_id):
        '''
        converts the individuals pitch, accidental, octave, and rhythm to a music stream
        using the music21 library. the music stream is then used to create a midi file
        '''        
        individual = model.pop_find_individual(int(indi_id))
        gene = []

        for i in individual:
            gene.append(i['user_note'])

        partupper = music21.stream.Part()
        m = music21.stream.Measure()
        for _note in gene:
            n = music21.note.Note(_note)
            print n
            #n.duration.type = "half"
            m.append(n)
        partupper.append(m)    
        return partupper
    
    def convert_midi(self, mfile, indi_id):
        '''
        mfile is a musicstream which is exported to as midi format
        '''
        mf = mfile.midiFile
        name = str(indi_id) + '_song.mid'
        mf.open('static/' + name, 'wb')
        mf.write()
        mf.close()
        return name

class Index:
    def GET(self):
        """Render the parameter initialization view"""
        model.pop_clear_conn()
        model.params_clear_conn()
        # call REST server for a list of available songs
        br = web.Browser()
        br.open('http://localhost:8000/q/song') # make dynamic later
        songs = json.loads(br.get_text())
        
        return render.index(title, songs)

    def POST(self):
        pd = web.input()
        num_gen = pd.num_gen           
        song = pd.influencer

        # call REST server to get artist
        br = web.Browser()
        br.open('http://localhost:8000/q/songartist/' + song) # make dynamic later
        artist = json.loads(br.get_text())[0]
        print artist

        num_indi = pd.pop_size
        num_traits = pd.num_traits
        size = pd.mc_size
        nodes = pd.mc_nodes

        model.params_save({"max_gen":int(num_gen)})
        model.params_save({"num_indi": int(num_indi)})

        population = GA().create_population(artist, song, num_indi, num_traits, size, nodes)
        
        for indi in population:
            for nt in range(int(num_traits)):
                trait = {
                    "artist": indi['artist'],
                    "song": indi['song'],
                    "indi_id": int(indi['indi_id']),
                    "trait_id": nt,
                    "generation": int(indi['generation']),
                    "fitness": 0,
                    "note": indi['note'][nt],
                    "user_note": indi['note'][nt],
                    "duration": 1,}
                model.pop_save_individual(trait)

        # call fitness on first individual
        raise web.seeother('/fitness/0')

class Fitness:
    """This is an interactive fitness function, i.e. the individual is scored
    by the user. The user is shown a melody and is allowed to make X modifications 
    to it (e.g. re-order up to X traits). The euclidean dsitance is taken for the original melody
    and the user-modified melody. Ideally, we want a fitness score of 0 because that
    means the user liked what the computer presented."""

    def GET(self, indi_id):
        individual = model.pop_find_individual(int(indi_id))
        # converts from unicode to dictionary
        fake_individual = []
        artist = ''
        song = ''
        current_gen = ''

        note_colors = {
            'A': 'red',
            'B': 'yellow',
            'C': 'orange',
            'D': 'green',
            'E': 'blue',
            'F': 'purple',
            'G': 'grey',}

        for i in individual:
            current_gen = i['generation']
            if i['note'][0] in note_colors.keys():
                if '-' in i['note']:
                    i['note'] = i['note'].replace('-', 'b')
                color = note_colors[i['note'][0]]                
                fake_individual.append([i['note'],color])
            artist = i['artist']
            song = i['song']
        
        # song_name = indi_id+"_song.mid" # don't cast indi_id to int because cant concat int and string
        max_gen = int(model.params_max_gen()['max_gen'])
        
        return render.fitness(title, indi_id, fake_individual, artist, song, max_gen, current_gen)
    
    def POST(self, indi_id):
        """
        @TODO get all traits for the individual by gathering all the notes
        and user-notes for the individual and storing in two lists. compute
        the euclidean distance between the two lists and set as fitness score
        for the individual

        @TODO oracle to decide what to do next
        """        

        #model.pop_update_indi_fitness(int(indi_id), score)
        # query the individual and extract note and user-note
        individual = model.pop_find_individual(int(indi_id))
        user_list = []
        original_list = []

        # so ugly -- fix later
        for trait in individual:
            user_list.append(str(trait['user_note']))
            original_list.append(str(trait['note']))

        score = GA().euclidean_distance(original_list, user_list)
        print 'Fitness score :: ', score
        #update fitness score for individual
        model.pop_update_indi_fitness(int(indi_id), score)        
        GA().fate(int(indi_id))

class SaveFitness:
    def POST(self, indi_id):
        """Updates the user-note in a single trait in an individual. This is information
        is used to find out what notes the user didn't like from the computer
        presented melody"""
        t_id = web.input()['trait_id']
        _note = web.input()['name'].replace('b', '-')
        saved_traits = model.pop_find_trait(int(indi_id), int(t_id))
        model.pop_update_user_trait(saved_traits, {"$set": {"user_note":_note}})
        # GA().convert_midi(GA().create_pheno(int(indi_id)),int(indi_id))


class Terminate:
    def GET(self):
        """Render the terminate view and present the user with a list of save options"""
        GA().convert_midi(GA().create_pheno(0),0)
        return 'game over...'

    def POST(self):
        pass

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run()


