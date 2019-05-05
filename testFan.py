import sys
sys.path.append('./SDL_Pi_GrovePowerDrive')

import  SDL_Pi_GrovePowerDrive
import time

GPIO_Pin_PowerDrive_Sig1 = 5
GPIO_Pin_PowerDrive_Sig2 = 6


myPowerDrive = SDL_Pi_GrovePowerDrive.SDL_Pi_GrovePowerDrive(GPIO_Pin_PowerDrive_Sig1, GPIO_Pin_PowerDrive_Sig2, True, True)
    
while True:
    print "turning Pin %i off" % GPIO_Pin_PowerDrive_Sig1
    myPowerDrive.setPowerDrive(1,0)


    myPowerDrive.setPowerDrive(2,0)

    time.sleep(10)
    
    print "turning Pin %i on" % GPIO_Pin_PowerDrive_Sig1
    myPowerDrive.setPowerDrive(1,1)
    time.sleep(10)

