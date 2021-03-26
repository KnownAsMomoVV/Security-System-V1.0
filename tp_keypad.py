#-------------------------------------------------Bibliotheken Importieren-------------------------------------------#

import RPi.GPIO as GPIO
import time
import blynklib
import runpy

#-------------------------------------------------Bibliotheken Importieren (END)-------------------------------------------#
# Texte formatieren und schöner gestalten
psw_abfrage = "Bitte gebe das Password ein falls du die Anlage auschalten möchtest: \n"
r_p = "Richtges passwort schalte alarmanlage AUS\n"
stt = "Die alarmanlage ist Gestartet und einsatzbereit\n"

header = ''
delimiter = '{}\n'.format('=' * 30)

psw_ab = '{}{}{}{}'.format(header, delimiter, psw_abfrage, delimiter)
r_psw = '{}{}{}{}'.format(header, delimiter, r_p, delimiter)
st = '{}{}{}{}'.format(header, delimiter, stt, delimiter)
# Texte formatieren und schöner gestalten (END)

print(st)   # Start Nachicht
time.sleep(4)



#-------------------------------------------------GPIO Konfiguieren-------------------------------------------#
IRC = 11
GPIO.setwarnings(False)   #GPIO einstellen und Board Anschlussweise (BCM oder BOARD)
GPIO.setmode(GPIO.BOARD)  #Warnungen austellen
GPIO.setup(3,GPIO.OUT)    #Pins Konfigurieren
GPIO.setup(IRC, GPIO.IN)
GPIO.input(IRC)
GPIO.setup(13,GPIO.OUT)
GPIO.output(3, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
#-------------------------------------------------GPIO Konfiguieren (END)-------------------------------------------#
# Keypad inputs bestimmen
SL = [40,38,36,32] # Die GPIO inputs für die Vertikale achse (Für das Keypad)
RH = [37,35,33,31] # Die GPIO inputs für die Horizontale achse (Für das Keypad)
# Keypad inputs bestimmen (END)

# Eine variable für die Länge auswählen
for j in range(4):    # Hierbe kann man jeden buchstaben verwenden (Jedoch ist j & i das häufigst verwendete)
    GPIO.setup(SL[j], GPIO.OUT)
    GPIO.output(SL[j], 1)
for i in range(4):
    GPIO.setup(RH[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
#Keypad einstellen


#-----------------------------------------Keypad eingabe erkennen -----------------------------------#
#Das Überprüfen der eingabe des Keypads
def check_keypad(length):
    COL = [40,38,36,32]
    ROW = [37,35,33,31]
    MATRIX = [ [1,4,7,"*"],
               [2,5,8,0],
               [3,6,9,"#"],
               ["A","B","c","D"] ]
    result = ""
    while(True):    #Temporäre Schleife
        for j in range(4):
            GPIO.output(COL[j], 0)
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    time.sleep(0.02)
                    result = result + (str(MATRIX[i][j]))
                    while(GPIO.input(ROW[i]) == 0):
                          time.sleep(0.02)
            GPIO.output(COL[j], 1)
            if len(result) >= length:
                return result
            elif GPIO.input(IRC) == 0: # Infrarot sensor erkennung
                  GPIO.output(3,1)  #LED ein
                  GPIO.output(13,1) #Buzzer ein
                  print ("Bewegung erkannt, sende signal")
                  time.sleep (4)
                  GPIO.output(3,0)  #LED aus
                  GPIO.output(13,0) #Buzzer aus
                  time.sleep(0.5)

#-----------------------------------------Keypad eingabe erkennen (END)------------------------------#

password = "1337"   #Passwort definieren
length = len(password)    
print(psw_ab)
result = check_keypad(length)   # Passwort auf länge prüfen
txt = ""
e_txt="Alarm wurde AUSGELÖST"

#-------------------------------------------------------Schleife--------------------------------------------------#

while True:
  if result == password:    #Passwort richtig
    print(result)
    print(r_psw)
    GPIO.output(3,1)
    time.sleep(3)
    GPIO.output(3,0)
    runpy.run_path(path_name='start_keypad.py')    #Starten der (BOOT) Datei
  elif result != password:    #Passwort falsch
    print ("Starte code neu")
    time.sleep(3)
    print (result)
    runpy.run_path(path_name="tp_keypad.py")  #Starten der (MAIN) Datei
    

#-------------------------------------------------------Schleife (END)--------------------------------------------------#
