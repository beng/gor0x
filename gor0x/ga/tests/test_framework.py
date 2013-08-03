"""
population = defaultdict(list)
for (current generation) in (total generations)
    population [current_generation].append((generate population)(number of individuals))
    children = crossover(select(fitness(population)))
    population[current_generation+1].append(children)
"""

from collections import defaultdict
from functools import partial
import random
import math

from context import ga


def random_genotype():
    return [random.uniform(-5,5),random.uniform(-5,5)]


def test_population(num_individuals=10):
    population = []
    for individual in range(num_individuals):
        population.append({
            'id': individual,
            'genotype': random_genotype(),
        })
    return population


def fitness(individual):
    return map(partial(math.pow, 2), individual.genotype)


def run(max_generations=5):
    world = ga.GA(test_population())
    population = defaultdict(list)
    for current_generation in range(max_generations):
        population[current_generation].append(world.population)

        # wait for input -- use coroutine to now switch to the server
        for individual in world.population:
            # print "individual fitness pre: {}".format(individual.fitness)
            individual.fitness = fitness(individual)
            # print "individual fitness post: {}".format(individual.fitness)
        # resume processing

        winners = world.selection.tournament()
        # print winners[0].genotype
        # print "-----------"
        mom, dad = random.sample(winners, 2)
        # hm, how do i do this? how many times do we want to crossover in a round?
        """THIS ISNT WORKING CORRECTLY! NEED TO CREATE NEW INDIVIUDAL OBJECTS
        FROM WHEN WE CROSSOVER!!!!"""
        brother, sister = world.crossover.single(mom.pop, dad.pop)
        mutated = random.choice([brother, sister])
        # world.mutation(mutated).mutate(mutated, default=.3)
        population[current_generation + 1].append([brother, sister])
        print "BEST :: ", world.statistics.best.id, world.statistics.best.fitness, world.statistics.best.genotype
        print "-----------------"
        print "WORST :: ", world.statistics.worst.id, world.statistics.worst.fitness, world.statistics.worst.genotype
    return population

run()

