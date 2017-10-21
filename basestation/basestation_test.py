# currently not in the required format dictated by cs-minibot/test.py,
# but will do

from basestation.base_station import BaseStation
from basestation.xbox.xbox_manager import XboxManager
import time

forward = ("50.0", "50.0", "50.0", "50.0")
stop = ("0.0", "0.0", "0.0", "0.0")

if __name__ == "__main__":
    bs = BaseStation()

    discovered_bots = bs.get_bot_manager().get_all_discovered_bots()
    while not discovered_bots:
        # list is empty
        time.sleep(2)
        discovered_bots = bs.get_bot_manager().get_all_discovered_bots()

    if discovered_bots:
        # list is not empty
        print("discovered bots: ", discovered_bots)
        testbot = bs.get_bot_manager().add_bot("testbot", discovered_bots.pop(),
                                               port=10000)

        if testbot is not None:
            print("testbot added")
            ttbot = bs.get_bot_manager().get_bot_by_name(testbot)
            if ttbot is not None:
                cc = ttbot.get_command_center()
                print("sending forward")
                cc.sendKV("WHEELS",
                          forward[0] + "," + forward[1] + "," + forward[2] +
                          "," + forward[3])
                time.sleep(5)
                print("sending stop")
                cc.sendKV("WHEELS",
                          stop[0] + "," + stop[1] + "," + stop[2] +
                          "," + stop[3])
                print("should stop")

                default_xbox_id = 0
                xbox_res = XboxManager().run_xbox(testbot, default_xbox_id)

                msg = ""
                if xbox_res is None:
                    msg = "Xbox with ID = " + str(
                        default_xbox_id) + "not detected."
                elif xbox_res < 0:
                    msg = "No MiniBot with name " + testbot + " exists."
                else:
                    msg = "MiniBot " + testbot + " associated with Xbox with " \
                                                "ID = " + \
                          str(default_xbox_id) + "."
                print(msg)
                while True:
                    pass
            else:
                print("bot not accessible")

        else:
            print("error in adding testbot")
