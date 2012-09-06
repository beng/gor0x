import web

urls = (
        '/', 'Index',)

render = web.template.render('templates/', base='')

title = 'GA Server'

class Index:
    def GET(self):
        return "index"

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


