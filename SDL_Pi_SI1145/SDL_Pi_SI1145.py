#!/usr/bin/python
# modified for medium range vis, IR SDL December 2016 and non Adafruit I2C (interfers with others)

# Original Author: Joe Gutting
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

import logging
import time

import smbus


# COMMANDS
SI1145_PARAM_QUERY                      = 0x80
SI1145_PARAM_SET                        = 0xA0
SI1145_NOP                              = 0x0
SI1145_RESET                            = 0x01
SI1145_BUSADDR                          = 0x02
SI1145_PS_FORCE                         = 0x05
SI1145_ALS_FORCE                        = 0x06
SI1145_PSALS_FORCE                      = 0x07
SI1145_PS_PAUSE                         = 0x09
SI1145_ALS_PAUSE                        = 0x0A
SI1145_PSALS_PAUSE                      = 0xB
SI1145_PS_AUTO                          = 0x0D
SI1145_ALS_AUTO                         = 0x0E
SI1145_PSALS_AUTO                       = 0x0F
SI1145_GET_CAL                          = 0x12

# Parameters
SI1145_PARAM_I2CADDR                    = 0x00
SI1145_PARAM_CHLIST                     = 0x01
SI1145_PARAM_CHLIST_ENUV                = 0x80
SI1145_PARAM_CHLIST_ENAUX               = 0x40
SI1145_PARAM_CHLIST_ENALSIR             = 0x20
SI1145_PARAM_CHLIST_ENALSVIS            = 0x10
SI1145_PARAM_CHLIST_ENPS1               = 0x01
SI1145_PARAM_CHLIST_ENPS2               = 0x02
SI1145_PARAM_CHLIST_ENPS3               = 0x04

SI1145_PARAM_PSLED12SEL                 = 0x02
SI1145_PARAM_PSLED12SEL_PS2NONE         = 0x00
SI1145_PARAM_PSLED12SEL_PS2LED1         = 0x10
SI1145_PARAM_PSLED12SEL_PS2LED2         = 0x20
SI1145_PARAM_PSLED12SEL_PS2LED3         = 0x40
SI1145_PARAM_PSLED12SEL_PS1NONE         = 0x00
SI1145_PARAM_PSLED12SEL_PS1LED1         = 0x01
SI1145_PARAM_PSLED12SEL_PS1LED2         = 0x02
SI1145_PARAM_PSLED12SEL_PS1LED3         = 0x04

SI1145_PARAM_PSLED3SEL                  = 0x03
SI1145_PARAM_PSENCODE                   = 0x05
SI1145_PARAM_ALSENCODE                  = 0x06

SI1145_PARAM_PS1ADCMUX                  = 0x07
SI1145_PARAM_PS2ADCMUX                  = 0x08
SI1145_PARAM_PS3ADCMUX                  = 0x09
SI1145_PARAM_PSADCOUNTER                = 0x0A
SI1145_PARAM_PSADCGAIN                  = 0x0B
SI1145_PARAM_PSADCMISC                  = 0x0C
SI1145_PARAM_PSADCMISC_RANGE            = 0x20
SI1145_PARAM_PSADCMISC_PSMODE           = 0x04

SI1145_PARAM_ALSIRADCMUX                = 0x0E
SI1145_PARAM_AUXADCMUX                  = 0x0F

SI1145_PARAM_ALSVISADCOUNTER            = 0x10
SI1145_PARAM_ALSVISADCGAIN              = 0x11
SI1145_PARAM_ALSVISADCMISC              = 0x12
SI1145_PARAM_ALSVISADCMISC_VISRANGE     = 0x10
#SI1145_PARAM_ALSVISADCMISC_VISRANGE     = 0x00

SI1145_PARAM_ALSIRADCOUNTER             = 0x1D
SI1145_PARAM_ALSIRADCGAIN               = 0x1E
SI1145_PARAM_ALSIRADCMISC               = 0x1F
SI1145_PARAM_ALSIRADCMISC_RANGE         = 0x20
#SI1145_PARAM_ALSIRADCMISC_RANGE         = 0x00

SI1145_PARAM_ADCCOUNTER_511CLK          = 0x70

