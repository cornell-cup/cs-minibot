import json
import tornado
import tornado.web
import os
import subprocess
import sys


class SetupApp:
    def __init__(self, port):
        self.port = port
        self.handlers = [
            ("/", WifiSetupPageHandler),
            ("/submitWifiCreds", WifiCredsHandler)
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


class WifiSetupPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("app/index.html", title="Title", items=[])


class WifiCredsHandler(tornado.web.RequestHandler):
    def post(self):
        print(self.request.body)
        print(self.request.body.decode())
        info = json.loads(self.request.body.decode())
        print("Wifi Name", info['wifiname'])
        print("Wifi Pass", info['wifipass'])

        # call the bash script to feed the wifi credentials
        res1 = subprocess.run(["sudo", "./handle_startup_wifi_connection.sh", "clean"])
        res2 = subprocess.run(["sudo", "./handle_startup_wifi_connection.sh", 
            "wifi", info['wifiname'], info['wifipass']])
        if res1.returncode != 0 or res2.returncode != 0:
            print("wifi setup failed")
            self.write("wifi setup failed!".encode())
        else:
            print("wifi setup success")
            sys.exit()
            self.write("wifi setup succeeded".encode())


if __name__ == "__main__":
    setup_app = SetupApp(8080)
    setup_app.start()
