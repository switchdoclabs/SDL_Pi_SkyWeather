#!usr/bin/python 
# SwitchDoc Labs, 2019
# added more reliablity functions including GrovePower Save


# MODULE IMPORTS
import time

import smbus

import traceback
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# GLOBAL VARIABLES
SHT30_I2CADDR = 0x44
SHT30_READCOMMAND = 0x2C
SHT30_READREG = 0x00
MAXREADATTEMPT = 10
SHT30_POLYNOMIAL = 0x131  # P(x) = x^8 + x^5 + x^4 + 1 = 100110001

SHT30DEBUG = False

class SHT30:
    """Base functionality for SHT30 humidity and temperature sensor. """

    def __init__(self, address=SHT30_I2CADDR, i2c=None, powerpin=0, **kwargs):

        i2c = smbus.SMBus(1)
        self.powerpin = powerpin
        # for Grove PowerSave
        if (self.powerpin <> 0):
            GPIO.setup(self.powerpin, GPIO.OUT)
            GPIO.output(self.powerpin, True)
            time.sleep(1.0)

        self._device = i2c 
        self.humidity = 0
        self.temperature = 0
        self.crcT = 0
        self.crcH = 0
        self.SHT30PreviousTemp = -1000
        self.goodreads = 0
        self.badreadings = 0
        self.badcrcs = 0
        self.retrys = 0
        self.powercycles = 0

    def powerCycleSHT30(self):
        if (SHT30DEBUG == True):
            print ("power cycling SHT30")
        GPIO.output(self.powerpin, False)
        time.sleep(10.50)
        GPIO.output(self.powerpin, True)
        time.sleep(1.50)
        self.powercycles += 1
    
    def verify_crc(self, data):
        crc = 0xff
        for byte in data:
            crc ^= byte
            for _ in range(8):
                 if crc & 0x80:
                    crc <<= 1
                    crc ^= SHT30_POLYNOMIAL
                 else:
                    crc <<= 1
        return crc



    # fast read for device detection without faults
    def _fast_read_data(self):   

        
        # TELL THE DEVICE WE WANT 4 BYTES OF DATA
        self._device.write_i2c_block_data(SHT30_I2CADDR,SHT30_READCOMMAND,[0x06])
        time.sleep(0.5)
        tmp = self._device.read_i2c_block_data(SHT30_I2CADDR,SHT30_READREG,6)
        print "tmp=", tmp
        TRaw = (((tmp[0] & 0x7F) << 8) | tmp[1]) 
        HRaw = ((tmp[3] << 8) | tmp[4]) 
        self.temperature = ((TRaw * 175) / 65535.0) - 45
        self.humidity = 100 * (HRaw) / 65535.0

        self.crcT = tmp[2]
        self.crcH = tmp[5]
        # Verify CRC here
        # force CRC error with the next line
        #tmp[0] = tmp[0]+1
        tT = bytearray([tmp[0], tmp[1]])
        crcTC = self.verify_crc(tT)
        tH = bytearray([tmp[3], tmp[4]])
        crcHC = self.verify_crc(tH)

        if (SHT30DEBUG == True):
            print "SHT30temperature=",self.temperature
            print "SHT30humdity=",self.humidity
            print "SHT30crcTR=",self.crcT
            print "SHT30crcTC=",crcTC
            print "SHT30crcHR=",self.crcH
            print "SHT30crcHC=",crcHC

        if (self.crcT != crcTC) or (self.crcH != crcHC):
            if (SHT30DEBUG == True):
                print "AM2314 BAD CRC"
            self.crc = -1


    def _read_data(self):
        count = 0
        tmp = None
        powercyclecount = 0
        while count <= MAXREADATTEMPT:
            try:
                self._device.write_i2c_block_data(SHT30_I2CADDR,SHT30_READCOMMAND,[0x06])
                time.sleep(0.5)
                tmp = self._device.read_i2c_block_data(SHT30_I2CADDR,SHT30_READREG,6)

                TRaw = (((tmp[0] & 0x7F) << 8) | tmp[1]) 
                HRaw = ((tmp[3] << 8) | tmp[4]) 
                self.temperature = ((TRaw * 175) / 65535.0) - 45
                self.humidity = 100 * (HRaw) / 65535.0

                self.crcT = tmp[2]
                self.crcH = tmp[5]
                # check for > 10.0 degrees higher
                if (self.SHT30PreviousTemp != -1000):   # ignore first time
                        if (self.humidity <0.01 or self.humidity > 100.0):
                            # OK, humidity is bad.  Ignore
                            if (SHT30DEBUG == True):
                                print ">>>>>>>>>>>>>"
                                print "Bad SHT30 Humidity = ", self.temperature
                                print ">>>>>>>>>>>>>"
                                self.badreadings = self.badreadings+1
                                tmp = None
                        else:
                            if (abs(self.temperature - self.SHT30PreviousTemp) > 10.0):
                                # OK, temp is bad.  Ignore
                                if (SHT30DEBUG == True):
                                    print ">>>>>>>>>>>>>"
                                    print "Bad SHT30 Humidity = ", self.temperature
                                    print ">>>>>>>>>>>>>"
                                    self.badreadings = self.badreadings+1
                                    tmp = None
                            else:
                                # Good Temperature
                                self.SHT30PreviousTemp = self.temperature
                else:
                    # assume first is good temperature
                    self.SHT30PreviousTemp = self.temperature
                # IF WE HAVE DATA, LETS EXIT THIS LOOP
                if tmp != None:
                    break
            except Exception as ex:
                if (SHT30DEBUG == True):
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print message
                    print traceback.format_exc()
                    print "SHT30readCount = ", count
            count += 1
            self.retrys += 1
            time.sleep(0.10)
            # only do three power cycle attempts
            if (self.powerpin <> 0):
                if (count > MAXREADATTEMPT):
                    self.powerCycleSHT30()
                    if (powercyclecount <=2): 
                        powercyclecount +1
                        count = 0 
            
        # GET THE DATA OUT OF THE LIST WE READ
        TRaw = (((tmp[0] & 0x7F) << 8) | tmp[1]) 
        HRaw = ((tmp[3] << 8) | tmp[4]) 
        self.temperature = ((TRaw * 175) / 65535.0) - 45
        self.humidity = 100 * (HRaw) / 65535.0

        self.crcT = tmp[2]
        self.crcH = tmp[5]
        # Verify CRC here
        # force CRC error with the next line
        # tmp[0] = tmp[0]+1
        tT = bytearray([tmp[0], tmp[1]])
        crcTC = self.verify_crc(tT)
        tH = bytearray([tmp[3], tmp[4]])
        crcHC = self.verify_crc(tH)

        if (SHT30DEBUG == True):
            print "SHT30temperature=",self.temperature
            print "SHT30humdity=",self.humidity
            print "SHT30crcTR=",self.crcT
            print "SHT30crcTC=",crcTC
            print "SHT30crcHR=",self.crcH
            print "SHT30crcHC=",crcHC

        if (self.crcT != crcTC) or (self.crcH != crcHC):
            if (SHT30DEBUG == True):
                print "SHT30 BAD CRC"
            self.badcrcs = self.badcrcs + 1
            self.crc = -1
        else:
            self.goodreads = self.goodreads+1

    def fast_read_temperature(self):
        self._fast_read_data()
        return self.temperature

    def read_temperature(self):
        self._read_data()
        return self.temperature

    def read_humidity(self):
        self._read_data()
        return self.humidity

    def read_humidity_temperature(self):
        self._read_data()
        return (self.humidity, self.temperature)

    def read_humidity_temperature_crc(self):
        self._read_data()
        return (self.humidity, self.temperature, self.crcH, self.crcT)

    def fast_read_humidity_temperature_crc(self):
        self._fast_read_data()
        return (self.humidity, self.temperature, self.crc, self.crcT)

    def read_status_info(self):
        return  (self.goodreads, self.badreadings, self.badcrcs, self.retrys,self.powercycles)

    
