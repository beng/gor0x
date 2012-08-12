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
        params = web.input(influencers=[])
        params.update(influencers='_'.join(params.influencers))
        model.insert('params', params)

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


