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
        max_gen = model.params_max_gen()['max_gen']        
        current_gen = model.pop_current_generation(indi_id)['generation']

        # returns a cursor even though i set the limit
        # figure out why...
        max_indi = model.pop_max_indi(current_gen)[0]['indi_id']    

        print 'MG ', max_gen
        print 'CG ',current_gen
        print 'current indi ', indi_id
        print 'max indi', max_indi

        if indi_id == max_indi:
            print 'last indi of pop!'
            # termination requirements met?
            if current_gen == max_gen:
                print 'peace! shits over!'
                raise web.seeother('/terminate')
            else:
                print 'go to select!'
                pop_size = 5
                num_traits = 2
                notes = ['A','B','C','D','E','F','G']
                for ps in range(indi_id+1,pop_size+indi_id+1):
                    for nt in range(num_traits):
                        chromosome = GA().create_indi(ps, nt, current_gen+1, 0, random.choice(notes), 1)
                        model.pop_save_individual(chromosome)
                raise web.seeother('/fitness/'+str(indi_id+1))
        elif indi_id < max_indi:
            print 'still more to go!'
            raise web.seeother('/fitness/'+str(indi_id+1))
        else:
            raise web.seeother('/terminate')
        #raise web.seeother('/fitness/' + str(indi_id+1))


class Index:
    def GET(self):
        model.pop_clear_conn()
        model.params_clear_conn()

        model.params_save({"max_gen":0})
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


