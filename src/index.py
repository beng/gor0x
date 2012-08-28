"""
@author   Ben G
@email    beg5670@gmail.com
@website  http://github.com/beng
  
this is a genetic algorithm that composes melodies. 
"""

from music21 import *
import web
import random
import json

#import model
import helper.song_name as song_name
import helper.consts as consts
import helper.utility as utility
import ga

urls = (
    '/', 'Index',
    '/fitness/(.+)', 'Fitness',
    '/extract_midi/(.*)', 'ExtractMidi',
    '/markov/(.+)/(.+)', 'Markov',)

render = web.template.render('templates/', base='layout')
song_selection = list(song_name.parse_name('static/pitches/'))
title = "Melody Composer"

'''
########################################################
# Index
########################################################
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

########################################################
# Fitness
########################################################
class Fitness:
    def GET(self, indi_id):
        traits = [trait for trait in model.get_traits(dict(indi_id=indi_id))]
        return render.fitness(title, traits)
        
    def POST(self):
        """Need to save re-ordering of pitches"""
        pass
'''

########################################################
# Markov JSON REST
########################################################
class Markov:
    """Return json of Markov chain"""

    def GET(self, size, nodes, influencer=consts.name):
        """Call with influencer name and other shit"""        
        pool = ga.genome(ExtractMidi().GET(influencer))
        web.header('Content-Type', 'application/json')
        
        return json.dumps({influencer : pool, 'settings' : {'size' : size, 'nodes' : nodes}})

########################################################
# Extract Midi JSON REST
########################################################
class ExtractMidi:
    """Return json of traits"""

    def GET(self, influencer):
        """Return traits of requested influencer"""
        # @TODO add parameter to accept different traits
        # @TODO remove default influencer and throw error
        #       if no influencer is supplied
         
        if '' in influencer:
            influencer = consts.name

        try:
            parsed_corpus = utility.extract_traits(utility.extract_corpus(influencer), traits=[note.Note, note.Rest])  
            # duration can be any name becuase we are just checking for type
            web.header('Content-Type', 'application/json')
            return json.dumps({influencer : parsed_corpus})
        except Exception, e:
            print 'issue with influencer request. please try again!'
            raise e      
        

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


