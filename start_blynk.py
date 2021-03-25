#-------------------------------------------------Bibliotheken Importieren-------------------------------------------#

import RPi.GPIO as GPIO
import time
import blynklib
import runpy

#-------------------------------------------------Bibliotheken Importieren (END)-------------------------------------------#
#----------------------------------------------------------Blynk einbinden---------------------------------------------------#


BLYNK_AUTH = 'pi7uPXSmODTvKsaNvdt7IADPvI9cNF_j' #Auth Token einfügen
blynk = blynklib.Blynk(BLYNK_AUTH)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

#-------------------------------------------------------Blynk einbinden (END)------------------------------------------------#

#-------------------------------------------------GPIO Konfiguieren-------------------------------------------#

GPIO.setmode (GPIO.BOARD)   # GPIO einstellen und Board Anschlussweise (BCM oder BOARD)
GPIO.setwarnings(False)     #Warnungen austellen

#-------------------------------------------------GPIO Konfiguieren (END)-------------------------------------------#

#-----------------------------------------BLYNK button eingabe Virtual pins 6-------------------------------------------#
#------------------------------------------------- Starten der Hauptdatei ---------------------------------------------#

@blynk.handle_event('write V6')
def write_handler(pin, values):
    result = ""
    header = ''
    delimiter = '{}\n'.format('=' * 30)
    if values and values[0] == "1234":      #Passwort abfrage
        result = ("Richtiges passwort, starte Hauptdatei \n")
        result2 = ("Haupdatei wird gestartet\n")
    else:
        w = ("        falsches password")
        blynk.virtual_write(pin,w)
        print(w)
    if result:
        output = '{}{}{}{}'.format(header, delimiter, result, delimiter)
        output2 = '{}{}{}{}'.format(header, delimiter, result2, delimiter)
        sucess = "                             Datei gestartet"
        blynk.virtual_write(pin,output)
        print(output)
        time.sleep(3)
        blynk.virtual_write(pin,output2)
        print(output2)
        time.sleep(5)
        blynk.virtual_write(pin,sucess)
        runpy.run_path(path_name='tp_blynk.py') #Starten der (MAIN) Datei

#-------------------------------------------------Starten der Hauptdatei (END)---------------------------------------------#
#-----------------------------------------BLYNK button eingabe Virtual pin 6 (END)-------------------------------------------#
        

#-------------------------------------------------------Schleife--------------------------------------------------#
while True:
    blynk.run()
#-------------------------------------------------------Schleife (END)--------------------------------------------------#
