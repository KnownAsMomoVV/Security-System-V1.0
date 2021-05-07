#-*- coding:utf-8 -*-
#-------------------------------------------------Bibliotheken Importieren-------------------------------------------#

import RPi.GPIO as GPIO
import time
import blynklib
import runpy
import sys

#-------------------------------------------------Bibliotheken Importieren (END)-------------------------------------------#
#----------------------------------------------------------Blynk einbinden---------------------------------------------------#
BLYNK_AUTH = 'pi7uPXSmODTvKsaNvdt7IADPvI9cNF_j' #Auth Token einfügen
blynk = blynklib.Blynk(BLYNK_AUTH)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

#-------------------------------------------------------Blynk einbinden (END)------------------------------------------------#

# Texte formatieren und schöner gestalten
result = ""
header = ''
delimiter = '{}\n'.format('=' * 30)
# Texte formatieren und schöner gestalten (END)


#-------------------------------------------------GPIO Konfiguieren-------------------------------------------#

ledPin = 3
Number4 = "Pin_Nummer"

GPIO.setwarnings(False)     # GPIO einstellen und Board Anschlussweise (BCM oder BOARD)
GPIO.setmode(GPIO.BOARD)    #Warnungen austellen
GPIO.setup(3,GPIO.OUT)      # Pins Konfigurieren
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.output(3, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

#-------------------------------------------------GPIO Konfiguieren (END)-------------------------------------------#


#-----------------------------------------BLYNK button eingabe Virtual pins 4 & 6-------------------------------------------#
#-----------------------------------------BLYNK Steuerung für LED Manuell -------------------------------------------#
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

#-----------------------------------------BLYNK Steuerung für LED Manuell (END)-------------------------------------------#


#-------------------------------------------------Zurück zur Start datei---------------------------------------------#


@blynk.handle_event('write V6')
def write_handler(pin, values):

  if values and values[0] == "999":  #Passwort definieren
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
    w = ("falsches Password")   # Nachicht für falsches Passwort
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
    runpy.run_path(path_name='start_blynk.py')  #Starten der (BOOT) Datei


#-----------------------------------------BLYNK button eingabe Virtual pin 4 & 6 (END)-------------------------------------------#


#-------------------------------------------------Zurück zur Start datei (END)---------------------------------------------#


#-------------------------------------------------------Schleife--------------------------------------------------#
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
        blynk.email("ShiroYasha9@yandex.com",e_txt,txt)     #Email senden
        time.sleep(3)
        GPIO.output(3,0)
        GPIO.output(13,0)

#-------------------------------------------------------Schleife (END)--------------------------------------------------#

