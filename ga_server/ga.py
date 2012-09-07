import model
import random

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele

def eval_func(chromosome):
	return random.randint(0,100)

def init_ga(num_traits):
	"""Shit is acting funky right now. I'm doing something stupid.
	The problem might be with using the GAllele structure. I'll
	experiment with this later once I get the real fitness function
	in place."""

	setOfAlleles = GAllele.GAlleles()
	num_traits = int(num_traits)

	for i in model.pop_find_all():
		a = GAllele.GAlleleList(i['note'])
		setOfAlleles.add(a)

	genome = G1DList.G1DList(num_traits)

	genome.setParams(allele=setOfAlleles)
	genome.evaluator.set(eval_func)
	genome.mutator.set(Mutators.G1DListMutatorAllele)
	genome.initializator.set(Initializators.G1DListInitializatorAllele)

	# Genetic Algorithm Instance
	ga = GSimpleGA.GSimpleGA(genome)
	ga.selector.set(Selectors.GRouletteWheel)
	ga.setGenerations(20)

	# Do the evolution, with stats dump
	# frequency of 10 generations
	ga.evolve(freq_stats=1)

	# Best individual
	print ga.bestIndividual()