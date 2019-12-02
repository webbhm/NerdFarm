
from Pump import *
import time
from env import env
from EC import EC
from LogUtil import Logger
from Persistence import Persistence


# full and low will be different for seedlings (without roots) and plants
full_ec = 19000
empty_ec = 25000
fill_time = 5
timeout = 10

class Reservoir:

    FULL=0
    EMPTY=1
    OK=2

    vol_per_mm = 0.3785  # estimate 1 gal per 10 mm, this is reservoir specific
    vol_per_sec = 0.3785  # estimate 100 ml per sec, this is reservoir specific
    
    def __init__(self):
        '''Get distances for determining reservoir levels'''
        self.res={'full':full_ec, 'empty':empty_ec, 'timeout':timeout}
        self._activity_type = 'Agronomic_Activity'
        self._logger = Logger('LogReservoir', Logger.INFO)
        self._persist = Persistence(self._logger)
        self._logger.detail("Reservoir Initialized")
        # flag for testing
        self._test=False

    def getStatus(self):
        "Logic for calling the reservoir full"
        self._logger.detail("In getStatus")        
        ec=self.getEC()
        if ec <= full_ec:
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir Full", EC, ec))            
            return Reservoir.FULL, ec
        elif ec >= empty_ec:
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir Empty", EC, ec))                        
            return Reservoir.EMPTY, ec
        else:
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir not Empty", EC, ec))                        
            return Reservoir.OK, ec

    def isFull(self):
        self._logger.detail("In isFull")                
        status, ec = self.getStatus()
        if status==Reservoir.FULL:
            return True
        else:
            return False

    def getEC(self):
        '''Get EC reading'''
        self._logger.detail("In getEC")                
        snsr = EC(self._logger)
        return snsr.getEC()

    def fill(self, test=False):
        ''' Routine to control re-filling of the reservoir'''
        self._logger.detail("{}".format("In Fill"))                                
        start_ec=self.getEC()
        start_t=time.time()
        pump=Pump()
        pump.on()
        # Loop till filled or times out
        while (not self.isFull()) and self.isFilling(start_t):
            self._logger.detail("{}".format("In Fill Loop"))                                            
        self._logger.detail("{}".format("Exit Fill Loop, close solenoid"))                                            
        # Close valve
        pump.off()
        # Calculate amount filled
        stop_t=time.time()        
        stop_ec=self.getEC()
        dif_t = stop_t - start_t
        volume = dif_t * self.vol_per_sec
        self._logger.detail("{}".format("Exit Fill"))                                            

        return volume

    def isFilling(self, start_time, test=False):
        '''Check that actually filling: the distance is actually changing'''
        start_ec=self.getEC()
        self._logger.detail("{} {}".format("Filling, Start EC:", start_ec))                                            
        time.sleep(fill_time)

# Check for level change first, else will never get to this logic till timeout        
        end_ec = self.getEC()
        change = start_ec - end_ec
        if end_ec < start_ec:  # need to see at least a 5mm change
            self._logger.detail("{} {} {} {} {} {}".format("Still Filling, change:", change, "Start", start_ec, "End", end_ec))                                            
            return True
        else:
            self._logger.detail("{} {} {} {} {} {}".format("Not Filling, no change:", change, "Start", start_ec, "End", end_ec))                                            
            return False

# Check for timeout        
        stop_time = time.time()
        if stop_time - start_time > self.res['timeout']:
            self._logger.detail("{}".format("Timeout"))                                            
            return False
        else:
            return True

    def checkReservoir(self):
        '''Check condition of reservoir and fill if necessary'''
        self._logger.detail("{}".format("Check Reservoir"))                                            
        status, ec = self.getStatus()
        self._logger.debug("{} {} {} {}".format("Status:", status, "EC", ec))                                            
        
        # Is full, log state
        if status==Reservoir.FULL:
            self._logger.detail("{}".format("Status: Full"))
            self._logger.info("{} {} {} {}".format("EC:", ec, "Full level:", self.res['full'], "Empty:", self.res['empty']))                                                        
            return True
        else:
            # Needs filling
            self._logger.debug("{}".format("Status: Filling"))            
            volume=self.fill()
            if volume > 0:
                # Filled, log volume
                self.logState(volume, 'Success')
                return True
            else:
                # Failure
                self._logger.debug("{}".format("Status: Failure"))                
                level='Empty'
                if status=='2':
                    level='Ok'
                self._logger.error("{}".format("Failure to fill Reservoir"))                
                self._logger.error("{} {} {} {}".format("EC:", ec, "Full level:", self.res['full'], "Empty:", self.res['empty']))                                                        
                self.logState(volume,'Failure')
                return False            

    def logState(self, value, status_qualifier):

        if self._test:
            status_qualifier='Test'
        txt={'Volume': value, 'full_level': self.res['full'], 'empty_level': self.res['empty'], 'status': 'Full'}        
        self._persist.save(['State_Change', '', 'Nutrient', 'Reservoir', 'Volume', value, 'Liter', 'Solenoid', status_qualifier, ''])
        self._logger.info(txt)

def test(level=Logger.DEBUG, test=True):
        print("Testing Reservoir")
        r = Reservoir()
        r._logger.setLevel(level)
        r._test = test
        ec = r.getEC()
        state="OK"
        if ec < Reservoir.FULL:
            state="Full"
        elif ec > Reservoir.EMPTY:
            state="Empty"
        print("State: " + state)    
        print( str({'EC': ec, 'full_level': r.res['full'], 'empty_level': r.res['empty'], 'status':state}))
        status, ec = r.getStatus()
        print("{}: {}, {}: {}".format("Status", status, "EC", ec))
        
def validate():
    test(Logger.INFO)
    
def main():    
    r=Reservoir()
    r.checkReservoir()

if __name__=="__main__":
    main()