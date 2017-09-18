import BlynkLib
import wifi_connect as wlan
import _thread as th
import time
from machine import I2C, Pin
from dht12 import DHT12 
import ssd1306
# OLED
rst = Pin(16, Pin.OUT)
rst.value(1)
oledScl = Pin(15, Pin.OUT, Pin.PULL_UP)
oledSda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2cOled = I2C(scl=oledScl, sda=oledSda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2cOled,  addr=0x3c)
oled.fill(0)
oled.text('SENSOR', 40, 5)
oled.text('McroPython', 25, 20)
oled.show()
# Sensor
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=20000)
dht = DHT12(i2c)

wlan.connect()
oled.text(wlan.get_ip(), 3, 35)
oled.show()
blynk = BlynkLib.Blynk('<TOKEN>')
#define a virtual pin write handler
def v4_write_handler(value):
  print('V4: ', value)
def v5_write_handler(value):
  print('V5: ', value)
def v6_write_handler(value):
  print('V6: ', value)
def v7_write_handler(value):
  print('V7: ', value)

# register the virtual pin
blynk.add_virtual_pin(4, write=v4_write_handler)
blynk.add_virtual_pin(5, write=v5_write_handler)
blynk.add_virtual_pin(6, write=v6_write_handler)
blynk.add_virtual_pin(7, write=v7_write_handler)
# start run thread
th.start_new_thread(blynk.run, ())
time.sleep(3)
blynk.virtual_write(0, '     ESP32')
blynk.virtual_write(1, '  MicroPython')
def dht12_read():
  while True:
    try:
      dht.measure()
      oled.fill(0)
      oled.text('SENSOR', 40, 5)
      oled.text('McroPython', 25, 20) 
      oled.text('T: {0:.1f} C'.format(dht.temperature()), 10, 35) 
      oled.text('H: {0:.1f} %'.format(dht.humidity()), 10, 50)
      oled.show()
      print('TEMP: {0:.1f}, HUMI: {1:.1f}'.format(dht.temperature(), dht.humidity()))
      blynk.virtual_write(2, dht.temperature())
      blynk.virtual_write(3, dht.humidity())
    except OSError as e:
      print('Err', e)
    time.sleep(60)

th.start_new_thread(dht12_read, ())
