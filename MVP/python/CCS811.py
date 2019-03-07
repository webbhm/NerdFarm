'''
See the following for technical documentation
https://cdn.sparkfun.com/datasheets/BreakoutBoards/CCS811_Programming_Guide.pdf
'''

from I2CUtil import I2C, bytesToWord
from BitField import bitfield
from time import sleep

path = "/dev/i2c-1"
addr = 0x5a

CCS811_HW_ID = 0x20


CCS811_STATUS = 0x00
CCS811_MEAS_MODE = 0x01
CCS811_ALG_RESULT_DATA = 0x02
CCS811_RAW_DATA = 0x03
CCS811_ENV_DATA = 0x05
CCS811_NTC = 0x06
CCS811_THRESHOLDS = 0x10
CCS811_BASELINE = 0x11
CCS811_HW_ID = 0x20
CCS811_HW_VERSION = 0x21
CCS811_FW_BOOT_VERSION = 0x23
CCS811_FW_APP_VERSION = 0x24
CCS811_ERROR_ID = 0xE0
CCS811_SW_RESET = 0xFF

CCS811_BOOTLOADER_APP_ERASE = 0xF1
CCS811_BOOTLOADER_APP_DATA = 0xF2
CCS811_BOOTLOADER_APP_VERIFY = 0xF3
CCS811_BOOTLOADER_APP_START = 0xF4

# Data read modes - time between reads
CCS811_DRIVE_MODE_IDLE = 0x00
CCS811_DRIVE_MODE_1SEC = 0x01
CCS811_DRIVE_MODE_10SEC = 0x02
CCS811_DRIVE_MODE_60SEC = 0x03
CCS811_DRIVE_MODE_250MS = 0x04

# Error Register
ERR_MSG_INVALID = 0x00
ERR_READ_REG_INVALID = 0x01
ERR_MEASMODE_INVALID = 0x02
ERR_MAX_RESISTANCE = 0x03
ERR_HEATER_FAULT = 0x04
ERR_HEATER_SUPPLY = 0x05

CCS811_HW_ID_CODE = 0x81
CCS811_REF_RESISTOR = 100000

APP_START = 0xF4
VALID_SENSOR_APP_MODE = 0x90

MASTER = 1
SLAVE = 0

class CCS811(object):

    def __init__(self, mode=MASTER, test=False):
        """Create sensor object
           Args:
               None
           Returns:
               None
           Raises:
               None
        """        
        self._addr = addr
        self._path = path
        self._i2c = I2C(path, addr)
        # Set up variables and bitfield registers
        self._TVOC = 0
        self._eCO2 = 0
        self.tempOffset = 0
        self._status = bitfield([('ERROR' , 1), ('unused', 2), ('DATA_READY' , 1), ('APP_VALID', 1), ('unused2' , 2), ('FW_MODE' , 1)])
        self._meas_mode = bitfield([('unused', 2), ('INT_THRESH', 1), ('INT_DATARDY', 1), ('DRIVE_MODE', 3)])
        self._error = bitfield([('ERR_HEATER_SUPPLY', 5), ('ERR_HEATER_FAULT', 4), ('ERR_MAX_RESISTANCE', 3), ('ERR_MEASMODE_INVALID', 2), ('ERR_READ_REG_INVALID', 1), ('ERR_MSG_INVALID', 0)])
        if mode:
            self.initialize(test)
        
    def initialize(self, test=False):        
        """Workflow for starting the sensor
           Args:
               self
               test
           Returns:
               None
           Raises:
               None
        """          
        # Boot Mode (power up)
        # Initialization Flow
        # Read HW_ID and validate
        # Read Status
        # Check App Valid Status
        # Start App
        # Read Status
        # Check FW_MODE
        # Write drive mode
        # Start polling data (in main loop)
        
        # Validate that the hardware id of the chip is correct
        if not self.check_hardware_id(test):
            raise Exception("Device ID returned is not correct! Please check your wiring.")
        else:
            if test:
                print("Good Hardware")
        
        
        # Get the status so can check things
        self.get_status()
        
        # Check app valid
        if not self._status.APP_VALID:
            raise Exception("App is not valid.")
        else:
            if test:
                print("App is Valid")

        # Try starting the app
        self.app_start(test)

        # Get the status so can check things
        self.get_status(test)
        
        # Check that runnning in the correct mode      
        if not self._status.FW_MODE:
           raise Exception("Device did not enter application mode! If you got here, there may be a problem with the firmware on your sensor.")
        else:
            if test:
                print("Good FW Mode")
        
        #Write drive mode and interrupt to MEAS_MODE
        if test:
            print("Set Drive Mode")
        self.set_drive_mode()
        
        # Get the status so can check things
        self.get_status()
        
        if self._status.ERROR:
            self.get_error()
        
        sleep(2)
        

    def app_start(self, test=False):
        """Put the sensor into low level running mode
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        

        msgs = [CCS811_BOOTLOADER_APP_START]
        self._i2c.msg_write(msgs, test)
        if test:
            print("App Start")
        
    def app_valid(self, test=False):
        """Check the bit flag that the app is valid
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        

        if(self._status.APP_VALID):
                if test:
                    print("App Valid")
                return True
        else:
                if test:
                    print("App Not Valid")
                return False
            
    def get_measure_mode(self, test=False):
        """Set the internal configuration for how measuring will be done 
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        
        
        msgs = [CCS811_MEAS_MODE]
        msgs = self._i2c.msg_read(1, msgs, test)
        print("Measure Mode Register")
        for msg in msgs:
            print("Msg: " + str(msg))
            for d in msg.data:
                print("d: " + str(hex(d)))

    def set_drive_mode(self, test=False):
        """Set the internal frequency for taking measurments
           This is currently coded for 2 seconds
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        
        
