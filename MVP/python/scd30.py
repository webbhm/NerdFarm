'''
SCD30 Sensirion C02 sensor with temperature and relative humidity
Arthur: Howard Webb
Data: 2019/02/12

Specifications are at:
https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.5_CO2/Sensirion_CO2_Sensors_SCD30_Interface_Description.pdf

Full CRC checks have not been implemented at this time
Base data collection is working, other functions may be incomplete or missing
'''
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Not fully implemented yet
# They may be bugs even in the functions with the comment 'WOKRS!'

from I2CUtil import I2C, bytesToWord
import numpy
import time

path = "/dev/i2c-1"
addr = 0x61

class SCD30:
    CMD_START_PERIODIC_MEASUREMENT = 0x0010
    CMD_STOP_PERIODIC_MEASUREMENT = 0x0104
    CMD_READ_MEASUREMENT = 0x0300
    CMD_GET_DATA_READY = 0x0202
    CMD_SET_MEASUREMENT_INTERVAL = 0x4600
    CMD_SET_TEMPERATURE_OFFSET = 0x5403
    CMD_SET_ALTITUDE = 0x5102

    WORD_LEN = 2
    COMMAND_LEN = 2
    MAX_BUFFER_WORDS = 24

    STATUS_FAIL = 1
    STATUS_OK = 0

    CO2_DATA_INDEX = 0
    TEMP_DATA_INDEX = 1
    HUMIDITY_DATA_INDEX = 2

    def __init__(self, test=False):
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
        self.start_periodic_measurement(test)
        

    
    def start_periodic_measurement(self, test):
        """Start sensor to generate data (about every 2 seconds
           Args:
               self:
               test: flag for test logic
           Returns:
               None
           Raises:
               None
        """        

        # command 0x0010, altitude 0x03eb, crc_check 0x87
        # altitude set to 1003 mb
        #msgs = [0x00,0x10, 0x03, 0xeb, 0x87]
        # Altitude is currently set to 0
        msgs = [0x00,0x10, 0x00, 0x00, 0x81]
        self._i2c.msg_write(msgs, test)                

    # TESTE ADN WORKS!
    def stop_periodic_measurement(self):
        """Stop automatic data gathering
           Args:
               None
           Returns:
               None
           Raises:
               None
        """        
        msgs = [0x01,0x14]
        self._i2c.msg_write(msgs, test)                
        
#        return self._i2c.msg_write(self.CMD_STOP_PERIODIC_MEASUREMENT
        pass


    def read_measurement(self, test=False):
        """Read data
           Args:
               self:
               test:
           Returns:
               CO2
               Temp
               Relative Humidity
           Raises:
               None
        """        
        self._i2c.msg_write([0x03, 0x00])
        if test:
            print("Read Measurement")
        msgs = self._i2c.msg_read(18)
        
        data3 = self.bytes_to_value(msgs[0].data, test)                    
        return data3[self.CO2_DATA_INDEX], data3[self.TEMP_DATA_INDEX], data3[self.HUMIDITY_DATA_INDEX]

    def bytes_to_value(self, byte_array, test=False):
        """Convert array of byte values into three float values
           Args:
               self
               byte_array: array of data from I2C sensor
               test
           Returns:
               data: array of float values (CO2, Temp, RH)
           Raises:
               None
        """        
        
        # Array for value bytes (exclude crc check byte)
        bytes_buf = [0]*12 # 2 words for each co2, temperature, humidity
        l = len(bytes_buf)
        ld = len(byte_array)
        # array for word conversion - two words per value
        word_buf = [0]*int(l/2)
        # final data structure - one place per value
        data = [0]*int(len(word_buf)/2)

        # Load bytes_buffer, strip crc bytes
        y = 0
        for x in range(0, ld, 6):
#            print("x: " + str(x) + " y: " + str(y))
            bytes_buf[y] = byte_array[x]
            bytes_buf[y+1] = byte_array[x+1]
            bytes_buf[y+2] = byte_array[x+3]
            bytes_buf[y+3] = byte_array[x+4]            
            y += 4
        if test:
            print ("bytes_buf: " + str(bytes_buf))
        
        # Convert sensor data reads to physical value per Sensirion specification
        # Load buffer with values
        # Cast 4 bytes to one unsigned 32 bit integer
        # Cast unsigned 32 bit integer to 32 bit float

        # Convert bytes to words
        for i in range(len(word_buf)):
            word_buf[i] = (bytes_buf[i*2] << 8) | bytes_buf[i*2+1]
            if test:
                print(str(hex(bytes_buf[i])) + " " + str(hex(bytes_buf[i+1])))
                print(hex(word_buf[i]))

        #convert words to int32
        data[self.CO2_DATA_INDEX] = (word_buf[0] << 16) | word_buf[1]
        data[self.TEMP_DATA_INDEX] = (word_buf[2] << 16) | word_buf[3]
        data[self.HUMIDITY_DATA_INDEX] = (word_buf[4] << 16) | word_buf[5]

        #Convert int32 data to float32
        floatData = numpy.array(data, dtype=numpy.int32)
        data = floatData.view('float32')

        if test:
            print("CO2: " + str(data[self.CO2_DATA_INDEX]))
            print("Temp: " + str(data[self.TEMP_DATA_INDEX]))
            print("RH: " + str(data[self.HUMIDITY_DATA_INDEX]))

        return data
        
        

    # interval : (u16 integer)
    def set_measurement_interval(self, interval_sec, test=False):
        """Set frequency of automatic data collectoin
           Args:
               self
               interval_sec: time in seconds
               test
           Returns:
               None
           Raises:
               None
        """          
        if interval_sec < 2 or interval_sec > 1800:
            return self.STATUS_FAIL
