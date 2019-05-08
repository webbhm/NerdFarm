# Author: Howard Webb
# Date: 2019-01-23
#
# This is a stripped down version of the Adafruit code re-written to use python-periphery
# It is limited to the needs of MarsFarm and the EC sensor at this time.

# python-periphery is used instead of sbus for better compatability Python3 and with Raspberry Pi
# If you are wanting flexibility and more features, use the Adafruit code
# https://github.com/adafruit/Adafruit_Python_ADS1X15
# or feel free to write more features for this code.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
from LogUtil import Logger

# Register and other configuration values:
ADS1x15_DEFAULT_ADDRESS        = 0x48
ADS1x15_POINTER_CONVERSION     = 0x00
ADS1x15_POINTER_CONFIG         = 0x01
ADS1x15_CONFIG_OS_SINGLE       = 0x8000
ADS1x15_CONFIG_MUX_OFFSET      = 12
# Maping of gain values to config register values.
ADS1x15_CONFIG_GAIN = {
    2/3: 0x0000,
    1:   0x0200,
    2:   0x0400,
    4:   0x0600,
    8:   0x0800,
    16:  0x0A00
}
ADS1x15_CONFIG_MODE_SINGLE      = 0x0100
# Mapping of data/sample rate to config register values for ADS1115 (slower).
ADS1115_CONFIG_DR = {
    8:    0x0000,
    16:   0x0020,
    32:   0x0040,
    64:   0x0060,
    128:  0x0080,
    250:  0x00A0,
    475:  0x00C0,
    860:  0x00E0
}
ADS1x15_CONFIG_COMP_QUE_DISABLE = 0x0003

PATH = "/dev/i2c-1"

from I2CUtil import I2C

class ADS1115(object):
    
    def __init__(self, logger=None):

        self._logger = logger
        if logger == None:
            self._logger = Logger("ADS1115", Logger.INFO, file="/home/pi/MVP/logs/obsv.log")
        self._path = PATH
        self._addr = ADS1x15_DEFAULT_ADDRESS
        self._i2c = I2C(self._path, self._addr, self._logger)
        self._logger.debug("Initialize ADS1115")
        
        
    def read_adc(self, channel, gain=1, data_rate=None):
        """High level read function for the ADC
         Read a single ADC channel and return the ADC value as a signed integer
         result.  Channel must be a value within 0-3.
         Calls the lower level read function
         Basically configures the parameters 
           Args:
               channel: which of the 4 I2C options to use
               gain: how much to multiply the reading
               data_rate: speed to collect data
           Returns:
               EC value as number between 0 and 32,000
           Raises:
               None
        """        
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Perform a single shot read and set the mux value to the channel plus
        # the highest bit (bit 3) set.
        value = self.read(channel + 0x04, gain, data_rate, ADS1x15_CONFIG_MODE_SINGLE)
        self._logger.info("{}: {}, {}: {}".format("Channel", channel, "Value", value))
        return value

    def read(self, mux, gain, data_rate, mode):
        """Perform an ADC read with the provided mux, gain, data_rate, and mode
        values.  Returns the signed integer result of the read.
           Args:
               mux: channel converted to chip address
               gain: how much to multiply the reading
               data_rate: speed to collect data
           Returns:
               EC value as number between 0 and 32,000
           Raises:
               None

        """
        # Build compound byte structure of configuration dta
        config = ADS1x15_CONFIG_OS_SINGLE  # Go out of power-down mode for conversion.
        # Specify mux value.
        config |= (mux & 0x07) << ADS1x15_CONFIG_MUX_OFFSET
        # Validate the passed in gain and then set it in the config.
        if gain not in ADS1x15_CONFIG_GAIN:
            raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
        config |= ADS1x15_CONFIG_GAIN[gain]
        # Set the mode (continuous or single shot).
        config |= mode
        # Get the default data rate if none is specified (default differs between
        # ADS1015 and ADS1115).
        if data_rate is None:
            data_rate = self.data_rate_default()
        # Set the data rate (this is controlled by the subclass as it differs
        # between ADS1015 and ADS1115).
        config |= self.data_rate_config(data_rate)
        config |= ADS1x15_CONFIG_COMP_QUE_DISABLE  # Disble comparator mode.

        # Send the config value to start the ADC conversion.
        # Explicitly break the 16-bit value down to a big endian pair of bytes.
        # Command is: write address, config part 1, config part 2
        cmds = [ADS1x15_POINTER_CONFIG, (config >> 8) & 0xFF, config & 0xFF]
        self._i2c.msg_write(cmds)
        
#        print("Sleep")
        # Wait for the ADC sample to finish based on the sample rate plus a
        # small offset to be sure (0.1 millisecond).
        time.sleep(1.0/data_rate+0.0001)

# Retrieve the result.
        # Message is: read address, read buffer of size
        cmds = [ADS1x15_POINTER_CONVERSION]
        size = 2
        ms2 = self._i2c.msg_read(size, cmds)
# Convert bytes to Word structure        
        full = self._i2c.bytesToWord(ms2[1].data[0], ms2[1].data[1])
        return full
 
    def data_rate_default(self):
        # Default from datasheet page 16, config register DR bit default.
        return 128
    
    def data_rate_config(self, data_rate):
        if data_rate not in ADS1115_CONFIG_DR:
            raise ValueError('Data rate must be one of: 8, 16, 32, 64, 128, 250, 475, 860')
        return ADS1115_CONFIG_DR[data_rate]    

def test():
   """Loop data collection
        Args:
            None
        Returns:
            None
        Raises:
            None
   """
   print("Test ADS1115")
   channel = 0
   gain=1
   data_rate = None    
   adc = ADS1115()
   print("ADS1115")
   while True:
       print("\n")
       for channel in range(0, 4):
           value = adc.read_adc(channel, gain, data_rate)
           print("{}: {}, {}: {}".format("Channel", channel, "Value", value))
       time.sleep(5)
   
def validate():
    """Exercise all the ADS1115 functions
        Args:
            None
        Returns:
            None
        Raises:
            None
    """
    
    print("Validate ADC")
    channel = 0
    gain=1
    data_rate = None    
    adc = ADS1115()
    value = adc.read_adc(channel, gain, data_rate)
    print("Value " + str(value))
    
if __name__=="__main__":
    test()            
    
    

