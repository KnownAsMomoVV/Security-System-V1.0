import RPi.GPIO as GPIO
import time
import blynklib
import runpy
import sys

BLYNK_AUTH = 'pi7uPXSmODTvKsaNvdt7IADPvI9cNF_j' #insert your Auth Token here
blynk = blynklib.Blynk(BLYNK_AUTH)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

# Texte formatieren und schöner gestalten
result = ""
header = ''
delimiter = '{}\n'.format('=' * 30)
# Texte formatieren und schöner gestalten (END)

ledPin = 3
Number4 = "Pin_Nummer"


#GPIO Konfigurieren

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT) 
GPIO.setup(11,GPIO.IN)
#GPIO.setup(12,GPIO.IN)
#GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.output(3, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

#GPIO.output(12,GPIO.HIGH)
#GPIO.input(12)


#GPIO Konfigurieren
#BLYNK button eingabe Virtual pin 4
#BLYNK button eingabe Virtual pin 4

@blynk.handle_event('write V4')
def write_virtual_pin_handler1(pin, value):

    if value == ["1"]:
        print(Number4,pin)
        print("LED AN")
        GPIO.output(ledPin,GPIO.LOW)
    else:
        print(Number4,pin)
        print("LED AUS")
        GPIO.output(ledPin,GPIO.HIGH)

#BLYNK button eingabe Virtual pin 4

#BLYNK button eingabe Virtual pin 4

@blynk.handle_event('write V5')
def write_virtual_pin_handler2(pin, value):
    if value == ["999"]:
        sys.exit()


#BACK TO START FILE-----------------------------------------------------------------------------------

#BACK TO START FILE-----------------------------------------------------------------------------------

@blynk.handle_event('write V6')
def write_handler(pin, values):

  if values and values[0] == "999":
    result = values
    result1_5="Richtiges passwort, starte Boot datei \n"
    result2 = "Starte Boot datei\n"
  elif values and values[0] == "usage":
    usage = ("""             __  
           / _ )/ /_ _____  / /__
          / _  / / // / _ \/  '_/
         /____/_/\_, /_//_/_/\_\
                /___/
                      for Python v0.2.6""")


    blynk.virtual_write(pin,usage)
  else:
    w = ("falsches Password")
    blynk.virtual_write(pin,w)
    print(w)
  if result:
    output = '{}{}{}{}'.format(header, delimiter, result1_5, delimiter)
    output2 = '{}{}{}{}'.format(header, delimiter, result2, delimiter)
    sucess = "Datei gestartet\n"
    blynk.virtual_write(pin,output)
    print(output)
    time.sleep(3)
    blynk.virtual_write(pin,output2)
    print(output2)
    time.sleep(5)
    blynk.virtual_write(pin,sucess)
    runpy.run_path(path_name='start_blynk.py')




#BACK TO START FILE-----------------------------------------------------------------------------------
#BACK TO START FILE-----------------------------------------------------------------------------------



while True:
    blynk.run()


    IRR=GPIO.input(11)
    bz=GPIO.input(13)
    
    txt = ""
    e_txt="Alarm wurde AUSGELÖST"

    if IRR==0:
        GPIO.output(3,1)
        GPIO.output(13,1)
        print ("Bewegung erkannt, sende signal")
        time.sleep(0.5)
        blynk.notify('ALARM AUSGELÖST.')
        blynk.email("ShiroYasha9@yandex.com",e_txt,txt)
        time.sleep(3)
        GPIO.output(3,0)
        GPIO.output(13,0)

