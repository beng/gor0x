import web
import httplib2

urls = (
        '/', 'Index',
        '/ga/population/(.*)', 'Population',)

render = web.template.render('templates/', base='')
app = web.application(urls, globals())

title = 'GA Server'
h = httplib2.Http()
root = 'http://localhost:8080'

class Population:
	def GET(self, generation=0):
		size = '100'
		nodes = '5'
		artist = 'Vivaldi'
		song = 'winter_allegro'
		call = '/markov/'+ size + '/' + nodes + '/' + artist + '/' + song
		path = root + call
		request = h.request(path, 'GET')

class Index:
    def GET(self):
        return "index"

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run() 


