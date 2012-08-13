from markov import markov
import model
import random

class Spawn:
    def create_pool(self,**kargs):          
        if ('pop_size' and 'num_traits' and 'influencers') in kargs:
            # slightly messy -- need to clean up
            pitch = self.markov_pitch(**kargs)
            for pop in range(0,int(kargs['pop_size'])):
                for trait in range(0,int(kargs['num_traits'])):
                    print 'pitch :: ', pitch
                    print 'pitch :: ', pitch[trait]
                    params = dict(
                        indi_id=pop,
                        generation=0,
                        trait=pitch[trait],
                        duration='half',
                        fitness=0,)
                    model.insert('song',params)

    def markov_pitch(self,**kargs):
        if ('num_traits' and 'influencers') in kargs:
            m = markov(open('./static/pitches/pitches_' + kargs['influencers'] + '.txt'))
            return m.generate_music(int(kargs['num_traits']))