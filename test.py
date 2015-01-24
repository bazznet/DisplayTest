import time
import datetime
import Adafruit_DHT
from decimal import Decimal
from Adafruit_LEDBackpack import LEDBackpack
from Adafruit_7Segment  import SevenSegment


sensor = Adafruit_DHT.AM2302
pin = 4
display = SevenSegment(address=0x70)
setting = LEDBackpack(address=0x70, debug=False)

def ReadTemp():
 humidityraw, temperatureraw = Adafruit_DHT.read_retry(sensor, pin)
 temperature = '%04.1f' % temperatureraw
 humidity = '%04.1f' % humidityraw

 if float(humidity) > 99.9:
  humidity = '99.9'

 print temperature
 print humidity
 return humidity, temperature

#humidity, temperature = ReadTemp()

for x in range (99,1000):
 display.writeDigitRaw(0,x)
 time.sleep(0.5)

#while 1:
# try:
#  if humidity is not None and temperature is not None:
#   display.writeDigit(0,int(temperature[0]), dot=False)
#   display.writeDigit(1,int(temperature[1]), dot=True)
#   display.writeDigit(3,int(temperature[3]), dot=False)
#   display.writeDigit(4,12)
#   time.sleep(2)
#   display.writeDigit(0,int(humidity[0]), dot=False)
#   display.writeDigit(1,int(humidity[1]), dot=True)
#   display.writeDigit(3,int(humidity[3]), dot=False)
#   display.writeDigitRaw(4,118)
#   time.sleep(2)
#   humidity, temperature = ReadTemp()
# except KeyboardInterrupt:
#  setting.clear()
#  print ('User stopped program')
#  raise
# except:
#  print ('Something went really wrong')
#setting.clear()


