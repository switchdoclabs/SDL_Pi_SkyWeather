'''
This code is basically an adaptation of the Arduino_TSL2591 library from 
adafruit: https://github.com/adafruit/Adafruit_TSL2591_Library

for configuring I2C in a raspberry 
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

datasheet: 
http://ams.com/eng/Products/Light-Sensors/Light-to-Digital-Sensors/TSL25911

'''
import smbus
import time

VISIBLE = 2  # channel 0 - channel 1
INFRARED = 1  # channel 1
FULLSPECTRUM = 0  # channel 0

ADDR = 0x29
READBIT = 0x01
COMMAND_BIT = 0xA0  # bits 7 and 5 for 'command normal'
CLEAR_BIT = 0x40  # Clears any pending interrupt (write 1 to clear)
WORD_BIT = 0x20  # 1 = read/write word (rather than byte)
BLOCK_BIT = 0x10  # 1 = using block read/write
ENABLE_POWERON = 0x01
ENABLE_POWEROFF = 0x00
ENABLE_AEN = 0x02
ENABLE_AIEN = 0x10
CONTROL_RESET = 0x80
LUX_DF = 408.0
LUX_COEFB = 1.64  # CH0 coefficient
LUX_COEFC = 0.59  # CH1 coefficient A
LUX_COEFD = 0.86  # CH2 coefficient B

REGISTER_ENABLE = 0x00
REGISTER_CONTROL = 0x01
REGISTER_THRESHHOLDL_LOW = 0x02
REGISTER_THRESHHOLDL_HIGH = 0x03
REGISTER_THRESHHOLDH_LOW = 0x04
REGISTER_THRESHHOLDH_HIGH = 0x05
REGISTER_INTERRUPT = 0x06
REGISTER_CRC = 0x08
REGISTER_ID = 0x0A
REGISTER_CHAN0_LOW = 0x14
REGISTER_CHAN0_HIGH = 0x15
REGISTER_CHAN1_LOW = 0x16
REGISTER_CHAN1_HIGH = 0x17
INTEGRATIONTIME_100MS = 0x00
INTEGRATIONTIME_200MS = 0x01
INTEGRATIONTIME_300MS = 0x02
INTEGRATIONTIME_400MS = 0x03
INTEGRATIONTIME_500MS = 0x04
INTEGRATIONTIME_600MS = 0x05

GAIN_LOW = 0x00  # low gain (1x)
GAIN_MED = 0x10  # medium gain (25x)
GAIN_HIGH = 0x20  # medium gain (428x)
GAIN_MAX = 0x30  # max gain (9876x)


class Tsl2591(object):
    def __init__(
                 self,
                 i2c_bus=1,
                 sensor_address=0x29,
                 integration=INTEGRATIONTIME_100MS,
                 gain=GAIN_LOW
                 ):
        self.bus = smbus.SMBus(i2c_bus)
        self.sendor_address = sensor_address
        self.integration_time = integration
        self.gain = gain
        self.set_timing(self.integration_time)
        self.set_gain(self.gain)
        self.disable()  # to be sure

    def set_timing(self, integration):
        self.enable()
        self.integration_time = integration
        self.bus.write_byte_data(
                    self.sendor_address,
                    COMMAND_BIT | REGISTER_CONTROL,
                    self.integration_time | self.gain
                    )
        self.disable()

    def get_timing(self):
        return self.integration_time

    def set_gain(self, gain):
        self.enable()
        self.gain = gain
        self.bus.write_byte_data(
                    self.sendor_address,
                    COMMAND_BIT | REGISTER_CONTROL,
                    self.integration_time | self.gain
                    )
        self.disable()

    def get_gain(self):
        return self.gain

    def calculate_lux(self, full, ir):
        # Check for overflow conditions first
        if (full == 0xFFFF) | (ir == 0xFFFF):
            return 0
            
        case_integ = {
            INTEGRATIONTIME_100MS: 100.,
            INTEGRATIONTIME_200MS: 200.,
            INTEGRATIONTIME_300MS: 300.,
            INTEGRATIONTIME_400MS: 400.,
            INTEGRATIONTIME_500MS: 500.,
            INTEGRATIONTIME_600MS: 600.,
            }
        if self.integration_time in case_integ.keys():
            atime = case_integ[self.integration_time]
        else:
            atime = 100.

        case_gain = {
            GAIN_LOW: 1.,
            GAIN_MED: 25.,
            GAIN_HIGH: 428.,
            GAIN_MAX: 9876.,
            }

        if self.gain in case_gain.keys():
            again = case_gain[self.gain]
        else:
            again = 1.

        # cpl = (ATIME * AGAIN) / DF
        cpl = (atime * again) / LUX_DF
        lux1 = (full - (LUX_COEFB * ir)) / cpl

        lux2 = ((LUX_COEFC * full) - (LUX_COEFD * ir)) / cpl

        # The highest value is the approximate lux equivalent
        return max([lux1, lux2])

    def enable(self):
        self.bus.write_byte_data(
                    self.sendor_address,
                    COMMAND_BIT | REGISTER_ENABLE,
                    ENABLE_POWERON | ENABLE_AEN | ENABLE_AIEN
                    )  # Enable

    def disable(self):
        self.bus.write_byte_data(
                    self.sendor_address,
                    COMMAND_BIT | REGISTER_ENABLE,
                    ENABLE_POWEROFF
                    )

    def get_full_luminosity(self):
        self.enable()
        time.sleep(0.120*self.integration_time+1)  # not sure if we need it "// Wait x ms for ADC to complete"
        full = self.bus.read_word_data(
                    self.sendor_address, COMMAND_BIT | REGISTER_CHAN0_LOW
                    )
        ir = self.bus.read_word_data(
                    self.sendor_address, COMMAND_BIT | REGISTER_CHAN1_LOW
                    )                    
        self.disable()
        return full, ir

    def get_luminosity(self, channel):
        full, ir = self.get_full_luminosity()
        if channel == FULLSPECTRUM:
            # Reads two byte value from channel 0 (visible + infrared)
            return full
        elif channel == INFRARED:
            # Reads two byte value from channel 1 (infrared)
            return ir
        elif channel == VISIBLE:
            # Reads all and subtracts out ir to give just the visible!
            return full - ir
        else: # unknown channel!
            return 0


if __name__ == '__main__':

    tsl = Tsl2591()  # initialize
    full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
    lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
    print (lux, full, ir)
    print ()

    def test(int_time=INTEGRATIONTIME_100MS, gain=GAIN_LOW):
        tsl.set_gain(gain)
        tsl.set_timing(int_time)
        full_test, ir_test = tsl.get_full_luminosity()
        lux_test = tsl.calculate_lux(full_test, ir_test)
        print ('Lux = %f  full = %i  ir = %i' % (lux_test, full_test, ir_test))
        print("integration time = %i" % tsl.get_timing())
        print("gain = %i \n" % tsl.get_gain())        

    for i in [INTEGRATIONTIME_100MS,
              INTEGRATIONTIME_200MS,
              INTEGRATIONTIME_300MS,
              INTEGRATIONTIME_400MS,
              INTEGRATIONTIME_500MS,
              INTEGRATIONTIME_600MS]:
        test(i, GAIN_LOW)

    for i in [GAIN_LOW,
              GAIN_MED,
              GAIN_HIGH,
              GAIN_MAX]:
        test(INTEGRATIONTIME_100MS, i)
