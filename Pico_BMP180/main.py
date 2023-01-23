# Indoor Temperature and pressure sensor using sh1106 128x64 OLED as output
# BMP180 Barometric sensor will read out alongside the on board sensor
# Display format 
# Temp board
# Pressure BMP180
# Temp BMP180
# Relative SLP or Altitude

# Import libs
from machine import Pin, I2C
from time import sleep
import sh1106
from sh1106 import SH1106_I2C
import framebuf
from bmp085 import BMP180
# Declare HW variables
    #I2C
i2c = I2C(0,sda=Pin(20), scl=Pin(21), freq=100000)
bus = I2C(0, sda=Pin(20), scl=Pin(21), freq=100000)
    #OLED
WIDTH = 128
HIGHT = 64
#display = SH1106_I2C(WIDTH, HIGHT, i2c)
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
    #BMP180
bmp180 = BMP180(bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325
    #onboard TEMP
sensor_temp = machine.ADC(4) #Read thermocouple value
conversion_factor = 3.3 / (65535) #Convert 
    #onboard LED 
led = Pin(25,Pin.OUT)
# Delcare program variables
# Declare timing variables
sleeptime = 0.050
waittime = 1.95
#
# FUNCTIONS
    #LED
def led_flash():
    led.toggle()
    sleep(sleeptime)
    led.toggle()
def do_it_all():
    #onboard Temp
    reading = sensor_temp.read_u16() * conversion_factor
    temp = 27 - (reading - 0.706)/0.001721
    temp_t = int(temp)
    #BMP180
    #gwar = blocking_read(bmp180.temperature)
    temp_bmp180 = bmp180.temperature
    p = bmp180.pressure
    altitude = bmp180.altitude
    print(temp, temp_bmp180, p, altitude)
    
    #OLED
    display.text("T1:",0,0)
    display.text(str(temp_t)+"*C",32,0)
    display.text("T2:",0,16)
    display.text(str(temp_bmp180)+"*C",32,16)
    display.text("P:",0,32)
    display.text(str(p)+"mB",32,32)
    display.text("Alt:",0,48)
    display.text(str(altitude)+"M",32,48)
    display.show()
    display.fill(0)
    led_flash()
    sleep(waittime)
# MAIN 
while True:
    #call function(s)
    do_it_all()
    #wait a bit and do it again.

    #END