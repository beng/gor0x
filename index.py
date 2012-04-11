import web

urls = (
        '/', 'index',
        )

render = web.template.render('templates/', base='layout')

class index():
    def GET(self):
        title = 'Mmm Espresso'
        return render.index(title)

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.internalerror = web.debugerror
   app.run() 


