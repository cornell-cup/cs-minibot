"""
Main file from which BaseStation HTTP interface begins.
"""

import tornado
import tornado.web
import os.path
import json
import logging

# Minibot imports.
from basestation.base_station import BaseStation

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
            ("/", BaseStationHandler),
            ("/gui", BaseStationHandler),
            ("/addBot", AddBotHandler),
            ("/commandBot", CommandBotHandler),
            ("/discoverBots", DiscoverBotsHandler),
            ("/getTrackedBots", GetTrackedBotHandler),
            ("/removeBot", RemoveBotHandler),
            ("/sendKV", SendKVHandler),
            #("/getBotData", BotDataHandler),
            ("/vision", VisionHandler)
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
    """
    Displays the GUI front-end.
    """
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
        res = {"botName": bot_name, "ip": ip}
        self.write(json.dumps(res).encode())


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
    """
    Listens for bot discoverability.
    """
    def post(self):
        discovered = BaseStation().get_bot_manager().get_all_discovered_bots()
        print("Discovered bot: " + str(discovered))
        self.write(json.dumps(discovered))


class GetTrackedBotHandler(tornado.web.RequestHandler):
    """
    Gets bot tracked by BotManager.
    """
    def post(self):
        tracked_bots = BaseStation().bot_manager. get_all_tracked_bots_names()
        print('Bots Tracked: ' + str(tracked_bots))

        self.write(json.dumps(tracked_bots).encode())


class RemoveBotHandler(tornado.web.RequestHandler):
    """
    Used to remove a MiniBot.
    """

    def post(self):
        info = json.loads(self.request.body.decode())
        name = info["name"]
        op_successful = BaseStation().get_bot_manager().remove_bot_by_name(name)

        if op_successful:
            self.write(("MiniBot " + name + " successfully removed").encode())
        self.write(("Could not remove " + name).encode())


class SendKVHandler(tornado.web.RequestHandler):
    """
    Sends Key-Value pair to bot to run pre-loaded scripts or run other bot-related
    commands.
    """
    def post(self):
        info = json.loads(self.request.body.decode())
        key = info['key']
        val = info['value']
        name = info['name']
        print("Sending key (" + key + ") and value (" + val + ") to " + name)

        # Sends KV through command center.
        bot_cc = BaseStation().get_bot_manager().\
            get_bot_by_name(name).get_command_center()
        self.write(json.dumps(bot_cc.sendKV(key, val)))

class ScriptHandler(tornado.web.RequestHandler):
    """
    Sends scripts written in GUI to bot to run.
    """
    def post(self):
        info = json.loads(self.request.body.decode())
        name = info['name']
        script = info['script']

        bot = BaseStation().get_bot_manager().get_bot_by_name(name)
        if bot is not None:
            print("Script sent to " + name + "!")
            self.write(bot.get_command_center().sendKV("SCRIPT", script))
        else:
            logging.warning("[ERROR] Bot not detected when trying to send script.")


class XboxHandler(tornado.web.RequestHandler):
    """
    Handles XBOX.
    """
    def post(self):
        pass

# class BotDataHandler(tornado.web.RequestHandler):
    #"""
    #Handles Bot Data.
    #"""
    #def get(self):
    #    info = json.loads(self.request.body.decode())
    #    print(info)
    #    name = info['name']
    #    bot = BaseStation().get_bot_manager().get_bot_by_name(name)
    #    if bot is not None:
    #        center = bot.get_sensor_center()
            #getalldatajson is not implemented, assume that it gives the name of the sensor as keys
    #        sensorinfo = list(center.get_all_data_json().keys())
    #    else:
    #        logging.warning("[ERROR] Bot not detected when trying to get data.") */


class VisionHandler(tornado.web.RequestHandler):
    """
    Handles vision data.
    """
    def post(self):
        info = json.loads(self.request.body.decode())
        tag_id = info['id']
        x, y, z = info['x'], info['y'], info['z']
        logging.info("Received vision data " + str((tag_id, x, y, z)))
        # TODO Update appropriate bots with position info

if __name__ == "__main__":
    """
    Main method for running base station GUI.
    """
    base_station = BaseInterface(8080)
    base_station.start()
