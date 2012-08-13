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
import helper

urls = (
    '/', 'Index',
    '/fitness/(.+)', 'Fitness',)

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
        helper.Spawn().create_pool(**params)
        # will always be first individual since this is the beginning
        raise web.seeother('/fitness/0')

class Fitness():
    def GET(self, indi_id):
        traits = [trait for trait in model.get_traits(dict(indi_id=indi_id))]
        return render.fitness(title, traits)
        
    def POST(self):
        """Need to save re-ordering of pitches"""
        pass

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


