import random

def mate(p1, p2, num_traits):
    # single point crossover
    split = random.randint(0,num_traits-1) 
    return p1[:split] + p2[split:], p2[:split] + p1[split:]