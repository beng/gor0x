import model
import random
import web
import json

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele

# def evolve_callback(ga_engine):
#     generation = ga_engine.getCurrentGeneration()
#     pop = ga_engine.getPopulation()
#     for i in pop:
#         print '--------------'
#         print i
#     #return 'leaving ga engine'

# def evolve_callback(ga_engine):
#     generation = ga_engine.getCurrentGeneration()
#     if generation == 0:
#         pop = ga_engine.getPopulation()
#         newPop=[]
#         for i in model.pop_find_all():
#             mnew = GAllele.GAlleleList([i['note']])
#             #setOfAlleles.add(a)
#         # CHANGE THE ENTIRE POPULATION "pop"
#         newPop.evaluate()
#         newPop.sort()
#     return False

def evolve_callback(ga_engine):
    generation = ga_engine.getCurrentGeneration()
    pop = ga_engine.getPopulation()
    print pop

def eval_func(chromosome):
    return random.randint(0,100)

########################################################
# NEW INITIALIZATION FUNCTION
########################################################
def init(genome, **args):
    """Creates the population for pyevolve"""
    a = []
    for i in model.pop_find_all():
        a.append(i['note'])
    genome.genomeList = a
    random.shuffle(genome.genomeList)

def init_ga(population_info):
    """Call the REST server to spawn an initial
    population based on the parameters in population_info

    population_info is a dictionary containing """

    # parameters for calling the server
    root = 'http://localhost:8000/spawn_pop/'
    params = [population_info['artist'], population_info['song'], population_info['num_indi'], population_info['num_traits'], population_info['size'], population_info['nodes']]
    params = root +'/'.join(params)
    print params
    br = web.Browser()
    br.open(params)
    traits = json.loads(br.get_text())

    # add content to population collection
    for trait in traits:
        model.pop_save_individual(trait)

    # do shit for pyevolve
    genome = G1DList.G1DList(int(population_info['num_indi']))

    genome.initializator.set(init)
    genome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(int(population_info['num_gen']))
    ga.setPopulationSize(int(population_info['num_indi']))

    # stepback callback
    ga.stepCallback.set(evolve_callback)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=10)

    # Best individual
    print ga.bestIndividual()

########################################################
# ORIGINAL INITIALIZATION FUNCTION!!!
########################################################
# def init_ga(num_indi):
#     """Shit is acting funky right now. I'm doing something stupid.
#     The problem might be with using the GAllele structure. I'll
#     experiment with this later once I get the real fitness function
#     in place."""

#     #setOfAlleles = GAllele.GAlleles()
#     num_indi = int(num_indi)

#     # list of traits per indi
#     #tl = [[t['note']] for t in model.pop_find_all()]
#     genome = G1DList.G1DList(num_indi)

#     # for i in model.pop_find_all():
#     #     a = GAllele.GAlleleList([i['note']])
#     #     setOfAlleles.add(a)

#     #genome = G1DList.G1DList(num_indi)
#     #genome.setParams(allele=setOfAlleles)
#     genome.initializator.set(init)
#     genome.evaluator.set(eval_func)
#     #genome.mutator.set(Mutators.G1DListMutatorAllele)
#     #genome.initializator.set(Initializators.G1DListInitializatorAllele)
    

#     # Genetic Algorithm Instance
#     ga = GSimpleGA.GSimpleGA(genome)
#     ga.selector.set(Selectors.GRouletteWheel)
#     ga.setGenerations(20)
#     ga.setPopulationSize(num_indi)

#     # stepback callback
#     ga.stepCallback.set(evolve_callback)

#     # Do the evolution, with stats dump
#     # frequency of 10 generations
#     ga.evolve(freq_stats=1)

#     # Best individual
#     print ga.bestIndividual()