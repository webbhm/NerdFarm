"""
# Check status on boot
# Check lights correctly set
# Make sure Solenoid is closed
"""

from Pump import Pump
from env import env
from datetime import datetime
from datetime import timedelta
from LogUtil import Logger

class StartUp(object):
    
    def __init__(self, logger=None):
        if logger == None:
            self._logger = Logger("StartUp", Logger.INFO)
        else:
            self._logger = logger
        self._logger.debug("StartUp Initialized")            

    def check(self, test=False):
        """Main function to run what needs to be done at restart
        Args:
            test: flag for testing system
        Returns:
            None:
        Raises:
            None
        """    
        # Check the pump first to avoid flooding
        # Don't check state, just make sure it is off
        self._logger.debug("In check")
        pump_state = "Unknown"
        pump_state = self.pumpOff()
        light_state = "Unknown"
        try:
            light_state = self.checkLight()
        except Exception as e:
            self._logger.error(e)
        msg="{}, {}, {}, {}".format("Pump is ", pump_state, " Lights are ", light_state)
        self._logger.info(msg)
        
    def pumpOff(self):
        """Make sure the pump is turned off
        Args:
            test: flag for testing system
        Returns:
            state: (should be Off)
        Raises:
            None
        """
        self._logger.debug("In pumpOff")
        p = Pump(self._logger)
        p.off()
        msg = "Pump is turned off"
        self._logger.debug(msg)
        return "Off"

    def checkLight(self):
        """Check if lights should be on or off
        Args:
            test: flag for testing system
        Returns:
            None
        Raises:
            None
        """
        # Move import here so can trap if fails
        # couchdb library does not seem to load when initially starting
        self._logger.debug("In checkLight")
        import Light
        # Get times from env and split into components
        s=env['lights']['On']
        e=env['lights']['Off']
        state = self.determineState(s, e)
        l= Light.Light(self._logger)
        if state:
            l.set_on(test)
            return "On"
        else:
            l.set_off(test)
            return "Off"
            
    def determineState(self, start, end):
        ''' Determine if lights should be on or off'''
        s=start.split(':')
        e=end.split(':')    
        # Munge date into times
        t=datetime.now()
        st=t.replace(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
        et=t.replace(hour=int(e[0]), minute=int(e[1]), second=int(e[2]))

        if st > et:
            # Night Light - roll to next day when lights go off
            et += timedelta(days=1)

        msg = "{} {} {} {}".format("Start Time: ", st, "End Time: ", et)
        self._logger.debug(msg)
        
        if (st < datetime.now()) and (et > datetime.now()):
            msg="Lights should be On"
            self._logger.debug(msg)            
            return True
        else:
            msg="Lights should be Off"
            self._logger.debug(msg)        
            return False


def test(level=Logger.DEBUG):
    print("Test StartUp")
    st = StartUp()
    st._logger.setLevel(level)
    st.determineState('06:30:00', '22:00:00')
    st.determineState('15:30:00', '08:30:00')
    st.check()
    
def validate():
    test(Logger.INFO)
    
def main():
    st = StartUp()
    st.check()

if __name__=="__main__":
    main()
     
