# currently not in the required format dictated by cs-minibot/test.py,
# but will do

from basestation.base_station import BaseStation as BaseStation
from basestation.bot.connection.tcp_connection import TCPConnection as \
    TCPConnection
import time

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
        else:
            print("error in adding testbot")
