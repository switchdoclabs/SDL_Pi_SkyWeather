SkyWeather Libraries and Examples for Raspberry Pi Solar Powered Weather Station

Supports SwitchDoc Labs WeatherRack PiWeather Board 

Version V028 

http://www.switchdoc.com/

April 6, 2019:   Version 028 - Support for WXLink - remote WeatherRack/Temp/Humidity
April 3, 2019:   Version 027 - Mod AS3935 Interrupt, added AQI to Database<BR>
March 31, 2019:  Version 026 - Fixed Pins for Optional Fan On/Off<BR>

-----------------
Install this for smbus:

sudo apt-get install python-smbus

Install this next:


git clone https://github.com/adafruit/Adafruit_Python_PureIO.git<BR>
cd Adafruit_Python_PureIO<BR>
sudo python setup.py install<BR>

Other installations required for AM2315:

sudo apt-get install python-pip

sudo apt-get install libi2c-dev


#Installing apscheduler

sudo pip install --upgrade setuptools pip <BR>

sudo pip install setuptools --upgrade  <BR>
sudo pip install apscheduler <BR>

#Installing pigiod

pigpiod is used to get accurate timing readings for the Air Quality sensor. <BR>

sudo apt-get install pigpio


----------------<BR>
Note some configurations of Raspberry Pi software requres the following:<BR>
It won't hurt to do this in any case.<BR>
----------------<BR>
<pre>
sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
cd ..
cd SDL_Pi_SkyWeather
cd Adafruit_Python_SSD1306
sudo python setup.py install
</pre>
SwitchDocLabs Documentation for WeatherRack/WeatherPiArduino under products on: store.switchdoc.com

Read the SkyWeather Instructable on instructables.com for more software installation instructions 

or

Read the tutorial on SkyWeather on http://www.switchdoc.com/
for more software installation instructions.

-----------
setup your configuration variables in config.py!
-----------
We recommend you copy config.py to conflocal.py to avoid updates copying over your configuration file.<BR>
--------
Add SQL instructions
----------

Use phpmyadmin or sql command lines to add the included SQL file to your MySQL databases.<BR>
Note:  If the database has been updated, run the example below to update your database.   The current contents will not be lost.


example:   sudo mysql -u root -p SkyWeather< SkyWeather.sql

user:  root

password: password

Obviously with these credentials, don't connect port 3306 to the Internet.   Change them if you aren't sure.

NOTE:

If you have a WXLink wireless transmitter installed, the software assumes you have connected your AM2315 outdoor temp/humidity sensor to the WXLink.  If you put another AM2315 on your local system, it will use those values instead of the WXLink values

-------------------<BR>
# Starting the SkyWeather.py program
-------------------<BR>

You start the program with two statements:

sudo pigpiod
sudo python SkyWeather.py

-------------------<BR>
Set up your rc.local for start on boot<BR>
-------------------<BR>

insert the following in your /etc/rc.local before the exit 0 statement:

pigpiod
cd /home/pi/SDL_Pi_SkyWeather <BR>
nohup sudo python SkyWeather.py & <BR>



