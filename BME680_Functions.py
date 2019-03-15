

# Check for user imports
try:
    import conflocal as config
except ImportError:
    import config

import sys
import time

sys.path.append('./BME680')



import bme680 as BME680


def setup_bme680(bme680):

    bme680.set_humidity_oversample(BME680.OS_2X)
    bme680.set_pressure_oversample(BME680.OS_4X)
    bme680.set_temperature_oversample(BME680.OS_8X)
    bme680.set_filter(BME680.FILTER_SIZE_3)


# Returns the normalized pressure at sealevel: derived from BMP datasheet
def getSeaLevelPressure(altitude, absolutePressure):
        return absolutePressure / pow(1.0 - (altitude / 44330.0), 5.255)

