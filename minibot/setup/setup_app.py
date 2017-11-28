import json
import tornado
import tornado.web
import os
import subprocess
import sys


class SetupApp:
    """
    An instance of this class creates a handle for a tornado-based website that is a simple form at URL 10.0.0.1:8080 (default port is 
    8080).
    - The form collects wifi credentials, and the submit button triggers a reset to the wifi settings on the pi.
    - On reboot (after this app has exited), the pi becomes automatically connected to the wifi that was supplied by the user.
    """
    
    def __init__(self, port=8080):
        """
        Initializes the tornado webapp handler at <IP>:port.
        
        Args:
            port (int): Port to associate the webapp handle with. (Default=8080) 
        """
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
    """
    Renders the page to be displayed on the website base URL.
    """
    
    def get(self):
        """
        Gets the index page to be displayd.
        """
        self.render("app/index.html", title="Title", items=[])


class WifiCredsHandler(tornado.web.RequestHandler):
    """
    Handles trigger by the user to submit wifi credential information.
    """
    
    def post(self):
        """
        Loads the information from the web page's form and calls the bash scripts to set the wifi configuration settings.
        """
        info = json.loads(self.request.body.decode())

        # call the bash script to feed the wifi credentials
        res1 = subprocess.run(["sudo", "./handle_startup_wifi_connection.sh", "clean"])
        res2 = subprocess.run(["sudo", "./handle_startup_wifi_connection.sh", 
            "wifi", info['wifiname'], info['wifipass']])
        
        if res1.returncode != 0 or res2.returncode != 0:
            # wifi setup failed
            self.write("wifi setup failed!".encode())
        else:
            # wifi setup succeeded
            tornado.ioloop.IOLoop.instance().stop()
            sys.exit(0)
            self.write("wifi setup succeeded!".encode())


if __name__ == "__main__":
    setup_app = SetupApp(8080)
    setup_app.start()
