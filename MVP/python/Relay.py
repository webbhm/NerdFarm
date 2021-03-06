# Author: Howard Webb
# Date: 7/25/2017
# Code for managing the relay switch

import RPi.GPIO as GPIO
import time
from LogUtil import Logger

ON=1
OFF=0

Relay1 = 29 # 
Relay2 = 31 # fan

FAN_PIN=Relay1

class Relay(object):

    def __init__(self, logger=None):
        self._logger = logger
        if logger == None:
           self._logger = Logger("Relay", Logger.INFO)
        self._logger.debug("Initialize Relay")
        GPIO.setwarnings(False)
        if not GPIO.getmode() == GPIO.BOARD:
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Relay1, GPIO.OUT)
        GPIO.setup(Relay2, GPIO.OUT)
        GPIO.setup(Relay3, GPIO.OUT)
        GPIO.setup(Relay4, GPIO.OUT)
        
    def __del__(self):
        '''
        Don't GPIO.cleanup() as need to leave pin state alone 
        '''
        pass
    
    def set_state(self, pin, state):
        '''Change state if different'''
        msg = "{}, {}, {}".format("Current ", state, GPIO.input(pin))
        self._logger.debug(msg)
        if state == ON and not GPIO.input(pin):
            self.set_on(pin)
            msg = "{} {} {}".format("Pin:", pin, " On")
            self._logger.debug(msg)
        elif state == OFF and GPIO.input(pin):
            self.set_off(pin)
            msg = "{} {} {}".format("Pin:", pin, " Off")
            self._logger.debug(msg)
        else:
            msg = "{} {} {}".format("Pin:", pin, " No Change")
            self._logger.debug(msg)

    def get_state(self, pin):
        '''Get the current state of the pin'''
        state=GPIO.input(pin)
        self._logger.debug("State: " + str(state))
        return state

    def set_off(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self._logger.debug("Set Off")

    def set_on(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        self._logger.debug("Set On")
        
  
    def watch_change(self, pin, callback):
        GPIO.setup(pin, GPIO.IN)
        # only react to going high
        GPIO.add_event_detect(pin, GPIO.RISING, callback)        
        

def test(level=Logger.DEBUG):
    
    relay=Relay()
    relay._logger.setLevel(level)
    print("Test")
    print("Debug Level: " + str(level))
    print("Read #3 Unknown: " + str(relay.get_state(Relay3)))
    print("Test Fan and Lights")
    print("Turn Fan On")
    relay.set_on(FAN_PIN)
    time.sleep(5)
    print("Turn Fan Off")
    relay.set_off(FAN_PIN)
    time.sleep(5)
    print("Turn Light On")
    relay.set_on(lightPin)
    time.sleep(5)
    print("Turn Light Off")
    relay.set_off(lightPin)
    time.sleep(5)

    print("Conditional Turn Fan On")
    relay.set_state(FAN_PIN, ON)
    time.sleep(5)        
    print("Conditional Turn Fan On")
    relay.set_state(FAN_PIN, ON)
    time.sleep(5)
    print("Conditional Turn Fan Off")
    relay.set_state(FAN_PIN, OFF)
    time.sleep(5)        
    print("Conditional Turn Fan Off")
    relay.set_state(FAN_PIN, OFF)

def validate():
    test(Logger.INFO)

if __name__=="__main__":
    test()

    
            
    

