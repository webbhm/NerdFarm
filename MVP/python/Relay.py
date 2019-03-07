# Author: Howard Webb
# Date: 7/25/2017
# Code for managing the relay switch

import RPi.GPIO as GPIO
import time
from LogUtil import get_logger

ON=1
OFF=0

Relay1 = 29 # light
Relay2 = 31 # fan
Relay3 = 33 # LED
Relay4 = 35 # Pump

lightPin=29
fanPin=31
ledPin = 33
pumpPin = 35

class Relay(object):

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Relay1, GPIO.OUT)
        GPIO.setup(Relay2, GPIO.OUT)
        GPIO.setup(Relay3, GPIO.OUT)
        GPIO.setup(Relay4, GPIO.OUT)
        self.logger = get_logger('Relay')        
    
    def set_state(self, pin, state, test=False):
        '''Change state if different'''
        msg = "{}, {}, {}".format("Current ", state, GPIO.input(pin))
        self.logger.debug(msg)
        if state == ON and not GPIO.input(pin):
            self.set_on(pin)
            msg = "{} {} {}".format("Pin:", pin, " On")
            self.logger.debug(msg)
        elif state == OFF and GPIO.input(pin):
            self.set_off(pin)
            msg = "{} {} {}".format("Pin:", pin, " Off")
            self.logger.debug(msg)
        else:
            msg = "{} {} {}".format("Pin:", pin, " No Change")
            self.logger.debug(msg)

    def get_state(self, pin):
        '''Get the current state of the pin'''
        state=GPIO.input(pin)
        return state

    def set_off(self, pin, test=False):
        GPIO.output(pin, GPIO.LOW)

    def set_on(self, pin, test=False):
        GPIO.output(pin, GPIO.HIGH)

def test():
    
    relay=Relay()
    print("Test")
    print("Read #3 Unknown: " + str(relay.get_state(Relay3)))
    print("Test Fan and Lights")
    print("Turn Fan On")
    relay.set_on(fanPin, True)
    time.sleep(5)
    print("Turn Light On")
    relay.set_state(lightPin, True)
    time.sleep(5)
    print("Turn Fan Off")
    relay.set_off(lightPin, True)
    time.sleep(5)        
    print("Turn Light Off")
    relay.set_off(lightPin, True)
    time.sleep(5)

    print("Conditional Turn Fan On")
    relay.set_state(fanPin, ON, True)
    time.sleep(5)        
    print("Conditional Turn Fan On")
    relay.set_state(fanPin, ON, True)
    time.sleep(5)
    print("Conditional Turn Fan Off")
    relay.set_state(fanPin, OFF, True)
    time.sleep(5)        
    print("Conditional Turn Fan Off")
    relay.set_state(fanPin, OFF, True)

def test2():
    relay = Relay()
    relay.set_state(Relay3, ON)
    print("Relay 3 On")
    print("State 3" + relay.get_state(Relay3))
    time.sleep(10)
    relay.set_state(Relay3, OFF)    
    print("Relay 3 Off")
    print("State 3" + relay.get_state(Relay3))

def test1():
    relay=Relay()
    relay.set_state(Relay1, ON)
    relay.set_state(Relay1, OFF)
    relay.set_state(Relay2, ON)
    relay.set_state(Relay2, OFF)
    relay.set_state(Relay3, ON)
    relay.set_state(Relay3, OFF)
    relay.set_state(Relay4, ON)
    relay.set_state(Relay4, OFF)

def test3():
    relay = Relay1
    print("Test Relay")
    testRelay(relay)

def testRelay(relay):
    r = Relay()
    print("Read " + str(relay) + ": " + str(r.get_state(relay)))
    print(str(relay) + " Turn On")
    r.set_state(relay, ON)
    time.sleep(5)
    print(str(relay) + " Turn Off")
    r.set_state(relay, OFF)

if __name__=="__main__":
    test()

    
            
    