SI1145_PARAM_ADCMUX_SMALLIR             = 0x00
SI1145_PARAM_ADCMUX_LARGEIR             = 0x03



# REGISTERS
SI1145_REG_PARTID                       = 0x00
SI1145_REG_REVID                        = 0x01
SI1145_REG_SEQID                        = 0x02

SI1145_REG_INTCFG                       = 0x03
SI1145_REG_INTCFG_INTOE                 = 0x01
SI1145_REG_INTCFG_INTMODE               = 0x02

SI1145_REG_IRQEN                        = 0x04
SI1145_REG_IRQEN_ALSEVERYSAMPLE         = 0x01
SI1145_REG_IRQEN_PS1EVERYSAMPLE         = 0x04
SI1145_REG_IRQEN_PS2EVERYSAMPLE         = 0x08
SI1145_REG_IRQEN_PS3EVERYSAMPLE         = 0x10


SI1145_REG_IRQMODE1                     = 0x05
SI1145_REG_IRQMODE2                     = 0x06

SI1145_REG_HWKEY                        = 0x07
SI1145_REG_MEASRATE0                    = 0x08
SI1145_REG_MEASRATE1                    = 0x09
SI1145_REG_PSRATE                       = 0x0A
SI1145_REG_PSLED21                      = 0x0F
SI1145_REG_PSLED3                       = 0x10
SI1145_REG_UCOEFF0                      = 0x13
SI1145_REG_UCOEFF1                      = 0x14
SI1145_REG_UCOEFF2                      = 0x15
SI1145_REG_UCOEFF3                      = 0x16
SI1145_REG_PARAMWR                      = 0x17
SI1145_REG_COMMAND                      = 0x18
SI1145_REG_RESPONSE                     = 0x20
SI1145_REG_IRQSTAT                      = 0x21
SI1145_REG_IRQSTAT_ALS                  = 0x01

SI1145_REG_ALSVISDATA0                  = 0x22
SI1145_REG_ALSVISDATA1                  = 0x23
SI1145_REG_ALSIRDATA0                   = 0x24
SI1145_REG_ALSIRDATA1                   = 0x25
SI1145_REG_PS1DATA0                     = 0x26
SI1145_REG_PS1DATA1                     = 0x27
SI1145_REG_PS2DATA0                     = 0x28
SI1145_REG_PS2DATA1                     = 0x29
SI1145_REG_PS3DATA0                     = 0x2A
SI1145_REG_PS3DATA1                     = 0x2B
SI1145_REG_UVINDEX0                     = 0x2C
SI1145_REG_UVINDEX1                     = 0x2D
SI1145_REG_PARAMRD                      = 0x2E
SI1145_REG_CHIPSTAT                     = 0x30

# I2C Address
SI1145_ADDR                             = 0x60

