# Actuator for pond pump run from the relay
# LOW/ON is pump off (normal state)
# This is wired so the pump is off if the power goes off (prevents flooding!!)

from Relay import *
from env import env
#from Recorder import record_env
from LogUtil import get_logger
from CouchUtil import saveList

class Pump:

    def __init__(self):
        '''Initialize the object'''
        self.solenoidPin = Relay4
        self.Relay=Relay()
        self._logger = get_logger('Solenoid')
        self.activity_type = 'State_Change'

    def on(self, test=False):
        self.Relay.set_off(self.solenoidPin)
        self._logger.debug("{}".format("Open Solenoid"))            
        self.logState("Open")
        
    def off(self, test=False):
        self.Relay.set_on(self.solenoidPin)
        self._logger.debug("{}".format("Close Solenoid"))            
        self.logState("Closed")

    def getState(self, test=False):
        state=self.Relay.get_state(self.solenoidPin)
        if state==0:
            return "On"
        else:
            return "Off"

    def logState(self, value, test=False):
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        saveList(['State_Change', '', 'Pump', 'Reservoir', 'State', value, 'state', 'Solenoid', status_qualifier, ''])

    def test(self):
        print("Pump Test")
        print("On")
        self.on(True)
        print("State: " + self.getState())
        time.sleep(5)
        print("Off")
        self.off(True)
        print("State: " + self.getState())

    def test2(self):
        state=self.getState(True)
        print( "State: " + state)

def test():
    print("Pump Test")
    print("On")
    s = Pump()
    s.on(True)
    print("State: " + s.getState())
    time.sleep(5)
    print("Off")
    s.off(True)
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

if __name__=="__main__":
    test()
        
        
        
