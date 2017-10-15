Intro to BaseStation v2.22e-16 Python
=====================================

### Updated Oct 15 2017.
##### Aimed at giving devs insight of how to use a base station to control their MiniBots.

# Links

* [The Java platform](https://github.com/cornell-cup/cs-minibot-platform)
* [The Python platform](https://github.com/cornell-cup/cs-minibot)
* [Java platform's BaseStation controller file](https://github.com/cornell-cup/cs-minibot-platform/blob/develop/cs-minibot-platform-src/src/main/java/minibot/BaseHTTPInterface.java)

# Using the BaseStation module/class

This Python version of the BaseStation is _almost_ equivalent to the Java version in cs-minibot-platform, and the usage is pretty similar.

Take a look at this [example script](https://github.com/cornell-cup/cs-minibot/blob/basestation/basestation/basestation_test.py) first.

**Always check for None values to avoid bugs**

* Import the BaseStation module/class. The import can be done from any script in the cs-minibot repo (I think). This should be enough for you to control _everything_, though I may be wrong.
  * `from basestation.base_station import BaseStation`
* Accessing the BaseStation
  * The BaseStation, as in the Java platform, is a **Singleton** class and you can access an instance using `BaseStation()`. Whenever you call it, it will always give you the same BaseStation instance as has been running elsewhere in the program.
  * A common idiom can be `bs = BaseStation()` if you want to make your code less clumsy.
* Accessing the BotManager and VisionManager
  * To add/play with MiniBots, we provide a `VirtualBot` instance on the BaseStation, that handles the communication between the real MiniBot and the BaseStation running device, and emulates a virtual bot on your device, as the name suggests.
  * You cannot directly add a `VirtualBot` instance to the BaseStation, but you can do so through the `BotManager` class, that will be your best friend throughout this tutorial. Get it by `BaseStation().get_bot_manager()` (common idiom can be `bm = BaseStation().get_bot_manager()` and use `bm` afterwards in the file).
  * `VisionManager` can be accessed as `BaseStation().get_vision_manager()` but most people won't need this often.
* Adding `VirtualBot`s
  * `bm.add_bot("name-of-bot", "IP of bot", port)` (port is optional, and the default is 10000). This method will return the `"name-of-bot"` that was added, and `None` if the operation failed. The operation can fail due to several reasons, including but not limited to:
    * TCP Connection could not be initiated.
    * TCP Connection initiated, but is not active.
    * Something related to the `VirtualBot` or MiniBot crashed.
    * A cosmic radiation from the space interacted with Earth's atmosphere, sending a high-energy neutron that hit your computer's memory unit and messed with some bits. This can potentially crash your computer too. However, the probability is too low for this to happen on a personal computer.
  * That's basically it.
* Remove a `VirtualBot`
  * Get the name of the VirtualBot you want to remove and call `bm.remove_bot_by_name("name-of-bot")`.
* Controlling a MiniBot's motion
  * First get control of the `VirtualBot` object created for your MiniBot by calling `mybot = bm.get_bot_by_name("name-of-bot")`.
  * Now get it's command center with `cc = mybot.get_command_center()`.
  * Send commands like this:
    ```Python
    # this is bad design from our side, and we will change this.
    cc.sendKV("WHEELS", fl + "," + fr + "," + bl + "," + br)
    ```
    where fl is the power of front-left wheel, br is the power of back-right wheel.
* Discovered MiniBots
  * The BaseStation initiates a UDP Listener that listens for MiniBot's broadcasted messages. If a MiniBot's message reaches the device on the network, that MiniBot's IP is stored in an internal map.
  * Access all discovered bots with `bm.get_all_discovered_bots()`, which returns a list of IPs corresponding to the MiniBots that are currently active.
  * Can similarly get all tracked bots with `bm.get_all_tracked_bots()`, which returns a list of all `VirtualBots` instances that were successfully created since the program started but not removed. There is no guarantee that all of them are active. Use discovered bots to find which MiniBots are still broadcasting their presence in the network.
* Sending `"RUN"` or `"SCRIPT"` instructions to the the MiniBot from the BaseStation
  * `"RUN"` will run a script on the MiniBot, **which is already present in the MiniBot's directory**.
  * `"SCRIPT"` can send a new script **that is not present on the MiniBot currently**.
  * `bm.get_bot_by_name("name-of-bot").get_command_center().sendKV("RUN", "script-name")`
  * `bm.get_bot_by_name("name-of-bot").get_command_center().sendKV("SCRIPT", "script-as-a-string")`
