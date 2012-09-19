# import random
# import operator

# population = {
#     1: {
#         "generation": 0,
#         "dna": {
#             "note": ['A4','B4','C4'],
#             "duration": 1
#         },
#         "fitness": 50

#     },
#     2: {
#         "generation": 0,
#         "dna": {
#             "rest": [],
#             "duration": 1
#         },        
#         "fitness": 30

#     },
#     3: {
#         "generation": 0,
#         "dna": {
#             "rest": ['E4', 'F4', 'G4'],
#             "duration": 1
#         },        
#         "fitness": 100

#     }
# }

# def fitness(individual):
#     # webpy can render individual on the webpage even though its a dict, have js parse for what it needs
#     return random.randint(0,100)

# def selection(population, n):
#     # select the best n individuals from the population

    
#     sort_id = []

#     for k,v in population.items():
#         if "fitness" in v:
#             sort_id.append([k,v])
    
#     # sort sort_id by highest fitness
#     #for k,v in 


# #print selection(population, 5)
# # for v in population.values():
# #     print v['generation']
# #     print fitness(v)
# #     print '--'