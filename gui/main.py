"""
Main file from which BaseStation HTTP interface begins.
"""

import tornado
import tornado.web
import os.path
import json

# Minibot imports.
from basestation.base_station import BaseStation
from basestation.bot.commands.command_center import CommandCenter

class BaseInterface:
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
            ("/gui", BaseStationHandler),
            ("/addBot", AddBotHandler),
            ("/commandBot", CommandBotHandler),
            ("/discoverBot", DiscoverBotsHandler)
        ]
        self.settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        self.base_station = BaseStation()

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

class BaseStationHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hi There")
        self.render("../gui/index.html", title="Title", items=[])

class AddBotHandler(tornado.web.RequestHandler):
    """
    Adds a bot to the BotManager.
    """
    def post(self):
        info = json.loads(self.request.body)
        discovered_bots = BaseStation().bot_manager.get_all_discovered_bots()
        print("Adding bot!")
        print(info)
        print(discovered_bots)
        print("That was the info.")

        name = info['name']
        ip = info['ip']
        port = info['port']

        bot_name = BaseStation().get_bot_manager().add_bot(name, ip, port)
        print('THING')
        print(bot_name)
        self.write(bot_name)

class CommandBotHandler(tornado.web.RequestHandler):
    """
    Used to send movement commands to minibots.
    """
    def post(self):
        info = json.loads(self.request.body)
        name = info['name']
        front_left = info['fl']
        front_right = info['fr']
        back_left = info['bl']
        back_right = info['br']

        # Gets virtual bot.
        bot = BaseStation().get_bot_manager().get_bot_by_name(name)
        # Gets command center.
        cc = bot.get_command_center()
        self.write(cc.sendKV("WHEELS", front_left + "," + front_right + "," + back_left +
                             "," + back_right))

class DiscoverBotsHandler(tornado.web.RequestHandler):
    def post(self):
        discovered = BaseStation().get_bot_manager().get_all_discovered_bots()
        return discovered

if __name__ == "__main__":
    """
    Main method for running base station GUI.
    """
    base_station = BaseInterface(8080)
    base_station.start()
