#
#
# SDL_Pi_HDC1000
# Raspberry Pi Driver for the SwitchDoc Labs HDC1000 Breakout Board
#
# SwitchDoc Labs
# January 2017
#
# Version 1.1

#constants

# I2C Address
HDC1000_ADDRESS =                       (0x40)    # 1000000 
# Registers
HDC1000_TEMPERATURE_REGISTER =          (0x00)
HDC1000_HUMIDITY_REGISTER =             (0x01)
HDC1000_CONFIGURATION_REGISTER =        (0x02)
HDC1000_MANUFACTURERID_REGISTER =       (0xFE)
HDC1000_DEVICEID_REGISTER =        	(0xFF)
HDC1000_SERIALIDHIGH_REGISTER =         (0xFB)
HDC1000_SERIALIDMID_REGISTER =          (0xFC)
HDC1000_SERIALIDBOTTOM_REGISTER =       (0xFD)

#Configuration Register Bits

HDC1000_CONFIG_RESET_BIT =              (0x8000)
HDC1000_CONFIG_HEATER_ENABLE =          (0x2000)
HDC1000_CONFIG_ACQUISITION_MODE =       (0x1000)
HDC1000_CONFIG_BATTERY_STATUS =         (0x0800)
HDC1000_CONFIG_TEMPERATURE_RESOLUTION = (0x0400)
HDC1000_CONFIG_HUMIDITY_RESOLUTION_HBIT =    (0x0200)
HDC1000_CONFIG_HUMIDITY_RESOLUTION_LBIT =    (0x0100)

HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT = (0x0000)
HDC1000_CONFIG_TEMPERATURE_RESOLUTION_11BIT = (0x0400)

HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT = (0x0000)
HDC1000_CONFIG_HUMIDITY_RESOLUTION_11BIT = (0x0100)
HDC1000_CONFIG_HUMIDITY_RESOLUTION_8BIT = (0x0200)

import smbus
import time


class SDL_Pi_HDC1000:
        def __init__(self, twi=1, addr=HDC1000_ADDRESS ):
                self._bus = smbus.SMBus(twi)
                self._addr = addr
                #       0x10(48)    Temperature, Humidity enabled, Resolultion = 14-bits, Heater off
                config = HDC1000_CONFIG_ACQUISITION_MODE 
                self._bus.write_byte_data(HDC1000_ADDRESS,HDC1000_CONFIGURATION_REGISTER, config>>8)


        # public functions

        def readTemperature(self):
                
                # Send temp measurement command, 0x00(00)

                self._bus.write_byte(HDC1000_ADDRESS, HDC1000_TEMPERATURE_REGISTER )
                time.sleep(0.020)


                # Read data back, 2 bytes

                # temp MSB, temp LSB
                data0 = self._bus.read_byte(HDC1000_ADDRESS)
                data1 = self._bus.read_byte(HDC1000_ADDRESS)
                # Convert the data
                temp = (data0 * 256) + data1
                cTemp = (temp / 65536.0) * 165.0 - 40
                return cTemp


        def readHumidity(self):
                # Send humidity measurement command, 0x01(01)

                self._bus.write_byte(HDC1000_ADDRESS, HDC1000_HUMIDITY_REGISTER) 

                time.sleep(0.020)


                # Read data back, 2 bytes

                # humidity MSB, humidity LSB
                data0 = self._bus.read_byte(HDC1000_ADDRESS)
                data1 = self._bus.read_byte(HDC1000_ADDRESS)
                # Convert the data
                humidity = (data0 * 256) + data1
                humidity = (humidity / 65536.0) * 100.0
                return humidity
        
        def readConfigRegister(self):
                # Read config register

                self._bus.write_byte(HDC1000_ADDRESS, HDC1000_CONFIGURATION_REGISTER) 

                # config register
                data0 = self._bus.read_byte(HDC1000_ADDRESS)
                data1 = self._bus.read_byte(HDC1000_ADDRESS)

                #print "register=%d %X"% (data0, data0)
                return data0

        def turnHeaterOn(self):
                # Read config register
                config = self.readConfigRegister()
                config = config<<8 | HDC1000_CONFIG_HEATER_ENABLE 
                self._bus.write_byte_data(HDC1000_ADDRESS,HDC1000_CONFIGURATION_REGISTER,config>>8)

                return

        def turnHeaterOff(self):
                # Read config register
                config = self.readConfigRegister()
                config = config<<8 & ~HDC1000_CONFIG_HEATER_ENABLE 
                self._bus.write_byte_data(HDC1000_ADDRESS,HDC1000_CONFIGURATION_REGISTER,config>>8)

                return

        def setHumidityResolution(self,resolution):
                # Read config register
                config = self.readConfigRegister()
                config = (config<<8 & ~0x0300) | resolution 
                self._bus.write_byte_data(HDC1000_ADDRESS,HDC1000_CONFIGURATION_REGISTER,config>>8)
                return

        def setTemperatureResolution(self,resolution):
                # Read config register
                config = self.readConfigRegister()
                config = (config<<8 & ~0x0400) | resolution 
                self._bus.write_byte_data(HDC1000_ADDRESS,HDC1000_CONFIGURATION_REGISTER,config>>8)
                return


        def readBatteryStatus(self):
                
                # Read config register
                config = self.readConfigRegister()
                config = config<<8 & ~ HDC1000_CONFIG_HEATER_ENABLE

                if (config == 0):
                    return True
                else:
                    return False

                return 0
	
	def readManufacturerID(self):

		data = self._bus.read_i2c_block_data (HDC1000_ADDRESS, HDC1000_MANUFACTURERID_REGISTER  , 2)
		return data[0] * 256 + data[1]

	def readDeviceID(self):

		data = self._bus.read_i2c_block_data (HDC1000_ADDRESS, HDC1000_DEVICEID_REGISTER  , 2)
		return data[0] * 256 + data[1]

	def readSerialNumber(self):

		serialNumber = 0

		data = self._bus.read_i2c_block_data (HDC1000_ADDRESS, HDC1000_SERIALIDHIGH_REGISTER  , 2)
                serialNumber = data[0]*256+ data[1] 

		data = self._bus.read_i2c_block_data (HDC1000_ADDRESS, HDC1000_SERIALIDMID_REGISTER  , 2)
                serialNumber = serialNumber*256 + data[0]*256 + data[1] 

		data = self._bus.read_i2c_block_data (HDC1000_ADDRESS, HDC1000_SERIALIDBOTTOM_REGISTER  , 2)
                serialNumber = serialNumber*256 + data[0]*256 + data[1] 

		return serialNumber
	
	
