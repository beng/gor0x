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

    def mutation(self):
        return Mutation(self)

    @property
    def statistics(self):
        return Statistics(self.population)

    @property
    def population(self):
        return map(Individual, self.pop)


class Individual(GA):
    @property
    def id(self):
        return self.pop['id']

    @property
    def fitness(self):
        return self.pop['fitness']

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
    def mutate(self, default=.3):
        rate = uniform(0, 1)

        if default > rate:
            return self.pop

        split = randint(1, len(self.pop.dna) - 1)
        start, stop = random_sampling(0, len(self.pop.dna), split)
        self.pop.dna[start:stop] = 'Z'  # replace with newly generated corpus

        return self.pop


class Selection(GA):
    def roulette(self):
        pass

    def tournament(self, k=3):
        """
        1. a random subset of size, k, from the given generation is extracted
        2. sort the pool by fitness value
        3. return the individuals with the highest fitness value
        """
        subset = [choice(self.pop) for indi in range(k)]

        return sorted(subset, key=lambda x: x.fitness, reverse=True)


class Crossover(GA):
    def single(self, other):
        split = randint(1, len(self.pop.dna))
        p1, p2 = self.pop.dna, other.dna

        return p1[:split] + p2[split:], p2[:split] + p1[split:]

    def two_point(self, other):
        return self, other
