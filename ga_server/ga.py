import model
import web
import json
import math
import music21
import random

USER_SETTINGS = {'size': 0, 'nodes': 0, 'rate': 0.0, 'artist': '', 'song': ''}

def create_population(artist, song, num_indi, num_traits, size, nodes, mrate):
    USER_SETTINGS['mc_size'] = int(size)
    USER_SETTINGS['mc_nodes'] = int(nodes)
    USER_SETTINGS['rate'] = float(mrate)

    root = 'http://localhost:8000/q/spawn_pop/'
    params = root +'/'.join([artist, song, str(num_indi), str(num_traits), str(size), str(nodes)])
    br = web.Browser()
    br.open(params)

    population = json.loads(br.get_text())
    
    return population

# def euclidean_distance(song1, song2):
#     """The songs are lists of notes converted to their midi value
#     @TODO clean this up. it's too messy"""
#     try:
#         score = 0
#         for i in range(len(song1)):
#             score += math.sqrt((music21.pitch.Pitch(song1[i]).midi - int(music21.pitch.Pitch(song2[i]).midi)) ** 2)
#         return score
#     except ValueError:
#         raise 'Songs must be the same length!'

def fate(indi_id):
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
            select(current_generation, indi_id)
    elif indi_id <= max_indi:
        raise web.seeother('/fitness/'+str(indi_id+1))
    else:
        raise web.seeother('/terminate')

def select(current_generation, current_indi_id):
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
    num_rounds = int(model.params_num_indi()['num_indi'])
    k = 2
    winner = []
    population = model.pop_population_by_generation(current_generation)

    # get list of winning individuals
    for i in range(num_rounds):
        winner.append(tournament(k,population))
    
    max_indi = int(model.pop_max_indi(current_generation)[0]['indi_id'])

    for i in range(model.params_num_indi()['num_indi']):
    # for i in range(num_rounds):
        # select random winners to be parent
        p1 = random.choice(winner)            
        p2 = random.choice(winner)
        _p1 = []
        _p2 = []
        # artist = ''
        # song = ''

        # find each parents traits
        for item in model.pop_find_individual(int(p1['indi_id'])):
            USER_SETTINGS['artist'] = item['artist']
            USER_SETTINGS['song'] = item['song']
            _p1.append(item['user_note'])

        for item in model.pop_find_individual(int(p2['indi_id'])):
            _p2.append(item['user_note'])

        # create child among parents
        child1, child2 = crossover(_p1,_p2)
        print 'p1 : ', p1
        print 'p2 : ', p2
        print "child 1 : ", child1
        print "child 2 : ", child2
        # perform mutation
        child1 = mutate(child1)
        child2 = mutate(child2)

        # save child
        t_id = 0
        # clean the fuck up
        for i in child1:
            # i = mutate(i)
            print "max indi loop c1 ", max_indi+1
            information = {
                "artist": USER_SETTINGS['artist'],
                "song": USER_SETTINGS['song'],
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
            # i = mutate(i)
            print "max indi loop c2", max_indi+2
            information = {
                "artist": USER_SETTINGS['artist'],
                "song": USER_SETTINGS['song'],
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
# def mutate(individual):
#     """
#     if mutation rate > random float
#         mutate random subset of individual
#     """
#     # random float
#     rnd_rate = random.uniform(0,1)
#     if rnd_rate < USER_SETTINGS['rate']:
#         print 'PERFORMING MUTATION!!!!!'

#         # generate new corpus using the same influencer
#         br = web.Browser()
#         uri = '/'.join(str(v) for v in [USER_SETTINGS['artist'], USER_SETTINGS['song'], 1, 1, USER_SETTINGS['mc_size'], USER_SETTINGS['mc_nodes']])
#         br.open('http://localhost:8000/q/spawn_pop/'+uri)

#         # replace old notes with notes from new corpus
#         new_corpus = json.loads(br.get_text())[0]['note']
#         return random.choice(new_corpus)
#     else:
#         return individual

def mutate(individual):
    """
    if mutation rate > random float
        mutate random subset of individual
    """
    # USER_SETTINGS['mc_size'] = 2000
    # USER_SETTINGS['mc_nodes'] = 4
    # USER_SETTINGS['rate'] = .01
    # USER_SETTINGS['artist'] = 'Biggie'
    # USER_SETTINGS['song'] = 'top100_Big_Poppa'

    # random float
    print 'MUTATE INDIVIDUAL : ', individual
    rnd_rate = random.uniform(0,1)
    if rnd_rate < USER_SETTINGS['rate']:
        print 'PERFORMING MUTATION!!!!!'

        # starting point for random subset
        split_point = random.randint(1,len(individual)-1)

        # size of subset
        # num_traits_to_replace = random.randrange(split_point, len(individual)-1)
        
        # starting and stopping points
        start,stop = random_sampling(0, len(individual), split_point)

        # generate new corpus using the same influencer
        br = web.Browser()
        uri = '/'.join(str(v) for v in [USER_SETTINGS['artist'], USER_SETTINGS['song'], 1, split_point, USER_SETTINGS['mc_size'], USER_SETTINGS['mc_nodes']])
        br.open('http://localhost:8000/q/spawn_pop/'+uri)

        # replace old notes with notes from new corpus
        new_corpus = json.loads(br.get_text())[0]['note']
        # new_corpus = [s.encode('utf-8') for s in new_corpus]
        print 'pre indi:', individual
        individual[start:stop] = new_corpus[start:stop]
        print 'post indi:', individual
        return individual
    else:
        return individual

def random_sampling(min, max, nt):
    """Return a starting index and a stopping index for a random
    consecutive sampling from a population"""

    start_idx = random.randrange(min, max)
    stop_idx = start_idx + nt

    if stop_idx > max:
        return random_sampling(min, max, nt)
    return start_idx, stop_idx

def tournament(k, population):
    """Tournament Selection

    k = subset size

    1. a random subset of size, k, from the given generation is extracted 
    2. sort the pool by fitness value
    3. return the winner, the individual with the highest fitness value"""

    # find k best individuals in population
    pool = []
    for i in range(k):
        while True:
            individual = random.choice(population)
            print "INDIVIDUAL ", individual
            if individual not in pool:
                pool.append(individual)
                break

    # select individual with the highest fitness score
    winner = sorted(pool, key=lambda x: -x['fitness'])[0]

    return winner

def crossover(parent1, parent2):
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

def create_pheno(indi_id):
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

def convert_midi(mfile, indi_id):
    '''
    mfile is a musicstream which is exported to as midi format
    '''
    mf = mfile.midiFile
    name = str(indi_id) + '_song.mid'
    mf.open('static/' + name, 'wb')
    mf.write()
    mf.close()
    return name