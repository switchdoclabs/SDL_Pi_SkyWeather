Modifications by SwitchDoc Labs to support the Grove OLED 128x64 Display from SwitchDoc Labs March 2016


Before using the library you will need to make sure you have a few dependencies installed. Connect to your device using SSH and follow the steps below.

If you're using a Raspberry Pi, install the RPi.GPIO library by executing:
 sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo pip install RPi.GPIO


Finally, on the Raspberry Pi install the Python Imaging Library and smbus library by executing:

sudo apt-get install python-imaging python-smbus

Now to download and install the SSD1306 python library code and examples, execute the following commands:

sudo apt-get install git 
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install

------------------------
Running test programs
------------------------

The Adafruit test programs have been slightly modified to run the SwitchDoc Labs OLED display.    The I2C address has changed to 0x3C.

To run:

sudo python SDL_image.py

sudo python SDL_animate.py

sudo python SDL_shapes.py
---------------------------------




Adafruit Python SSD1306
=======================

Python library to use SSD1306-based 128x64 or 128x32 pixel OLED displays with a Raspberry Pi or Beaglebone Black.

Designed specifically to work with the Adafruit SSD1306-based OLED displays ----> https://www.adafruit.com/categories/98

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Tony DiCola for Adafruit Industries.
MIT license, all text above must be included in any redistribution
