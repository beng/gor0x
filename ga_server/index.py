import web
import json
import ast
import model
import random
import ga
import math
import music21

urls = (
        '/', 'Index',
        '/fitness/(.+)', 'Fitness',
        '/save_fitness/(.+)', 'SaveFitness',
        '/terminate', 'Terminate',)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())
title = 'GA Server'

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

        max_gen = model.params_max_gen()['max_gen']        
        current_generation = model.pop_current_generation(indi_id)['generation']
        max_indi = model.pop_max_indi(current_generation)[0]['indi_id']    

        if indi_id == max_indi:
            # termination requirements met?
            if current_generation == max_gen:
                raise web.seeother('/terminate')
            else:
                # current generation over, start mating!
                self.select(current_generation)
        elif indi_id < max_indi:
            raise web.seeother('/fitness/'+str(indi_id+1))
        else:
            raise web.seeother('/terminate')

    def select(self, current_generation):
        """Selection phase -- right now I've only implemented tournament
        selection. Use current_generation to grab all individuals of 
        previous generation"""

        num_rounds = 2
        k = 2
        winner = []
        population = model.pop_population_by_generation(current_generation)

        # get list of winning individuals
        for i in range(num_rounds):
            winner.append(self.tournament(k,population))
        
        for i in range(len(population)):
            # select random winners to be parent
            p1 = random.choice(winner)            
            p2 = random.choice(winner)
            #print "PARENT 1", p1
            #print "PARENT2 ", p2
            _p1 = []
            _p2 = []
            artist = ''
            song = ''
            # find each parents traits
            for i in model.pop_find_individual(int(p1['indi_id'])):
                for k,v in i.items():
                    if k == 'artist':
                        artist = v
                    if k == 'song':
                        song = v
                    if k == 'note':
                        _p1.append(v)

            for i in model.pop_find_individual(int(p2['indi_id'])):
                for k,v in i.items():
                    if k == 'note':
                        _p2.append(v)
            # create child among parents
            child = self.crossover(_p1,_p2)
            
            # save child
            max_indi = model.pop_max_indi(current_generation)[0]['indi_id']
            t_id = 0
            for i in child:
                information = {
                    "artist": artist,
                    "song": song,
                    "indi_id": int(max_indi)+1, 
                    "trait_id":t_id, 
                    "generation": int(current_generation)+1,
                    "fitness": 0,
                    "note": i,
                    "user_note": note,
                    "duration": 1,}
                t_id += 1
                print "information :: ", information
                model.pop_save_individual(information)

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

        try:
            split = random.randint(0, len(parent1))
            print "split ", split
            print "parents1 ", parent1
            print "parent2 ", parent2
            return parent1[:split] + parent2[split:]#, parent2[:split] + parent1[split:]
        except ValueError:
            raise "Parents aren't the same length!"

class Index:
    def GET(self):
        """Render the parameter initialization view"""
        model.pop_clear_conn()
        model.params_clear_conn()
        model.params_save({"max_gen":1})
        num_indi = 3
        num_traits = 5
        size = 2000
        nodes = 5
        population = GA().create_population('Vivaldi', 'winter_allegro', num_indi,num_traits,size,nodes)
        
        for indi in population:
            for nt in range(num_traits):
                trait = {
                    "artist": indi['artist'],
                    "song": indi['song'],
                    "indi_id": indi['indi_id'],
                    "trait_id": nt,
                    "generation": indi['generation'],
                    "fitness": 0,
                    "note": indi['note'][nt],
                    "user_note": indi['note'][nt],
                    "duration": 1,}
                print 'trait :', trait
                model.pop_save_individual(trait)
            
            #model.pop_save_individual(indi)
        
        
        # notes = ['A','B','C','D','E','F','G']
        # for ps in range(pop_size):
        #     for nt in range(num_traits):
        #         chromosome = GA().create_indi(ps, nt, 0, 0, random.choice(notes), 1)
        #         model.pop_save_individual(chromosome)
        # raise web.seeother('/fitness/0')

    def POST(self):
        pass

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

        for i in individual:
            fake_individual.append(i['note'])

        #print fake_individual
        return render.fitness(title, indi_id, fake_individual)
    
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
            for k,v in trait.items():
                if k == 'user_note':
                    user_list.append(str(v))
                if k == 'note':
                    original_list.append(str(v))

        score = GA().euclidean_distance(original_list, user_list)

        #update fitness score for individual
        model.pop_update_indi_fitness(int(indi_id), score)
        GA().fate(int(indi_id))

class SaveFitness:
    def POST(self, indi_id):
        """Updates the user-note in a single trait in an individual. This is information
        is used to find out what notes the user didn't like from the computer
        presented melody"""
        t_id = web.input()['trait_id']
        _note = web.input()['name']
        saved_traits = model.pop_find_trait(int(indi_id), int(t_id))
        model.pop_update_trait(saved_traits, {"$set": {"user_note":_note}})

class Terminate:
    def GET(self):
        """Render the terminate view and present the user with a list of save options"""
        return 'game over...'

    def POST(self):
        pass

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run()


