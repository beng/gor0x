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
MAX_GEN = 5

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
        # is the indi the last in the generation?
        current_generation = model.pop_current_generation(int(indi_id))['generation']
        print "CURRENT GENERATION = ", current_generation
        #max_indi = model.pop_max_indi(current_generation)
        max_indi = model.pop_max_indi(current_generation)[0]['indi_id']
        print "current indid == ", indi_id
        print "max indi == ", max_indi
        if indi_id == max_indi:
            if current_generation >= MAX_GEN:
                print 'cg >= mg'
                raise web.seeother('/terminate')
            else:
                # select best individuals
                print 'in raise indi'
                raise web.seeother('/fitness/' + str(indi_id + 1))
        elif indi_id <= max_indi:
            raise web.seeother('/fitness/' + str(indi_id + 1))
        else:
            raise web.seeother('/terminate')


class Index:
    def GET(self):
        model.pop_clear_conn()
        pop_size = 20
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
        user = [{'trait_id': 0, 'note': 'G'}, {'trait_id':1, 'note':'F'}]

        for u in user:
            user_tid = u['trait_id']
            saved_traits = model.pop_find_trait(int(indi_id), user_tid)
            model.pop_update_trait(saved_traits, {"$set": {"note":u['note']}})

        #raise web.seeother('/fitness/' + str(int(indi_id)+1))
        GA().fate(int(indi_id))

class Terminate:
    def GET(self):
        #model.print_info()
        return 'game over...'

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run()


