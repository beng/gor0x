import web
import json
import model
import ga

urls = (
        '/', 'Index',
        '/fitness/(.+)', 'Fitness',
        '/save_fitness/(.+)', 'SaveFitness',
        '/terminate', 'Terminate',)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())
title = 'GA Server'

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

        population = ga.create_population(artist, song, num_indi, num_traits, size, nodes)
        
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

        score = ga.euclidean_distance(original_list, user_list)
        print 'Fitness score :: ', score
        #update fitness score for individual
        model.pop_update_indi_fitness(int(indi_id), score)        
        ga.fate(int(indi_id))

class SaveFitness:
    def POST(self, indi_id):
        """Updates the user-note in a single trait in an individual. This is information
        is used to find out what notes the user didn't like from the computer
        presented melody"""
        t_id = web.input()['trait_id']
        _note = web.input()['name'].replace('b', '-')
        saved_traits = model.pop_find_trait(int(indi_id), int(t_id))
        model.pop_update_user_trait(saved_traits, {"$set": {"user_note":_note}})
        # ga.convert_midi(ga.create_pheno(int(indi_id)),int(indi_id))


class Terminate:
    def GET(self):
        """Render the terminate view and present the user with a list of save options"""
        ga.convert_midi(ga.create_pheno(0),0)
        return 'game over...'

    def POST(self):
        pass

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run()


