from minibot.hardware.communication.ZMQ import ZMQExchange
from minibot.hardware.communication.TCP import TCP
import minibot.hardware.communication.UDP as UDP
from minibot.bot import Bot
from queue import Queue
import time, json
from threading import Thread

threads = []

def main():
    CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'
    config = json.loads(open(CONFIG_LOCATION).read())

    print("SETTING UP TCP")
    tcpInstance = TCP()

    print("SETTING UP UDP THREAD")
    thread_udp = Thread(target=UDP.udpBeacon)
    thread_udp.start()

    bot = Bot(config)
    print("RUNNING SWARMBOT (minion)")
    run(bot)

def run(bot):

    # get the IP of the mediator (hosted on the master) from the basestation
    TCP.tcp.send_to_basestation("SwarmIP", "")

    # look in the queue for info
    (key, value) = bot.extraCMD.get()
    while key != "SwarmIP":
        # keep searching the queue
        (key, value) = bot.extraCMD.get()

    if key == "SwarmIP":
        MEDIATOR_IP = value

    # Sets up ZMQ connection between master and minions. Starts subscriber-side 
    # connection
    z = ZMQExchange()
    z.setReceiver(MEDIATOR_IP)
    receivedQueue = Queue()
    
    receiveThread = Thread(target=z.receive, args=(receivedQueue, ))
    receiveThread.start()
    threads.append(receiveThread)

    try:
        while True:
            if (not receivedQueue.empty()):
                command = receivedQueue.get()
                
                # react to commamd
                bot.get_actuator_by_name("two_wheel_movement").move(command[0], command[1])
                
                #print "running ", command
            time.sleep(0.01)

            if not TCP.tcp.isConnected():
                break

    finally:
        cleanup(z)

def cleanup(z):
    for t in threads:
        t.join(1)

    z.stopZMQExchange()

if __name__=="__main__":
    main()
