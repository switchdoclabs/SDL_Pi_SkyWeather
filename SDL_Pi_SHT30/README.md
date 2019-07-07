#
# SDL_Pi_SHT30
#
# SHT30 Pure Python Library
# SwitchDoc Labs July 2019
#
#

Version 1.1: July 8, 2019:  Initial Version
 

#Introduction

For the SwitchDoc Labs SHT30<BR>



# testing

```
import SHT30 
sens = SHT30.SHT30()
print sens.read_temperature()
print sens.read_humidity()
print sens.read_humidity_temperature()
print sens.read_humidity_temperature_crc()
```
