# currently not in the required format dictated by cs-minibot/test.py,
# but will do

from basestation.base_station import BaseStation
from basestation.bot.connection.tcp_connection import TCPConnection
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
        tcp_connection_obj = TCPConnection(discovered_bots.pop(), 10000)
        testbot = bs.get_bot_manager().add_bot(tcp_connection_obj, "testbot")

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
            else:
                print("bot not accessible")

        else:
            print("error in adding testbot")
