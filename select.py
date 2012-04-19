import tournament

def helper(k, population, num_rounds):
    # run tournament selection on requested population
    return [tournament.extract(k,population) for i in range(num_rounds)]
        