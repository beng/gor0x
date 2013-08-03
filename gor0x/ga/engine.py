class GAEngine(object):
    def __init__(self, pop_size=10, num_gen=1, artist=None, song_name=None, mutation=.3):
        self.pop_size = pop_size
        self.num_gen = num_gen
        self.cache = Cache(prefix="generation")
        self.artist = artist
        self.song_name = song_name
        self.mutation = mutation
        self.song = Song(artist=self.artist, song=self.song_name)

    def _run(self):
        for generation in range(self.num_gen):
            if generation == 0:
                self.song._load_corpus()
                ga = GA(self.song.corpus)
            else:
                ga = GA(self.cache.hgetall(generation))

            for individual in ga.population:
                individual.fitness = randint(0, 100)

            winners = ga.selection.tournament()

            for rounds in range(len(winners)):
                mom, dad = choice(winners), choice(winners)
                print mom, dad
                print mom.dna
                brother, sister = mom.crossover.single(dad)
                print brother, sister

                brother.mutation.mutate(default=self.mutation)
                self.cache.hset(generation, brother.id, brother.dna)

                sister.mutation.mutate(default=self.mutation)
                self.cache.hset(generation, sister.id, sister.dna)