class SDL_Pi_SI1145(object):
        def __init__(self, address=SI1145_ADDR, busnum=1, indoor=0):

                self._logger = logging.getLogger('SI1145')

                # Create I2C device.
                self._device = smbus.SMBus(1) 

                #reset device
                self._reset()

                # Load calibration values.
                self._load_calibration(indoor)

        # device reset
        def _reset(self):
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_MEASRATE0, 0)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_MEASRATE1, 0)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_IRQEN, 0)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_IRQMODE1, 0)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_IRQMODE2, 0)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_INTCFG, 0)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_IRQSTAT, 0xFF)

                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_COMMAND, SI1145_RESET)
                time.sleep(.01)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_HWKEY, 0x17)
                time.sleep(.01)

        # write Param
        def writeParam(self, p, v):
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_PARAMWR, v)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_COMMAND, p | SI1145_PARAM_SET)
                paramVal = self._device.read_byte_data(SI1145_ADDR, SI1145_REG_PARAMRD)
                return paramVal

        # load calibration to sensor
        def _load_calibration(self, indoor):
                # /***********************************/
                # Enable UVindex measurement coefficients!
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_UCOEFF0, 0x29)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_UCOEFF1, 0x89)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_UCOEFF2, 0x02)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_UCOEFF3, 0x00)

                # Enable UV sensor
                self.writeParam(SI1145_PARAM_CHLIST, SI1145_PARAM_CHLIST_ENUV | SI1145_PARAM_CHLIST_ENALSIR | SI1145_PARAM_CHLIST_ENALSVIS | SI1145_PARAM_CHLIST_ENPS1)

                # Enable interrupt on every sample
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_INTCFG, SI1145_REG_INTCFG_INTOE)
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_IRQEN, SI1145_REG_IRQEN_ALSEVERYSAMPLE)

                # /****************************** Prox Sense 1 */

                # Program LED current
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_PSLED21, 0x03) # 20mA for LED 1 only
                self.writeParam(SI1145_PARAM_PS1ADCMUX, SI1145_PARAM_ADCMUX_LARGEIR)

                # Prox sensor #1 uses LED #1
                self.writeParam(SI1145_PARAM_PSLED12SEL, SI1145_PARAM_PSLED12SEL_PS1LED1)


                # Fastest clocks, clock div 1
                if (indoor == 1):
                    self.writeParam(SI1145_PARAM_PSADCGAIN, 1)
                else: 
                    #self.writeParam(SI1145_PARAM_PSADCGAIN, 4)
                    self.writeParam(SI1145_PARAM_PSADCGAIN, 0)

                # Take 511 clocks to measure
                self.writeParam(SI1145_PARAM_PSADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

                # in prox mode, high range
                self.writeParam(SI1145_PARAM_PSADCMISC, SI1145_PARAM_PSADCMISC_RANGE | SI1145_PARAM_PSADCMISC_PSMODE)
                self.writeParam(SI1145_PARAM_ALSIRADCMUX, SI1145_PARAM_ADCMUX_SMALLIR)

                # Fastest clocks, clock div 1
                if (indoor == 1):
                    self.writeParam(SI1145_PARAM_ALSIRADCGAIN, 1)
                else:
                    #self.writeParam(SI1145_PARAM_ALSIRADCGAIN, 4)
                    self.writeParam(SI1145_PARAM_ALSIRADCGAIN, 0)
                #self.writeParam(SI1145_PARAM_ALSIRADCGAIN, 4)

                # Take 511 clocks to measure
                self.writeParam(SI1145_PARAM_ALSIRADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

                # in high range mode
                self.writeParam(SI1145_PARAM_ALSIRADCMISC, 0)
                #self.writeParam(SI1145_PARAM_ALSIRADCMISC, SI1145_PARAM_ALSIRADCMISC_RANGE)

                # fastest clocks, clock div 1
                self.writeParam(SI1145_PARAM_ALSVISADCGAIN, 0)
                #self.writeParam(SI1145_PARAM_ALSVISADCGAIN, 4)


                # Take 511 clocks to measure
                self.writeParam(SI1145_PARAM_ALSVISADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

                # in high range mode (not normal signal)
                #self.writeParam(SI1145_PARAM_ALSVISADCMISC, SI1145_PARAM_ALSVISADCMISC_VISRANGE)
                self.writeParam(SI1145_PARAM_ALSVISADCMISC, 0)

                # measurement rate for auto
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_MEASRATE0, 0xFF) # 255 * 31.25uS = 8ms

                # auto run
                self._device.write_byte_data(SI1145_ADDR,SI1145_REG_COMMAND, SI1145_PSALS_AUTO)

        # returns the UV index * 100 (divide by 100 to get the index)
	# apply additional calibration of /10 based on sunlight
        def readUV(self):
                data = self._device.read_i2c_block_data(SI1145_ADDR,0x2C,2)
		return (data[1] * 256 + data[0])/10

        #returns visible + IR light levels
        def readVisible(self):
                data =  self._device.read_i2c_block_data(SI1145_ADDR,0x22,2)
		return data[1] * 256 + data[0]

        #returns IR light levels
        def readIR(self):
                data = self._device.read_i2c_block_data(SI1145_ADDR,0x24,2)
		return data[1] * 256 + data[0]

        # Returns "Proximity" - assumes an IR LED is attached to LED
        def readProx(self):
                data = self._device.read_i2c_block_data(SI1145_ADDR,0x26,2)
		return data[1] * 256 + data[0]

