import BlynkLib
import wifi_connect as wlan
import _thread as th
import time
from machine import I2C, Pin
from dht import DHT22
import ssd1306
# define out put
p1 = Pin(23, Pin.OUT)
p2 = Pin(19, Pin.OUT)
p3 = Pin(18, Pin.OUT)
p4 = Pin(5,  Pin.OUT)
# DHT22 
dhtPn = Pin(17)
dht = DHT22(dhtPn)
# OLED
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda)
oled = ssd1306.SSD1306_I2C(128, 64, i2c,  addr=0x3c)
oled.fill(0)
oled.text('SENSOR', 40, 5)
oled.text('McroPython', 25, 20)
oled.show()
# wfi connect
wlan.connect()
oled.text(wlan.get_ip(), 3, 35)
oled.show()
# blynk clent
blynk = BlynkLib.Blynk('<TOKEN>', '<SERVER>')
#define a virtual pin write handler
def v4_write_handler(value):
  print('V4: ', int(value))
  p1.value(int(value))
def v5_write_handler(value):
  print('V5: ', int(value))
  p2.value(int(value))
def v6_write_handler(value):
  print('V6: ', int(value))
  p3.value(int(value))
def v7_write_handler(value):
  print('V7: ', int(value))
  p4.value(int(value))

# register the virtual pin
blynk.add_virtual_pin(4, write=v4_write_handler)
blynk.add_virtual_pin(5, write=v5_write_handler)
blynk.add_virtual_pin(6, write=v6_write_handler)
blynk.add_virtual_pin(7, write=v7_write_handler)
# start blink process thread
th.start_new_thread(blynk.run, ())
time.sleep(3)
# lcd display
blynk.virtual_write(0, '     ESP32')
blynk.virtual_write(1, '  MicroPython')
# gpio status
blynk.virtual_write(4, p1.value())
blynk.virtual_write(5, p2.value())
blynk.virtual_write(6, p3.value())
blynk.virtual_write(7, p4.value())

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