# Need to finish this so value is 32 word split to two 16 words
# Calculate crc value for last word
        # [Cmd MSB, Cmd LSB, Interval MSB, Interval LSB, CRC]
        # msb, lsb = convert_word(interval_sec, test)
        # crc = calc_crc(msb, lsb, test)
        # msg = [0x46,0x10, msb, lsb, crc]
        msgs = [0x46,0x10, 0x00, 0x02, 0xE3]
        self._i2c.msg_write(msgs, test)                


    def get_data_ready(self, test=False):
        """Check if have fresh data from periodic update
           Args:
               self
               test
           Returns:
               ready flag
           Raises:
               None
        """          
        
        self._i2c.msg_write([0x02, 0x02])
        msgs = self._i2c.msg_read(3)        
        if test:
            for msg in msgs:
                print("Msg: " + str(msg))
                for d in msg.data:
                    print("Data: " + str(hex(d)))
        return msgs[0].data[1]
    
    # Strange behaviour
    def set_temperature_offset(self, temperature_offset):
        """Temperature compensation offset
           Args:
               self
               temperature offset
               test
           Returns:
               None
           Raises:
               None
        """          
        
# Need to finish this so value is 32 word split to two 16 words
# Calculate crc value for last word
        # [Cmd MSB, Cmd LSB, Interval MSB, Interval LSB, CRC]
        # msb, lsb = convert_word(interval_sec, test)
        # crc = calc_crc(msb, lsb, test)
        # msg = [0x54,0x03, msb, lsb, crc]
        msgs = [0x54,0x03, 0x00, 0x02, 0xE3]
        self._i2c.msg_write(msgs, test)                 


    # TESTE ADN WORKS!
    def set_altitude(self, altitude, test=False):
        """Altitude compensation 
           Args:
               self
               altitude: uint16, height over sea level in [m] above 0
               test
           Returns:
               None
           Raises:
               None
        """          
        
# Need to finish this so value is 32 word split to two 16 words
# Calculate crc value for last word
        # [Cmd MSB, Cmd LSB, Interval MSB, Interval LSB, CRC]
        # msb, lsb = convert_word(interval_sec, test)
        # crc = calc_crc(msb, lsb, test)
        # msg = [0x51,0x02, msb, lsb, crc]
        msgs = [0x51,0x02, 0x00, 0x02, 0xE3]
        self._i2c.msg_write(msgs, test)                 

    # TESTE ADN WORKS!
    def get_configured_address(self, test=False):
        """Altitude compensation 
           Args:
               self
               test
           Returns:
               self._addr: address of the sensor
           Raises:
               None
        """                  
        return self._addr
    
    def get_data(self, test=False):
        """High level logic to simply get data
           Args:
               self
               test
           Returns:
               co2: co2 value
               temp: temperature value
               rh: relative humidity value
           Raises:
               NameError: if error in logic (I2C Problem)
        """                  
        for x in range(0, 4): # Only give four reste tries before giving up
            try:
                while True:
                    # Test if data is ready
                    if self.get_data_ready(test):
                       # fetch data 
                       co2, temp, rh = self.read_measurement(test)
                       if test:
                           print("CO2: " + str(co2))
                           print("Temp: " + str(temp))
                           print("RH: " + str(rh))
                       return co2, temp, rh
                    time.sleep(1)
            # try reset to see if can recover from errors
            except Exception as e:
                print(str(e))
                self.__init__()
                time.sleep(2)
        # Give up if cannot fix the problems
        raise NameError("Too Many Failures")                        
                
        

def test():
   """Test script to exercise the code
           Args:
               None
           Returns:
               None
           Raises:
               None
   """        
   print("Test SCD30")
   # Set this to True for full info dump
   test = False

   scd = SCD30(test)
   print("Get Address")
   print(str(scd.get_configured_address()))
   print("Get Data")
   try:
       while True:
           print("\n")
           co2, temp, rh = scd.get_data(test)
           print("CO2: " + str(co2))
           print("Temp: " + str(temp))
           print("RH: " + str(rh))
       else:
           print("No data available")
       # Give time for periodic check to reset 
       time.sleep(3)
   except Exception as e:
        print(str(e))

if __name__ == "__main__":
    test()
    
