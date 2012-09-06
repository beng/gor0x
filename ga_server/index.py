import web
import json
import ast

urls = (
        '/', 'Index',
        '/ga/population/(.*)', 'Population',)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())
title = 'GA Server'

class Index:
	def GET(self):
		# generate population
		params = ['spawn_pop', 'Vivaldi', 'winter_allegro', '5', '10']
		params = '/'.join(params)

		br = web.Browser()
		br.open(params)
		#traits = ast.literal_eval(traits)
		#traits = json.loads(traits)

		traits = json.loads(br.get_text())
		
		for trait in traits:
			model.population_save_individual(trait)

		# pass to pyevolve
		
		# fitness

		# select

		# crossover

		# mutate

		# termination?
		return render.index(title)

class Population:
	"""Generate a population"""

	def GET(self, generation=0):
		params = ['markov', '100', '5', 'Vivaldi', 'winter_allegro']
		params = '/'.join(params)

		br = web.Browser()
		br.open(params)
		traits = eval(br.get_text())	# string to list

	
if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run() 


