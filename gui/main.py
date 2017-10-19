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
            ("/discoverBot", DiscoverBotsHandler),
            ("/sendKV", SendKVHandler)
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
        info = json.loads(self.request.body.decode())
        discovered_bots = BaseStation().bot_manager.get_all_discovered_bots()
        print("Adding bot!")
        print(info)
        print(discovered_bots)
        print("That was the info.")

        name = info['name']
        ip = info['ip']
        port = info['port']

        bot_name = BaseStation().get_bot_manager().add_bot(name, ip, port)
        print("Bot name: " + bot_name)
        self.write(bot_name.encode())


class CommandBotHandler(tornado.web.RequestHandler):
    """
    Used to send movement commands to minibots.
    """
    def post(self):
        info = json.loads(self.request.body.decode())
        name = info['name']
        fl = info['fl']
        fr = info['fr']
        bl = info['bl']
        br = info['br']

        # Gets virtual bot.
        bot_cc = BaseStation().get_bot_manager().\
            get_bot_by_name(name).get_command_center()

        # temp success/failure messages
        if bot_cc.set_wheel_power(fl, fr, bl, br):
            self.write("Wheel power adjusted".encode())
        else:
            self.write("Wheel power adjustment failed".encode())


class DiscoverBotsHandler(tornado.web.RequestHandler):
    def post(self):
        discovered = BaseStation().get_bot_manager().get_all_discovered_bots()
        self.write(discovered)

class SendKVHandler(tornado.web.RequestHandler):
    def post(self):
        info = json.loads(self.request.body.decode())
        key = info['key']
        val = info['value']
        name = info['name']
        print("Sending key (" + key + ") and value (" + val + ") to " + name)

        # Sends KV through command center.
        bot_cc = BaseStation().get_bot_manager.get_bot_by_name(name).get_command_center()
        return bot_cc.sendKV(key, val)

if __name__ == "__main__":
    """
    Main method for running base station GUI.
    """
    base_station = BaseInterface(8080)
    base_station.start()
