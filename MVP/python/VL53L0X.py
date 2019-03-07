# Author: Howard Webb
# Date: 7/26/2017
# Designed for the VL53L0X time-of-flight laser distance chip, using an I2C bus

import smbus
import time

VL53L0X_REG_IDENTIFICATION_MODEL_ID		= 0x00c0
VL53L0X_REG_IDENTIFICATION_REVISION_ID		= 0x00c2
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD	= 0x0050
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD	= 0x0070
VL53L0X_REG_SYSRANGE_START			= 0x000

VL53L0X_REG_RESULT_INTERRUPT_STATUS 		= 0x0013
VL53L0X_REG_RESULT_RANGE_STATUS 		= 0x0014
address = 0x29


def VL53L0X_decode_vcsel_period(vcsel_period_reg):
# Converts the encoded VCSEL period register value into the real
# period in PLL clocks
    vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
    return vcsel_period_pclks;

# Get I2C bus
class VL53L0X:

    address = 0x29
    
    def __init__(self):
        '''Initialize the object'''
        self.rev = self.getRevision()
        self.id = self.getId()
        

    def makeuint16(self, lsb, msb):
        return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

    def getDistance(self):
        ''' Build in error checking for null value returned
        retry if get bad value up to five times '''
        self.measureDistance()
        for x in range(0,5):
            dist=self.measureDistance()
            if dist>20:
                return dist
            

    def measureDistance(self):
        ''' Actual call to get distance '''
        bus = smbus.SMBus(1)
        val1 = bus.write_byte_data(address, VL53L0X_REG_SYSRANGE_START, 0x01)

        cnt = 0
        while (cnt < 100): # 1 second waiting time max
                time.sleep(0.010)
                val = bus.read_byte_data(address, VL53L0X_REG_RESULT_RANGE_STATUS)
                # print(val)
                if (val & 0x01):
                        break
                cnt += 1
        if not (val & 0x01):
                print "not ready"
                # Throw error

        data = bus.read_i2c_block_data(address, 0x14, 12)
        distance = int(str(self.makeuint16(data[11], data[10])))
        return distance

    def getRevision(self):
        bus = smbus.SMBus(1)
        return bus.read_byte_data(address, VL53L0X_REG_IDENTIFICATION_REVISION_ID)    

    def getId(self):
        bus = smbus.SMBus(1)
        return bus.read_byte_data(address, VL53L0X_REG_IDENTIFICATION_MODEL_ID)

    def preRange(self):
        bus = smbus.SMBus(1)
        return bus.read_byte_data(address, VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)    

    def finalRange(self):
        bus = smbus.SMBus(1)
        return bus.read_byte_data(address, VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD)

    def test(self):
        'Self test of the object'
        print('\n*** Test VL53LOX ***\n')
        print("Revision ID: " + str(self.rev))
        print("Revision ID (hex): " + hex(self.getRevision()))
        print("Device ID: " + str(self.id))
        print("Device ID (hex): " + hex(self.getId()))
        val1 = self.preRange()
        decd = VL53L0X_decode_vcsel_period(val1)
        print("Pre-Range Config Period: " + hex(val1) + " decode: " + str(decd))


        val2 = self.finalRange()
        decd2 = VL53L0X_decode_vcsel_period(val2)
        print("Final Range Config Period: " + hex(val2) + " decode: " + str(decd2))

        for x in range(1, 10):
            print('Distance : %i' %self.getDistance())

        
if __name__=="__main__":
    s=VL53L0X()
    s.test()

