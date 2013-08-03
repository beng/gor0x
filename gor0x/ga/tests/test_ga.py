import unittest
from random import randint

from context import ga, chromosome, markov


class TestGA(unittest.TestCase):
    def setUp(self):
        directory = "../gor0x/assets/midi"
        artist = "vivaldi"
        title = "winter_allegro"
        self.midiobj = chromosome.MidiObject(
            artist=artist, title=title, directory=directory)

    def test_songobj(self):
        self.midiobj.corpus = self.midiobj.from_midi()
        population = []
        for x in range(5):
            start, stop = ga.random_sampling(0, len(self.midiobj.corpus), 5)
            population.append({
                'id': x,
                'fitness': randint(0, 100),
                'genotype': self.midiobj.corpus[start:stop]
            })

        _ga = ga.GA(population)
        print _ga.population
        print '\n\n'

        for indi in _ga.population:
            print indi.id, indi.fitness, indi.genotype
        # for indi in _ga.population:
        #     print indi.genotype

        print "STATS ----------"
        print _ga.statistics.best.id, _ga.statistics.worst.id

        initial_population = markov.generate(self.midiobj.corpus)
        print initial_population

        """
        @TODO figure out how to map the markov output to an individual
            -map the character in the markov output to the Note/Rest class name property
        """

if __name__ == '__main__':
    unittest.main()
