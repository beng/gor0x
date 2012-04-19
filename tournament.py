import random

def winner(popoulation):
    # sort population by fitness
    return sorted(pool, key=lambda x:-x[1])[0][0]

def extract(k, population):
    # take random subset of population of size k
    # return individual with highest fitness
    return winner([random.choice(population) for i in xrange(k)])