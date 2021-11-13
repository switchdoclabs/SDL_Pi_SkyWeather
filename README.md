SkyWeather Libraries and Examples for Raspberry Pi Solar Powered Weather Station

Supports SwitchDoc Labs WeatherRack PiWeather Board

# Changes

* December 15, 2019: Version 055 - MySQL SolarMAX Fixes
* November 27, 2019: Version 054 - Fixed reporting of SolarMAX inside temperature/humidity
* November 26, 2019: Version 053 - Update Blynk with latest SolarMAX Packet Status
* November 2, 2019: Version 052 - Fixed WeatherUnderground URL and Added more debug for LoRa WXLink
* October 15, 2019: Version 051 - Added support for SolarMAX Lead Acid - Must update conflocal.py if used

<pre>
@@ -42,6 +42,10 @@ runLEDs = False
 SolarMAX_Present = False
 Dual_MAX_WXLink = False

# SolarMAX_Type = "LEAD" for SolarMAX Lead Acid
# SolarMAX_Type = "LIPO" for SolarMAX LiPo
SolarMAX_Type = ""
</pre>

* October 14, 2019: Version 050 - Fixed Camera Detection on Buster
* October 12, 2019:   Version 049 - Fixed BlynkBug / AM2315 Bug
* September 29, 2019: Version 048 - Fixed SolarMAX bug
* September 1, 2019: Version 047 - Fixed to Camera Exposure, Minor tweak to WeatherSTEM Interface and SolarMAX (added Version)
* August 19, 2019: Version 046 - Minor Bug release (matplotlib, SolarMAX, blynk)
* August 14, 2019: Version 045 - Camera Debug Support - SolarMAX support - Must update conflocal.py
* August 12, 2019: Version 044 - Camera Debug Support - Overexposure problem
* August 8, 2019:  Version 043 - Improved AM2315 Detection, SQL Structure Fixed, time and date changed, debug for overexposure
* August 6, 2019:  Version 042 - Overlays, Lightning Params added - Must update conflocal.py if used
* July 27, 2019:   Version 041 - Fix to SHT30 for > 122 degrees
* July 8, 2019:    Version 040 - WeatherUnderground Fix, Support for SHT30- Must update conflocal.py if used
* June 5, 2019:    Version 039 - AM2315 Reliablity Fix
* May 21, 2019:    Version 038 - Blynk Bug Fix
* May 21, 2019:    Version 037 - Blynk Changes / Bug Fix
* May 20, 2019:    Version 036 - Fixed Barometric Pressure Reporting
* May 12, 2019:    Version 035 - Debug Statements removed
* May 4, 2019:     Version 034 - WeatherSTEM testing Version
* May 1, 2019:     Version 033 - WeatherSTEM API Started
* April 29, 2019:  Version 033 - WeatherSTEM Modification
* April 28, 2019:  Version 032 - Improved MySQL Reporting
* April 28, 2019:  Version 031 - Fixed WXLink Temperature Reporting
* April 27, 2019:  Version 030 - Modified test programs
* April 20, 2019:  Version 029 - Fixed Lightning_Mode added Image test to blynkCode
* April 6, 2019:   Version 028 - Support for WXLink - remote WeatherRack/Temp/Humidity
* April 3, 2019:   Version 027 - Mod AS3935 Interrupt, added AQI to Database
* March 31, 2019:  Version 026 - Fixed Pins for Optional Fan On/Off

# New SD card configuration
This software requires Python 2 and will not work with Python 3. Support for Python 2 has been dropped in most new Raspberry Pi SD card images. For easiest setup please use a Buster compatible image. The last lite image provided by Rasbian is:
 
