#
#
# SI1145 Lux Conversion Routines
# SwitchDocLabs
# Thanks to primexandy for C routines
# December 2016
#
# Added Dark Offsets for IR/Vis
#
#
DARKOFFSETVIS = 259
DARKOFFSETIR = 253



def SI1145_IR_to_Lux(ir):
   # irlux = ir * 14.5 / 2.44 for range = high and gain = 1
   # apply dark offset   
   ir = ir - DARKOFFSETIR
   if ir < 0:
    ir = 0

   lux = 2.44
   irlux = 0
   multiplier = 0
   range = 0
   sensitivity =  0
   gain = 1
   # Get gain multipler
   # These are set to defaults in the Adafruit driver - need to change if you change them in the SI1145 driver
   '''
   range = SI1145_Read_Param(fd, (unsigned char)ALS_IR_ADC_MISC)
   if ((range & 32) == 32):
       gain = 14.5
   '''
   #gain = 14.5
   # Get sensitivity
   # These are set to defaults in the Adafruit driver - need to change if you change them in the SI1145 driver
   '''
   sensitivity = SI1145_Read_Param(fd, (unsigned char)ALS_IR_ADC_GAIN)
   if ((sensitivity & 7) == 0): 
       multiplier = 1
   if ((sensitivity & 7) == 1): 
       multiplier = 2
   if ((sensitivity & 7) == 2): 
       multiplier = 4
   if ((sensitivity & 7) == 3): 
       multiplier = 8
    if ((sensitivity & 7) == 4): 
        multiplier = 16
   if ((sensitivity & 7) == 5): 
       multiplier = 32
   if ((sensitivity & 7) == 6): 
       multiplier = 64
   if ((sensitivity & 7) == 7): 
       multiplier = 128
   '''
   multiplier = 1
   #calibration factor to sunlight applied
   irlux = ir * (gain / (lux * multiplier)) * 50
   return irlux

def SI1145_VIS_to_Lux(vis):
   # vislux = vis * 14.5 / 2.44 for range = high and gain = 1
   # apply dark offset   
   vis = vis - DARKOFFSETVIS
   if vis < 0:
    vis = 0

   lux = 2.44
   vislux = 0
   multiplier = 0
   range = 0
   sensitivity =  0
   gain = 1
   # Get gain multipler
   # These are set to defaults in the Adafruit driver - need to change if you change them in the SI1145 driver
   '''
   range = SI1145_Read_Param(fd, (unsigned char)ALS_VIS_ADC_MISC)
   if ((range & 32) == 32):
       gain = 14.5
   '''
   #gain = 14.5
   # Get sensitivity
   # These are set to defaults in the Adafruit driver - need to change if you change them in the SI1145 driver
   '''
   sensitivity = SI1145_Read_Param(fd, (unsigned char)ALS_VIS_ADC_GAIN)
   if ((sensitivity & 7) == 0): 
       multiplier = 1
   if ((sensitivity & 7) == 1): 
       multiplier = 2
   if ((sensitivity & 7) == 2): 
       multiplier = 4
   if ((sensitivity & 7) == 3): 
       multiplier = 8
    if ((sensitivity & 7) == 4): 
        multiplier = 16
   if ((sensitivity & 7) == 5): 
       multiplier = 32
   if ((sensitivity & 7) == 6): 
       multiplier = 64
   if ((sensitivity & 7) == 7): 
       multiplier = 128
   '''
   multiplier = 1
   # calibration to bright sunlight added
   vislux = vis * (gain / (lux * multiplier)) * 100
   return vislux


