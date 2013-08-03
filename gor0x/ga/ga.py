from random import choice, randint, randrange, uniform

from music21 import stream


def random_sampling(low, high, nt):
    """Return a starting index and a stopping index for a random
    consecutive sampling from a population"""
    start_idx = randrange(low, high)
    stop_idx = start_idx + nt

    if stop_idx > high:
        return random_sampling(low, high, nt)
    return start_idx, stop_idx


class GA(object):
    def __init__(self, pop, *args, **kwargs):
        self.pop = pop

    @property
    def crossover(self):
        return Crossover(self)

    @property
    def selection(self):
        return Selection(self.population)

    def mutation(self, individual):
        return Mutation(individual)

    @property
    def statistics(self):
        return Statistics(self.population)

    @property
    def population(self):
        return map(Individual, self.pop)


class Individual(GA):
    def __init__(self, pop, *args, **kwargs):
        super(Individual, self).__init__(pop, *args, **kwargs)
        self._fitness = 0

    @property
    def id(self):
        return self.pop['id']

    @property
    def fitness(self):
        return self._fitness
        # return self.pop['fitness']

    @fitness.setter
    def fitness(self, score):
        self._fitness = score

    @property
    def genotype(self):
        return self.pop['genotype']

    @property
    def phenotype(self):
        upper = stream.Part()
        measure = stream.Measure()

        for trait in self.genotype:
            measure.append(trait)

        upper.append(measure)
        return upper


class Statistics(GA):
    @property
    def worst(self):
        """Return the worst individual in the population"""
        return sorted(self.pop, key=lambda x: x.fitness)[0]

    @property
    def best(self):
        """Return the best individual in the population"""
        return sorted(self.pop, key=lambda x: x.fitness, reverse=True)[0]


class Mutation(GA):
    def mutate(self, individual, traits=None, default=.3):
        rate = uniform(0, 1)

        if default > rate:
            # return self.population
            return

        split = randint(1, len(individual.genotype) - 1)
        start, stop = random_sampling(0, len(individual.genotype), split)
        individual.genotype[start:stop] = traits
        # return self.population


class Selection(GA):
    def roulette(self):
        pass

    def tournament(self, k=3):
        """
        1. a random subset of size, k, from the given generation is extracted
        2. sort the pool by fitness value
        3. return the individuals with the highest fitness value
        """
        # 7/22 switched to self.population for testing
        # subset = [choice(self.pop) for indi in range(k)]
        subset = [choice(self.population) for indi in range(k)]
        return sorted(subset, key=lambda x: x.fitness, reverse=True)


class Crossover(GA):
    def single(self, p1, p2):
        split = randint(1., len(p1.genotype))
        bg, sg = p1.genotype[:split] + p2.genotype[split:], p2.genotype[:split] + p1.genotype[split:]
        bg = Individual({'id': len(self.pop.pop), 'genotype': bg})
        sg = Individual({'id': bg.id+1, 'genotype': sg})
        return bg, sg

    def two_point(self, other):
        return self, other
