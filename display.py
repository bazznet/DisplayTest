import time
import datetime
import Adafruit_DHT
from decimal import Decimal
from Adafruit_LEDBackpack import LEDBackpack
from Adafruit_7Segment  import SevenSegment
import json
import urllib2
import RPi.GPIO as GPIO

sensor = Adafruit_DHT.AM2302
pin = 4 
display = SevenSegment(address=0x70)
setting = LEDBackpack(address=0x70, debug=False)
GPIO.setmode(GPIO.BCM)
RedLED = 23
GreenLED = 24
BlueLED = 25
GPIO.setup(RedLED,GPIO.OUT)
GPIO.setup(GreenLED,GPIO.OUT)
GPIO.setup(BlueLED,GPIO.OUT)

GPIO.output(RedLED,GPIO.HIGH)
GPIO.output(GreenLED,GPIO.HIGH)
GPIO.output(BlueLED,GPIO.HIGH)

def ReadTemp():
 humidityraw, temperatureraw = Adafruit_DHT.read_retry(sensor, pin)
 temperature = '%04.1f' % temperatureraw
 humidity = '%04.1f' % humidityraw
 if float(humidity) > 99.9:
  humidity = '99.9'
 return humidity, temperature

def ReadExt():
 f = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=laval,qc&units=metric')
 json_string = f.read()
 parsed_json = json.loads(json_string)
 temp_f = parsed_json['main']['temp']
 hum_f = parsed_json['main']['humidity']
 f.close()
 return temp_f

def UpdateLED(temp, hum): #fonction qui update une LED RGB en fonction de l'humidity opttimial vs la temperature exterieur
 out_temp = float(temp)
 in_hum = float(hum)
 print ('outside is: ' + str(out_temp))
 print ('inside humitidy is: ' + str(in_hum))
 
 if -10 <= out_temp <= 10: #si temperature exterieur est 'normale'
  if 20 <= in_hum <= 30: #si on est dans le bon range d'humidity, on allume VERT, on femer les autres au cas
   GPIO.output(RedLED, GPIO.HIGH)
   GPIO.output(GreenLED, GPIO.LOW)
   GPIO.output(BlueLED, GPIO.HIGH)
  elif in_hum < 20: #par contre, si on est en bas du range, on allume BLEU brrr fait froid (sec dans ce cas)
   GPIO.output(RedLED, GPIO.HIGH)
   GPIO.output(GreenLED, GPIO.HIGH)
   GPIO.output(BlueLED, GPIO.LOW)
  elif in_hum > 30: #par contre, si on est en haut du range, on allume ROUGE danger trop humide!
   GPIO.output(RedLED, GPIO.LOW)
   GPIO.output(GreenLED, GPIO.HIGH)
   GPIO.output(BlueLED, GPIO.HIGH)

 elif out_temp < -10: #si temperature exterieur est en bas de -10
  if 10 <= in_hum <= 20: #si on est dans le bon range d'humidity, on allume VERT, on femer les autres au cas
   GPIO.output(RedLED, GPIO.HIGH)
   GPIO.output(GreenLED, GPIO.LOW)
   GPIO.output(BlueLED, GPIO.HIGH)
  elif in_hum < 10: #par contre, si on est en bas du range, on allume BLEU brrr fait froid (sec dans ce cas)
   GPIO.output(RedLED, GPIO.HIGH)
   GPIO.output(GreenLED, GPIO.HIGH)
   GPIO.output(BlueLED, GPIO.LOW)
  elif in_hum > 20: #par contre, si on est en haut du range, on allume ROUGE danger trop humide!
   GPIO.output(RedLED, GPIO.LOW)
   GPIO.output(GreenLED, GPIO.HIGH)
   GPIO.output(BlueLED, GPIO.HIGH)
 
 elif out_temp > 10: #si temperature exterieur est en haut de 10
  if 30 <= in_hum <= 40: #si on est dans le bon range d'humidity, on allume VERT, on femer les autres au cas
   GPIO.output(RedLED, GPIO.HIGH)
   GPIO.output(GreenLED, GPIO.LOW)
   GPIO.output(BlueLED, GPIO.HIGH)
  elif in_hum < 30: #par contre, si on est en bas du range, on allume BLEU brrr fait froid (sec dans ce cas)
   GPIO.output(RedLED, GPIO.HIGH)
   GPIO.output(GreenLED, GPIO.HIGH)
   GPIO.output(BlueLED, GPIO.LOW)
  elif in_hum > 40: #par contre, si on est en haut du range, on allume ROUGE danger trop humide!
   GPIO.output(RedLED, GPIO.LOW)
   GPIO.output(GreenLED, GPIO.HIGH)
   GPIO.output(BlueLED, GPIO.HIGH)

out_temp = ReadExt()
humidity, temperature = ReadTemp()
UpdateLED(out_temp, humidity)
time2 = time.time() #used to get wheater from web api every 10 minutes

while 1:
 try:
  if humidity is not None and temperature is not None:
   display.writeDigit(0,int(temperature[0]), dot=False)
   display.writeDigit(1,int(temperature[1]), dot=True)
   display.writeDigit(3,int(temperature[3]), dot=False)
   #display.writeDigit(4,12) #Capital C
   #display.writeDigitRaw(4,88) #c miniscule
   display.writeDigitRaw(4,99) #signe degre
   time.sleep(5)
   display.writeDigit(0,int(humidity[0]), dot=False)
   display.writeDigit(1,int(humidity[1]), dot=True)
   display.writeDigit(3,int(humidity[3]), dot=False)
   display.writeDigitRaw(4,118) #Capital H
   #display.writeDigitRaw(4,116) #h minuscule
   time.sleep(5)
   humidity, temperature = ReadTemp()

   #read outsite every 10 minutes
   time1 = time.time()
   if float(time1) > float(time2)+600:
    out_temp = ReadExt()
    time2 = time.time()

   UpdateLED(out_temp, humidity) #update LED en dehors du IF car l'humidity peut changer meme si on relit pas la temp exterieur

 except KeyboardInterrupt:
  setting.clear()
  GPIO.cleanup()
  print ('User stopped program')
  raise
 except:
  print ('Something went really wrong')
setting.clear()
GPIO.cleanup()
