import sys

"""
initial population
    -supply either artist name or 2 songs 
    -select subset of pitches from each song OR if artist supplied, take 2 random subsets of pitch file of length num_traits
        -EXPERIMENT WITH -- when getting pitches, do i want to select a subset of same pitches (e.g. [C# C# C# C# C#] or do i want diversity?) 
    -take euclidean distance between 2 subsets -- this becomes the fitness comparator
    -build markov model with the traits selected above

fitness
    -sum([euclidean distance individual and parent_1], [euclidean distance between individual and parent_2]    
    -winners of round =  30%similar, 30%X middle, and 60% different children depending on desired number of children.       this will be useful to ensure that the population doesnt converge 
    -use case:
        the 2 songs supplied on the cmd line are "billy joel - we didnt start the fire" and "jay-z - hard knock life". 
        take the euclidean distance between those 2 songs and use that to compare against the SUM of the euclidean distance between the child and billy joel, and the euclidean distance between the child and jay-z.       
"""


def run():
	pass

def main(args):
    try:
    	run()
        # implement opts, args = getopt.getopt to allow flags and args
        # e.g. python music.py -a <artist> -s1 <song_1> -s2 <song_2>
    except ValueError:
		pass
    
if __name__ == '__main__':	
	main(sys.argv[1:])