#        msgs = [CCS811_MEAS_MODE, CCS811_DRIVE_MODE_1SEC]
        msgs = [CCS811_MEAS_MODE, 0x10]
        self._i2c.msg_write(msgs, test)
        
        
    def get_hwd_id(self, test=False):
        """Get the sensor hardware id
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        
        
        msgs = [CCS811_HW_ID]
        self._i2c.msg_write(msgs, test)
        msgs = self._i2c.msg_read(1, None, test)
        hwd_id = msgs[0].data[0]
        if test:
            print("Hwd Id: " + str(hex(hwd_id)))
        return hwd_id
    
    def get_hwd_version(self, test=False):
        """Read the sensors hardware version
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        
        
        msgs = [CCS811_HW_VERSION]
        self._i2c.msg_write(msgs, test)
        msgs = self._i2c.msg_read(1, None, test)
        hwd_version = msgs[0].data[0]
        if test:
            print("Hwd Version: " + str(hex(hwd_version)))
        return hwd_version
    
    def get_app_version(self, test=False):
        """Read the sensors appliction version
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        
        
        msgs = [CCS811_FW_APP_VERSION]
        self._i2c.msg_write(msgs, test)
        msgs = self._i2c.msg_read(1, None, test)
        app_version = msgs[0].data[0]
        if test:
            print("App Version: " + str(hex(app_version)))
        return app_version
    
    def get_boot_version(self, test=False):
        """Read the sensors boot code version
           Args:
               None
           Returns:
               None
           Raises:
               None
        """        
        
        msgs = [CCS811_FW_BOOT_VERSION]
        self._i2c.msg_write(msgs, test)
        msgs = self._i2c.msg_read(1, None, test)
        boot_version = msgs[0].data[0]
        if test:
            print("Boot Version: " + str(hex(boot_version)))
        return boot_version
    
    
    
    def check_hardware_id(self, test=False):
        """ Read the sensor's hardware version
           Args:
               test
           Returns:
               None
           Raises:
               None
        """        
        
        hwd_id = self.get_hwd_id(test)
        if hwd_id == CCS811_HW_ID_CODE:
            return True
        else:
            return False
        
    def check_error(self, test=False):
      """Get status and check error flag
           Args:
               None
           Returns:
               error status:
           Raises:
               None
      """      
      self.get_status(test)
      return self._status.ERROR
    
    def get_status(self, test=False):
      """Get the error register
           Args:
               None
           Returns:
               None
           Raises:
               None
      """
      msgs = [CCS811_STATUS]
      self._i2c.msg_write(msgs, test)
      msgs = self._i2c.msg_read(1, None, test)
      status = msgs[0].data[0]

      if test:
          print("Get Status CMD: " + str(hex(CCS811_STATUS)))
          for msg in msgs:
              print("Msg: " + str(msg))
              for d in msg.data:
                  print("d: " + str(hex(d)))
      if test:
          print("Status:" + str(hex(status)))
      self._status.set(status)
      if test:
          self.print_status()
      return status
    
    def get_error(self, test=False):
      """Get the error register
           Args:
               None
           Returns:
               None
           Raises:
               None
        Bit  Cause
        7-8  Not used
        5    Heater Supply
        4    Heater Fault
        3    Max Resistance
        2    MeasMode Invalid
        1    Read_Reg Invalid
        0    Msg Invalid
      """
      msgs = self._i2c.msg_read(1, [CCS811_ERROR_ID], test)
      status = msgs[1].data[0]
      if test:
          print("Get Error CMD: " + str(hex(CCS811_ERROR_ID)))
          for msg in msgs:
              print("Msg: " + str(msg))
              for d in msg.data:
                  print("d: " + str(hex(d)))
      if test:
          print("Error:" + str(hex(status)))
      return status
    

    
    def print_status(self):
     """Print dump of status register
           Args:
               None
           Returns:
               None
           Raises:
               None
     """
     print("\nStatus Register")
     print("ERROR: " + str(self._status.ERROR))
     print("Unused: " + str(self._status.unused))
     print("Data Ready: " + str(self._status.DATA_READY))
     print("App_Valid: " + str(self._status.APP_VALID))
     print("Unused 2: " + str(self._status.unused2))
     print("FW Mode: " + str(self._status.FW_MODE))

    def print_error(self):
        """Print dump of error register
           Args:
               None
           Returns:
               None
           Raises:
               None
        """      
        print("\nError Register")
        print("Msg Invalid: " + str(self._error.ERR_MSG_INVALID))
        print("Read Reg Invalid: " + str(self._error.ERR_READ_REG_INVALID))
        print("MeasMode Invalid: " + str(self._error.ERR_MEASMODE_INVALID))
        print("Max Resistance: " + str(self._error.ERR_MAX_RESISTANCE))
        print("Heater Fault: " + str(self._error.ERR_HEATER_FAULT))
        print("Heater Supply: " + str(self._error.ERR_HEATER_SUPPLY))


    def available(self):
        """Check status to see if data is available
           Args:
               None
           Returns:
               True/False: boolean of data availability
           Raises:
               None
        """         

        self.get_status()
        return self._status.DATA_READY
            
    def get_result_data(self, test):
      """Get the result data, convert to word and store in variables
           Args:
               None
           Returns:
               None
           Raises:
               None
      """

      msgs = [CCS811_ALG_RESULT_DATA]
#      self._i2c.msg_write(msgs, test)
      msgs = self._i2c.msg_read(4, msgs, test)
      
      if test:
          for msg in msgs:
              print("Msg: ")
              for d in msg.data:
                  print("d: " + str(hex(d)))
                  
      self._eCO2 = bytesToWord(msgs[1].data[0], msgs[1].data[1])
#      print "CO2", self._eCO2
      self._TVOC = bytesToWord(msgs[1].data[2], msgs[1].data[3])
#      print "TVOC", self._TVOC
      return
    
    def get_co2(self, test=False):
        '''
          Wait for available data, then get value
          Validate data value and return co2
           Args:
               test
           Returns:
               co2
           Raises:
               None          
        '''
        #ccs = CCS811()
        if test:
            print("\nGet CO2")
        while True:
            try:
                if self.available():
                    self.get_result_data(test=False)
                    if 0 < self._eCO2 < 32100:
                        if test:
                            print("CO2: " + str(self._eCO2))
                            print("TVOC: " + str(self._TVOC))
                        return self._eCO2
                    else:
                        if test:
                            print("Bad CO2: " + str(self._eCO2))
            except Exception as e:
                if test:
                    print(str(e))
            sleep(3) 
               
        
    def main(self, test=False):
        '''
          Exercise all functions
           Args:
               test
           Returns:
               None
           Raises:
               None          
        '''
        
        if test:
            print("Test CCS811")
            print("Address: " + str(hex(self._addr)))

        ccs = CCS811()

        if test:
            hwd_id = self.get_hwd_id(test)
    
            if self.check_hardware_id() == True:
                print("Hwd Id: " + str(hwd_id))
            else:
                print("Bad Hwd Id")
            #   print("Get Hwd Id")
            hwd_version = self.get_hwd_version(test)
            print("Hwd Version: " + str(hwd_version))
            #   print("Get Boot Version")
            boot_version = self.get_boot_version(test)
            print("Boot Version: " + str(boot_version))
            #   print("Get App Version")
            app_version = self.get_app_version(test)
            print("App Version: " + str(app_version))
            print("Print Status") 
            self.get_status(test)
            self.print_status()
            print("Print Errors")
            self.get_error(test)
            self.print_error()
            #   ccs.get_measure_mode()
        # Main data loop
        #print("CO2: " + str(self.get_co2()))
        while True:
            self.get_co2(test)
            sleep(3)

def test():
    '''
          Call main to run everything
           Args:
               None
           Returns:
               None
           Raises:
               None          
    '''
    
    ccs = CCS811()
    ccs.main(True)

def master(test=False):
    """Set up sensor in master mode
        Turns the sensor on and starts data polling
        This will likely be continuously running to keep the heater on
           Args:
               None
           Returns:
               None
           Raises:
               None
    """        
    
    CCS811(MASTER, test)
    if test:
        print("Master")
    ccs = CCS811(test)
    while True:
        ccs.get_co2(test)
        sleep(6)
    
def slave(test=False):
    """Code to get data on demand
        This assumes  another code instance is running in MASTER mode
           Args:
               None
           Returns:
               None
           Raises:
               None
    """        
    
    if test:
        print("Slave")
    CCS811(SLAVE, test)
    

if __name__ == "__main__":
    master(True)