import tornado
import tornado.web
import os

class SetupApp:
    def __init__(self, port):
        self.port = port
        self.settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }

    def start(self):
        """
        Starts server for application.
        """
        app = self.make_app()
        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()

    def make_app(self):
        """
        Creates the application object (via Tornado).
        """
        return tornado.web.Application(self.handlers, **self.settings)

class MainSetup(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Title", items=[])

if __name__ == "__main__":
    setup_app = SetupApp(8080)
    setup_app.start()
