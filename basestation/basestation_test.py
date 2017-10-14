# currently not in the required format dictated by cs-minibot/test.py,
# but will do

from basestation.base_station import BaseStation as BaseStation
import time

if __name__ == "__main__":
    bot = BaseStation()
    while True:
        time.sleep(2)
        print("discovered bots: ",
              bot.get_bot_manager().get_all_discovered_bots())
