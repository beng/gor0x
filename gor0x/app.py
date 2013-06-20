import web

urls = (
    '/', 'Index'
)

render = web.template.render('templates/', base='layout')
app = web.application(urls, globals())


class Index(object):
    def GET(self):
        pass


if __name__ == "__main__":
    app.internalerror = web.debugerror
    app.run()
