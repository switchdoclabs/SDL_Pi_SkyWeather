#
#
# SDL_Pi_GrovePowerDrive
# Raspberry Pi Driver for the SwitchDoc Labs GrovePowerDrive 
#
# SwitchDoc Labs
# April  2017
#
# Version 1.1

import RPi.GPIO as GPIO

GrovePowerDrive_Default_GPIO_Pin_Sig1 = 20
GrovePowerDrive_Default_GPIO_Pin_Sig2 = 21

class SDL_Pi_GrovePowerDrive:
	
	def __init__(self, GPIOPinSig1=GrovePowerDrive_Default_GPIO_Pin_Sig1, GPIOPinSig2=GrovePowerDrive_Default_GPIO_Pin_Sig2,  initialStateSig1 = True, initialStateSig2 = True):
                self._GPIOPinSig1 = GPIOPinSig1
                self._GPIOPinSig2 = GPIOPinSig2

                self._initialStateSig1 = initialStateSig1
                self._initialStateSig2 = initialStateSig2
		
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self._GPIOPinSig1,GPIO.OUT, initial=self._initialStateSig1)
		GPIO.setup(self._GPIOPinSig2,GPIO.OUT, initial=self._initialStateSig1)

	def setPowerDrive(self, sigvalue, value):

		if (sigvalue == 1):
			GPIO.output(self._GPIOPinSig1, value)
		if (sigvalue == 2):
			GPIO.output(self._GPIOPinSig2, value)



		
		
