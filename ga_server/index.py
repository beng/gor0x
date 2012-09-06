import web

urls = (
        '/', 'Index',
        '/ga/population/(.*)', 'Population',)

render = web.template.render('templates/', base='')
app = web.application(urls, globals())
title = 'GA Server'

class Population:
	def GET(self, generation=0):
		params = ['markov', '100', '5', 'Vivaldi', 'winter_allegro']
		params = '/'.join(params)
		
		br = web.Browser()
		br.open(params)
		
		return br.get_text()

class Index:
    def GET(self):
        return "index"

if __name__ == "__main__":
   app.internalerror = web.debugerror
   app.run() 


