import Blynk8266import wifi_connect as wlan import time
from dht import DHT22from machine import I2C, Pinimport gcdhtPn = Pin(5)
dht = DHT22(dhtPn)
p4 = Pin(4, Pin.OUT)
p13 = Pin(13, Pin.OUT)
wlan.connect()print('WIFI Connected: ', wlan.get_ip())blynk = Blynk8266.Blynk('71554af7a98b4535a7383f5be5d91ca3', '27.254.63.34')#define a virtual pin write handlerdef v4_write_handler(value):  print('V4: ', int(value))
  p4.value(int(value))
  blynk.virtual_write(6, 0 if p4.value() == 0 else 255)def v5_write_handler(value):  print('V5: ', int(value))
  p13.value(int(value))
  blynk.virtual_write(7, 0 if p13.value() == 0 else 255)
def v6_write_handler(value):
  print('V6: ', int(value))
def v7_write_handler(value):
  print('V7: ', int(value))
def task():
  heap = gc.mem_free()/1000
  print('HEAP: ', heap)
  try:    
    dht.measure()
    blynk.virtual_write(0, heap)
    blynk.virtual_write(1, dht.temperature())
    blynk.virtual_write(2, dht.humidity()) 
  except OSError as e:
    print('Err', e)
def blynk_connected():
  blynk.virtual_write(4, p4.value())
  blynk.virtual_write(5, p13.value())
  blynk.virtual_write(6, 0 if p4.value() == 0 else 255)
  blynk.virtual_write(7, 0 if p13.value() == 0 else 255)
  print('blynk connected')
# register the virtual pinblynk.add_virtual_pin(4, write=v4_write_handler)blynk.add_virtual_pin(5, write=v5_write_handler) 
blynk.add_virtual_pin(8, write=v6_write_handler)
blynk.add_virtual_pin(9, write=v7_write_handler)
blynk.set_user_task(task, 60000)
blynk.on_connect(blynk_connected)# start run thread
print('HEAP: ', gc.mem_free())
gc.collect()blynk.run()