"""
@author   Ben G
@email    beg5670@gmail.com
@website  http://github.com/beng
  
this is a genetic algorithm that composes melodies. 
"""

import web
import random

import model
import song_name

from markov import markov
from music21 import *

urls = (
    '/', 'Index',)

render = web.template.render('templates/', base='layout')
song_selection = list(song_name.parse_name('static/pitches/'))
title = "Melody Composer"

class Index:
    def GET(self):
        # clear tables 
        model.clear_tables()        
        songs = [song for song in song_selection]
        return render.index(title, songs)

    def POST(self):        
        params = web.input()
        model.insert('params', params)
        Spawn().create_pool(**params)

class Spawn:
    def create_pool(self,**kargs):        
        if ('pop_size' and 'num_traits' and 'influencers') in kargs:
            # slightly messy -- need to clean up
            pitch = self.markov_pitch(**kargs)
            for pop in range(0,int(kargs['pop_size'])):
                for trait in range(0,int(kargs['num_traits'])):
                    try:
                        params = dict(
                            indi_id=pop,
                            generation=model.get_max_gen()+1,
                            pitch=pitch[trait][0],
                            octave=pitch[trait][1],
                            modifier=pitch([trait][2]),
                            duration='half',
                            fitness=0,)
                        model.insert('song',params)
                    except IndexError:
                        params = dict(
                            indi_id=pop,
                            generation=model.get_max_gen()+1,
                            pitch=pitch[trait][0],
                            octave=pitch[trait][1],
                            modifier=random.choice('#',''],
                            duration='half',
                            fitness=0,)
                        model.insert('song',params)

                    #print pitch[trait][0]
                    #print pitch[trait][1]
            #model.insert('song', params)

    def markov_pitch(self,**kargs):
        if ('num_traits' and 'influencers') in kargs:
            m = markov(open('./static/pitches/pitches_' + kargs['influencers'] + '.txt'))
            return m.generate_music(int(kargs['num_traits']))

        

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


