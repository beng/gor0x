import web
import json
import ast
import model
import random
import ga


urls = (
        '/', 'Index',
        '/fitness/(.+)', 'Fitness',
        '/terminate', 'Terminate',)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())
title = 'GA Server'

class GA:
    def create_indi(self,indi_id, trait_id, generation, fitness, note, duration):
        indi = {
            "indi_id": indi_id,
            "trait_id": trait_id,
            "generation": generation,
            "fitness": fitness,
            "note": note,
            "duration": duration,
        }
        return indi

    def fate(self,indi_id):
        """Use the individual that was just evaluated to determine
        where we are in the grand scheme of things. How many more individuals
        of the current generation need to be evaluated? Are the termination
        requirements met? Are we ready to move to the next generation? Etc..."""

        max_gen = model.params_max_gen()['max_gen']        
        current_generation = model.pop_current_generation(indi_id)['generation']
        max_indi = model.pop_max_indi(current_generation)[0]['indi_id']    

        if indi_id == max_indi:
            print 'last indi of pop!'
            # termination requirements met?
            if current_generation == max_gen:
                print 'peace! shits over!'
                raise web.seeother('/terminate')
            else:
                # current generation over, start mating!
                print 'go to select!'
                self.select(current_generation)
        elif indi_id < max_indi:
            print 'still more to go!'
            raise web.seeother('/fitness/'+str(indi_id+1))
        else:
            raise web.seeother('/terminate')

    def select(self, current_generation):
        """Use current_generation to grab all individuals of previous generation"""
        num_rounds = 2
        k = 2
        winner = []

        for i in range(num_rounds):
            winner.append(self.tournament(k,current_generation))

        
        child = self.crossover(random.choice(winner), random.choice(winner))

    def tournament(self, k, current_generation):
        """Tournament Selection

        k = subset size
    
        1. a random subset of size, k, from the given generation is extracted 
        2. sort the pool by fitness value
        3. return the winner, the individual with the highest fitness value"""

        # find k best individuals in population
        population = model.pop_population_by_generation(current_generation)
        pool = []
        for i in range(k):
            individual = random.choice(population)
            if individual not in pool:
                pool.append(individual)

        # select individual with the highest fitness score
        winner = sorted(pool, key=lambda x: -x['fitness'])[0]
        return winner
    
    def crossover(self, parent1, parent2):
        """Do tomorrow..."""
        pass

class Index:
    def GET(self):
        model.pop_clear_conn()
        model.params_clear_conn()

        model.params_save({"max_gen":1})
        pop_size = 5
        num_traits = 2
        notes = ['A','B','C','D','E','F','G']
        for ps in range(pop_size):
            for nt in range(num_traits):
                chromosome = GA().create_indi(ps, nt, 0, 0, random.choice(notes), 1)
                model.pop_save_individual(chromosome)
                #print chromosome
        raise web.seeother('/fitness/0')

class Fitness:
    def GET(self, indi_id):
        score = random.randint(0,100)
        model.pop_update_indi_fitness(int(indi_id), score)
        GA().fate(int(indi_id))

        """
        THIS SHIT WORKS DO NOT DELETE WHAT IS BELOW!
        """
        # user = [{'trait_id': 0, 'note': 'G'}, {'trait_id':1, 'note':'F'}]

        # for u in user:
        #     user_tid = u['trait_id']
        #     saved_traits = model.pop_find_trait(int(indi_id), user_tid)
        #     model.pop_update_trait(saved_traits, {"$set": {"note":u['note']}})

        #raise web.seeother('/fitness/' + str(int(indi_id)+1))
        

class Terminate:
    def GET(self):
        #model.print_info()
        return 'game over...'

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run()


