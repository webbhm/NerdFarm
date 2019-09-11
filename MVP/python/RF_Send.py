from rpi_rf import RFDevice
from LogUtil import Logger
import time

'''
Pulse: 444
Protocol: 1

#1 On: 9434117
#1 Off: 9434125

#2 On: 9434115
#2 Off: 9434123

#3 On: 9434121
#3 Off: 9434113
'''

code = {1:{'On':9434117, 'Off':9434125},2:{'On':9434115, 'Off':9434123},3:{'On':9434121, 'Off':9434113}}
protocol = 1
length = 444

class RF_Sender:
    
    def __init__(self, logger = None, pin = 11):
        self._pin = pin
        self._protocol = 1
        self._length = 444
        self._logger = logger
        if self._logger == None:
            self._logger = Logger('RF_Send', Logger.INFO)
        self._logger.debug("Initialize RF Sender on channel {}".format(pin))
        self._rfdevice = RFDevice(pin)
        self._rfdevice.enable_tx()
    

    def send(self, code, protocol, length):
        self._rfdevice.tx_code(code, protocol, length)
        print("TX Pin: {}, Code: {}, Protocol: {}, Length: {}".format(self._pin, code, protocol, length))
        
    def set_on(self, pin):
        self.send(code[pin]['On'], protocol, length)        
        
    def set_off(self, pin):
        self.send(code[pin]['Off'], protocol, length)        

    def cleanup(self):
        self._rfdevice.cleanup()

def test():
    print("RX Test")
    send = RF_Sender()
    protocol = 1
    length = 444
    for x in range(1, 4):
        print(x, 'On', code[x]['On'])
        send.send(code[x]['On'], protocol, length)
        time.sleep(1)
    time.sleep(3)        
    for x in range(1, 4):
        print(x, 'Off', code[x]['Off'])
        send.send(code[x]['Off'], protocol, length)
        time.sleep(1)
    send.cleanup()
    print("Done")
    
if __name__ == "__main__":
    test()        