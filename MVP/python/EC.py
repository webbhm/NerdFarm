'''
# Get elecrical conductivity (moisture probe) from ADC
# The analog moisture probe is hooked to pin1 of the analog to digital converter
# The ADC is running on the I2C bus
# Howard Webb
# 2019/08/16

 Out of water reads about 30000
 Just touching is about 28000 or lower
 The deeper it is submerged, the lower the value
 There is a good bit of drift when it is sitting
'''

import time
# Import the ADS1x15 module (analog to digital converter).
from ADS1115 import ADS1115
from LogUtil import Logger

class EC(object):
    
   GAIN = 1    

   def __init__(self, logger=None):
      self._pin = 0 # ADS1115 Channel to use
      self._logger = logger
      if logger == None:
          self._logger = Logger("EC", Logger.INFO)
      # Create an ADS1115 ADC (16-bit) instance.
      self._adc = ADS1115(logger)      

   def getEC(self):
      """Read the sensor value
           Args:
               None
           Returns:
               EC value as number between 0 and 32,000
           Raises:
               None
      """
       
      return self._adc.read_adc(self._pin, gain=self.GAIN)

def validate():
    ec = EC()
    ec._logger.info(ec.getEC())

def test():
    ec = EC()
    while True:
        print("EC: " + str(ec.getEC()))
        time.sleep(0.5)
        
if __name__ == "__main__":
    test()
