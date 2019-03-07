#simple bitfield object taken from Adafruit
from collections import OrderedDict

class bitfield(object):
	def __init__(self, _structure):
		self._structure = OrderedDict(_structure)

		for key, value in self._structure.items():
			setattr(self, key, 0)

	def get(self):
		fullreg = 0
		pos = 0
		for key, value in self._structure.items():
			fullreg = fullreg | ( (getattr(self, key) & (2**value - 1)) << pos )
			pos = pos + value

		return fullreg

	def set(self, data):
		pos = 0
		for key, value in self._structure.items():
			setattr(self, key, (data >> pos) & (2**value - 1))
			pos = pos + value

def test():
     status = bitfield([('ERROR' , 1), ('unused', 2), ('DATA_READY' , 1), ('APP_VALID', 1), ('unused2' , 2), ('FW_MODE' , 1)])

     print_status(status)
     "ERROR", status.ERROR

     status.set(0xff)

     print_status(status)

def print_status(status):
     print("ERROR: " + str(status.ERROR))
     print("Unused: " + str(status.unused))
     print("Data Ready: " + str(status.DATA_READY))
     print("App_Valid: " + str(status.APP_VALID))
     print("Unused 2: " + str(status.unused2))
     print("FW Mode: " + str(status.FW_MODE))
    

    
if __name__ == "__main__":
    test()
