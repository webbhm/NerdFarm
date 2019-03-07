"""
 Wrapper of commonly used I2C message functions from periphery

 Author : Howard Webb
 Date   : 06/20/2018
 
"""


from periphery import I2C as pI2C
import time

class I2C(object):

   def __init__(self, path, addr):
      self._path = path
      self._addr = addr
      self._i2c = pI2C(self._path)

   def __exit__(self, exc_type, exc_value, traceback):
      self._i2c.close()

   def msg_write(self, cmds, test=False):
       """Write to sensor
           Args:
               cmds: commands to send
           Returns:
               msgs: basically returns the cmds, since nothing altered
           Raises:
               None
      """
#       print("Msg Write")
#       for cmd in cmds:
#           print(str(cmd))
       msgs = [self._i2c.Message(cmds)]
       try:
           self._i2c.transfer(self._addr, msgs)
   #        msb = msgs[0].data[0]
   #        print "MSB", hex(msb)
   #        return msgs

       except Exception as e:
           print(str(e))
           return None

   def msg_read(self, size, cmds=None, test=False):
       """Read existing data
           Args:
               cmds: addresses to read from - optional for some sensors (SI7021)
               size: size of byte array for receiving data
           Returns:
               msgs: message package, last one should hold data
           Raises:
               None
      """
           
#       print("Msg Read - cmd " + str(cmds))
#       print("Msg Read = size " + str(size))
   #    print "Msg Read", size
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
           print(str(e))
           return None    


   def get_data(self, cmd, sleep, size, read=None, test=False):
       '''Combine sending of command and reading
        Some sensors default the read to the prior command and don't specify a read address
       ''' 
       self.msg_write(cmd)
       time.sleep(sleep)
       msgs = self.msg_read(size, read)
       if msgs == None:
           return None
       else:
#           for msg in msgs:
#               print("-")
#               for dt in msg.data:
#                   print("Dt " + str(dt))
#           print("Data " + str(msgs[0].data[0]) + " " + str(msgs[0].data[1]))
           value = bytesToWord(msgs[0].data[0], msgs[0].data[1])
           return msgs
        

def bytesToWord(high, low, test=False):
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
   word = (high << 8) + low
   return word


