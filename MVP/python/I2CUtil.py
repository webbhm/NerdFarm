"""
 Wrapper of commonly used I2C message functions from periphery

 Author : Howard Webb
 Date   : 06/20/2018
 
"""


from periphery import I2C as pI2C
import time
from LogUtil import Logger

class I2C(object):

   def __init__(self, path, addr, logger=None):
      self._path = path
      self._addr = addr
      self._i2c = pI2C(self._path)
      self._logger = logger
      if logger == None:
         self._logger = Logger("SCD30", Logger.INFO)
      self._logger.debug("initialize I2C object")        
      

   def __exit__(self, exc_type, exc_value, traceback):
      self._i2c.close()

   def msg_write(self, cmds):
       """Write to sensor
           Args:
               cmds: commands to send
           Returns:
               msgs: basically returns the cmds, since nothing altered
           Raises:
               None
      """
       self._logger.debug("In Msg Write")
       for cmd in cmds:
           self._logger.detail("{}, {}".format("Cmd: ", cmd))

       msgs = [self._i2c.Message(cmds)]
       try:
           self._logger.detail("Transfer")
           self._i2c.transfer(self._addr, msgs)
           msb = msgs[0].data[0]
           self._logger.detail("{}, {}".format("MSB: ", hex(msb)))
           return msgs

       except Exception as e:
           self._logger.error(str(e))
           return None

   def msg_read(self, size, cmds=None):
       """Read existing data
           Args:
               cmds: addresses to read from - optional for some sensors (SI7021)
               size: size of byte array for receiving data
           Returns:
               msgs: message package, last one should hold data
           Raises:
               None
      """
           
       self._logger.detail("{}, {}, {}, {}".format("Msg Read - size: ", size, " cmds: ", cmds))
       sz = self._i2c.Message(bytearray([0x00 for x in range(size)]), read=True)
       msgs = [sz]
#       print("C " + str(type(cmds)))
       if cmds is not None:
#           print("Cmds " + str(cmds))
           rd = self._i2c.Message(cmds)
           msgs = [rd, sz]
       try:
           self._i2c.transfer(self._addr, msgs)
           return msgs 

       except Exception as e:
           self._logger.error(str(e))
           return None    


   def get_data(self, cmd, sleep, size, read=None):
       '''Combine sending of command and reading
        Some sensors default the read to the prior command and don't specify a read address
       '''
       self._logger.debug("{}, {}, {}, {}, {}, {}".format("In Get Data-cmd: ", cmd, " sleep: ", sleep, " size: ", size))          
       self.msg_write(cmd)
       time.sleep(sleep)
       msgs = self.msg_read(size, read)
       if msgs == None:
           return None
       else:
           for msg in msgs:
               self._logger.detail("-")
               for dt in msg.data:
                   self._logger.detail("Dt " + str(dt))
           self._logger.debug("Data " + str(msgs[0].data[0]) + " " + str(msgs[0].data[1]))
           value = self.bytesToWord(msgs[0].data[0], msgs[0].data[1])
           return msgs
        

   def bytesToWord(self, high, low):
       """Convert two byte buffers into a single word value
           shift the first byte into the work high position
           then add the low byte
            Args:
                high: byte to move to high position of word
                low: byte to place in low position of word
            Returns:
                word: the final value
            Raises:
                None
       """
       self._logger.debug("{}, {}, {}, {}".format("In Bytes To Word-high: ", high, " Low: ", low))   
       word = (high << 8) + low
       return word


