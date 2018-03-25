"""
Main file from which BaseStation HTTP interface begins.
"""

import tornado
import tornado.web
import os.path


class Gui:
    """
    Class which contains the base station and necessary functions for running the
    base station GUI.
    """
    def __init__(self, port):
        """
        Initializes base station
        :param port: Port number from which basestation runs.
        """
        self.port = port
        self.handlers = [
            ("/", MainHandler),
        ]
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


class MainHandler(tornado.web.RequestHandler):
    """
    Displays the GUI front-end.
    """
    def get(self):
        # self.write("Hi There")
        self.render("../gui/index.html", title="Title", items=[])


if __name__ == "__main__":
    """
    Main method for running base station GUI.
    """
    gui = Gui(8080)
    gui.start()

"""
MISSING ENDPOINTS:

High priority:
- trackedBots

Low priority:
- postOccupancyMatrix

"""