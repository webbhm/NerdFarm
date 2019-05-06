# Actuator for pond pump run from the relay
# LOW/ON is pump off (normal state)
# This is wired so the pump is off if the power goes off (prevents flooding!!)

from Relay import *
from env import env
#from Recorder import record_env
from LogUtil import Logger
from CouchUtil import CouchUtil

class Pump:

    def __init__(self, logger=None):
        '''Initialize the object'''
        self.solenoidPin = Relay4
        if logger==None:
            self._logger = Logger('Solenoid', Logger.INFO)
        else:
            self._logger = logger
        self._relay=Relay(self._logger)
        self._couch=CouchUtil(self._logger)
        self._test = False
        
        self.activity_type = 'State_Change'

    def on(self):
        self._relay.set_off(self.solenoidPin)
        self._logger.debug("{}".format("Open Solenoid"))            
        self.logState("Open")
        
    def off(self):
        self._relay.set_on(self.solenoidPin)
        self._logger.debug("{}".format("Close Solenoid"))            
        self.logState("Closed")

    def getState(self):
        state=self._relay.get_state(self.solenoidPin)
        if state==0:
            return "On"
        else:
            return "Off"

    def logState(self, value):
        status_qualifier='Success'
        if self._test:
            status_qualifier='Test'
        self._couch.saveList(['State_Change', '', 'Pump', 'Reservoir', 'State', value, 'state', 'Solenoid', status_qualifier, ''])

def test(level=Logger.DEBUG, test=True):
    print("Pump Test")
    print("On")
    s = Pump()
    s._logger.setLevel(level)
    s._test = test
    s.on()
    print("State: " + s.getState())
    time.sleep(5)
    print("Off")
    s.off()
    print( "State: " + s.getState())
    
def test3():
    print("Test 3")
    s = Pump()
    print("On")
    s.on()
    time.sleep(5)
    s.off()
    print("Off")
    print("Done")

def manual():
    s = Solenoid()
#    print "On"
#    s.on()
    s.off()
    print("Off")
    print("Done")
    
def validate():
    test(Logger.INFO, False)

if __name__=="__main__":
    test()
        
        
        
