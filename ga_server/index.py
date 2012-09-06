import web

urls = (
        '/', 'Index',
        '/ga/population/(.+)/(.+)/(.+)/(.+)', 'Population',)

render = web.template.render('templates/', base='')
app = web.application(urls, globals())
title = 'GA Server'

class Population:
	def GET(self, size, nodes, artist, song):
		# request markov population
		br = web.Browser().open('http://localhost:8080/markov')

class Index:
    def GET(self):
        return "index"

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run() 