[ https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-lite.zip](URL)
 
 Please check your Python version before continuing using:

    python -V

 Which should report "Python 2.7.x"

 If you are creating a new SD card image then you must configure the raspberry pi for your locale and to enable sensor interfaces using raspi-config. Use [tab] key to navigate between UI elements, [space] to select options, and [enter] to select buttons.
 
     sudo raspi-config

 * Select Option 3 Interface Options -> P4 SPI -> Yes to enable SPI.
 * Select Option 3 Interface Options -> P5 I2C -> Yes to enable I2C.
 
 If not in UK set locale to your country
 
 * Select Option 5 Localisation Options -> L1 Locale -> Use [down arrow] to find your desired language code e.g. en_US.UTF-8 (for USA) -> Select using [space] -> [OK] -> Select default locale to match previous selection e.g. en_US.UTF-8 -> [OK]
 * Select Option 5 Localisation Options -> L2 Timezone -> e.g. America -> Los Angeles -> [OK]
 * Select Option 5 Localisation Options -> L3 Keyboard -> e.g. Generic 105 key Intl -> Select appropriate keyboard layout. For US first select "Other" then "English (US) -> [OK] -> Use defaults [OK] -> No Compose Key [OK]

 If using Wifi:
 
 * Select Option 1 system Options -> S1 Wireless -> Select country [ok] -> Enter your wifi SSID [ok] -> Enter your wifi password [ok].

 Optional but recommended:
 
 Enable SSH to allow for remote command line interface.
 
  * Select Option 3 Interface Options -> P2 SSH -> Yes to enable SSH.

 Change hostname:
 
 * Select Option 1 system Options -> S4 Hostname -> Enter your desired name e.g. "skyweatherpi" [enter]

 Change "pi" user password:
 
 IMPORTANT: If you have changed the keyboard layout please exit out of "raspi-config" and reboot before changing password.
 
 * Select Option 1 system Options -> S3 Password -> Enter your desired password [enter]
 

## New SD: Install core requirements

    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y build-essential python-smbus python-pip python-dev git libi2c-dev pigpio python-pigpio python-numpy python-matplotlib python-mpltoolkits.basemap python-picamera
    sudo pip install --upgrade pip setuptools apscheduler requests

Install this next:

     cd ~
     git clone https://github.com/adafruit/Adafruit_Python_PureIO.git
     cd Adafruit_Python_PureIO
     sudo python setup.py install

## New SD: Download SkyWeather

     cd ~
     git clone https://github.com/switchdoclabs/SDL_Pi_SkyWeather.git
     cd ~/SDL_Pi_SkyWeather/Adafruit_Python_BMP
     sudo python setup.py install
     cd ~/SDL_Pi_SkyWeather/Adafruit_Python_GPIO
     sudo python setup.py install
     cd ~/SDL_Pi_SkyWeather/Adafruit_Python_SSD1306
     sudo python setup.py install

## New SD: Configuration settings

We recommend you copy config.py to conflocal.py to avoid updates copying over your configuration file.

     cd ~/SDL_Pi_SkyWeather
     cp config.py conflocal.py

Edit the setting:

     nano conflocal.py

## New SD: Database configuration
If you plan on using the SQL database for data storage.

    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install mariadb-server python-mysqldb -y
    sudo mysql_secure_installation
    sudo mysql -u root -p < ~/SDL_Pi_SkyWeather/SkyWeatherSQLWeatherPiStructure.sql

[More help installing sql server](https://pimylifeup.com/raspberry-pi-mysql/)

# Upgrading existing SD card
If you have an existing working SD card and wish to upgrade the SkyWeather code.

     cd ~/SDL_Pi_SkyWeather
     git pull

## Existing SD: Updating conflocal.py
To merge new config.py variables into your conflocal.py version for compatibility run this command:

    diff conflocal.py config.py

Check your new settings:

    nano conflocal.py

# Starting SkyWeather.py program
You start the program with two statements:

     sudo pigpiod
     sudo python SkyWeather.py

# Auto start SkyWeather on Boot
Set up your rc.local for start on boot. Insert the following in your /etc/rc.local before the exit 0 statement:

     pigpiod
     cd /home/pi/SDL_Pi_SkyWeather
     nohup sudo python SkyWeather.py &

# More documentation

[SkyWeather Product Page](https://shop.switchdoc.com/products/skyweather-raspberry-pi-based-weather-station-kit-for-the-cloud)

[SkyWeather Manual](https://www.switchdoc.com/wp-content/uploads/2019/07/SkyWeatherAssemblyAndTesting-2.pdf)

[SkyWeather Assembly Tips](https://www.switchdoc.com/2019/06/skyweather-assembly-tips-raspberry-pi/)


NOTE:

If you have a WXLink wireless transmitter installed, the software assumes you have connected your AM2315 outdoor temp/humidity sensor to the WXLink.  If you put another AM2315 on your local system, it will use those values instead of the WXLink values
