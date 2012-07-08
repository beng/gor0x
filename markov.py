"""
create a markov chain based off the user selected artist(s)
   
SMALL PORTION OF CODE TAKEN FROM 
        http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
"""
import random 

"""
THIS WILL THROW AN ERROR IF THE NUMBER OF SONGS IN THE FILE IS < SPECIFIED VALUE
"""
_number_of_songs = 2    # how many songs to go through in the entire file, -1 = random amount

class markov(object):
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.pitches = self.file_to_pitches()
        self.pitches_size = len(self.pitches)
        self.pitch_set = []
        self.database()
        
    def file_to_pitches(self):
        self.open_file.seek(0)
        #data = self.open_file.read()
        data = {}
        data[0] = self.open_file.readline()
        i = 0
        while len(data[i]) != 0:
            i += 1
            data[i] = self.open_file.readline()
        
        if _number_of_songs == -1:
            number_of_songs = random.randint(0, i - 1)
        else:
            number_of_songs = _number_of_songs
        ret_data = []
        n = []
        while number_of_songs > 0:
            n.append(random.choice(range(0, i - 1)))
            for p in data[n[-1]].split():
                ret_data.append(p)
            number_of_songs -= 1
        return ret_data
        
    def triples(self):
        if len(self.pitches) < 3:
            return
    
        for i in range(len(self.pitches) - 2):
            yield (self.pitches[i], self.pitches[i + 1], self.pitches[i + 2])
            
    def database(self):
        for p1, p2, p3 in self.triples():
            if p1 not in self.pitch_set:
                self.pitch_set.append(p1)
            if p2 not in self.pitch_set:
                self.pitch_set.append(p2)
            if p3 not in self.pitch_set:
                self.pitch_set.append(p3)
            key = (p1, p2)
            if key in self.cache:
                self.cache[key].append(p3)
            else:
                self.cache[key] = [p3]
                
    def get_next_pitch(self, p1, p2):
        return random.choice(self.cache[(p1, p2)])
    
    def get_next_pitches(self, p1, p2, size=500):
        n = len(self.cache)
        while ((p1, p2) not in self.cache) and n > 0:
            p2 = random.choice(self.pitch_set)
            n -= 1
        if n == 0:
            (p1, p2) = random.choice(self.cache.keys())
            
        gen_pitches = []
        for i in xrange(size):
            gen_pitches.append(p1)
            p1, p2 = p2, random.choice(self.cache[(p1, p2)])
        gen_pitches.append(p2)
        return gen_pitches
                
    def generate_music(self, size=500):
        seed = random.randint(0, self.pitches_size - 3)
        seed_pitch, next_pitch = self.pitches[seed], self.pitches[seed + 1]
        p1, p2 = seed_pitch, next_pitch
        gen_pitches = []
        for i in xrange(size):
            gen_pitches.append(p1)
            n = len(self.cache)
            while ((p1, p2) not in self.cache) and n > 0:
                p2 = random.choice(self.pitch_set)
                n -= 1
            if n == 0:
                (p1, p2) = random.choice(self.cache.keys())
            p1, p2 = p2, random.choice(self.cache[(p1, p2)])
        gen_pitches.append(p2)
        return gen_pitches