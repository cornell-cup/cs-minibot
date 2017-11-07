from hardware.communication.ZMQ import ZMQExchange
from hardware.communication.TCP import TCP
from threading import Thread
from peripherals.colorsensor import ColorSensor
import time

threads = []
count = {"F":0,"B":0,"L":0,"R":0}

def run(bot):
    # Sets up TCP connection between master and minions. Starts publisher-side 
    # connection.
    # always set the mediator first
    z = ZMQExchange()
    z.setMediator()
    z.setBroadcaster()
    
    TCP.tcp.send_to_basestation("SwarmIP", z.getIP("wlan0"))

    mediateThread = Thread(target=z.mediate)
    mediateThread.start()
    threads.append(mediateThread)
    
    #echobot(bot,z)
    colorbot(bot,z)
    
def colorbot(bot,z):
    speed = 10
    cs = bot.get_sensor_by_name("ColorSensor")
    cs.calibrate()
    pinkFirstTime = True
    orangeFirstTime = True
    
    try:
        while(True):
            c = cs.read_color()
            if(c=="RED"):
                # stop
                msg = (0,0)
                count["F"]=0
                count["B"]=0
                count["L"]=0
                count["R"]=0
                speed = 10
            elif(c=="GREEN"):
                # forwards
                count["F"]+=1
                count["B"]=0
                count["L"]=0
                count["R"]=0
                speed = increment_speed("F",3,speed,15)
                msg = (speed,speed)
            elif(c=="BLUE"):
                # backwards
                count["F"]=0
                count["B"]+=1
                count["L"]=0
                count["R"]=0
                speed = increment_speed("B",3,speed,15)
                msg = (-speed,-speed)
            elif(c=="YELLOW"):
                # turn left
                count["F"]=0
                count["B"]=0
                count["L"]+=1
                count["R"]=0
                speed = increment_speed("L",3,speed,15)
                msg = (-speed,speed)
            elif(c=="VIOLET"):
                # turn right
                count["F"]=0
                count["B"]=0
                count["L"]=0
                count["R"]+=1
                speed = increment_speed("R",3,speed,15)
                msg = (speed,-speed)
            z.broadcast(msg)
            time.sleep(0.2)
    finally:
        cleanup(z)

def increment_speed(direction, inc_time, speed, inc_amt):
    """ Given a direction, increments the speed after inc_time amount of seconds by
    inc_amt increase of power to the motors. 
    """
    if(count[direction]>(inc_time*5)):
        count[direction] = 0
        if(speed<50):
            speed += inc_amt
        print("Speed increased: " + str(speed))
    return speed

def echobot(bot,z):
    try:
        while(True):
            # msg is a tuple of left motor and right motor, respectively.
            msg = bot.get_actuator_by_name("two_wheel_movement").get_value()
            print("MSG: " + msg)
            z.broadcast(msg)
            time.sleep(0.1)

            if not TCP.tcp.isConnected():
                break

    finally:
        cleanup(z)

def cleanup(z):
    for t in threads:
        t.join(0.1)

    z.stopZMQExchange()
