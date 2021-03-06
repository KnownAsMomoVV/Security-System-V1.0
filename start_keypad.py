#-------------------------------------------------Bibliotheken Importieren-------------------------------------------#

import RPi.GPIO as GPIO
import time
import runpy

#-------------------------------------------------Bibliotheken Importieren (END)-------------------------------------------#


# Texte formatieren und schöner gestalten
psw_abfrage = "Bitte gebe das Passwort ein um die Alarmanlage zu starten: \n"
r_p = "Richtges passwort schalte alarmanlage AUS\n"
wrng = "Das Password ist falsch\n"
stt = "Boot datei gestartet\n"

header = ''
delimiter = '{}\n'.format('=' * 30)

psw_ab = '{}{}{}{}'.format(header, delimiter, psw_abfrage, delimiter)
r_psw = '{}{}{}{}'.format(header, delimiter, r_p, delimiter)
st = '{}{}{}{}'.format(header, delimiter, stt, delimiter)
wrong = '{}{}{}{}'.format(header, delimiter, wrng, delimiter)
# Texte formatieren und schöner gestalten (END)

#----------------------------HAUPTTEIL----------------------------#

print (st)
time.sleep(5)

#-------------------------------------------------GPIO Konfiguieren-------------------------------------------#

# GPIO einstellen und Board Anschlussweise (BCM oder BOARD)
GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)         #Warnungen austellen

# GPIO eingänge für das Keypad angeben
S = [40,38,36,32] # Seule (Pins) für die Vertikalen Buttons
R = [37,35,33,31] # Reihe (Pins) für die Horizontalen Buttons

#-------------------------------------------------GPIO Konfiguieren (END)-------------------------------------------#

for j in range(4): # Hierbe kann man jeden buchstaben verwenden (Jedoch ist j & i das häufigst verwendete)
    GPIO.setup(S[j], GPIO.OUT)
    GPIO.output(S[j], 1)
for i in range(4):
    GPIO.setup(R[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

#-----------------------------------------Keypad eingabe erkennen -----------------------------------#
#Das Überprüfen der eingabe des Keypads
def check_keypad(length):
    MATRIX = [ [1,4,7,"*"],
               [2,5,8,0],
               [3,6,9,"#"],
               ["A","B","c","D"] ]
    result = ""
    while(True):            #Temporäre Schleife
        for j in range(4):
            GPIO.output(S[j], 0)

            for i in range(4):
                if GPIO.input(R[i]) == 0:
                    time.sleep(0.02)
                    result = result + (str(MATRIX[i][j]))
                    while(GPIO.input(R[i]) == 0):
                          time.sleep(0.02)

            GPIO.output(S[j], 1)
            if len(result) >= length:
                return result
#-----------------------------------------Keypad eingabe erkennen (END)------------------------------#


# Das password angeben
password = "A1234"  
length = len(password)

# Die Startnachicht angeben
print(psw_ab)
result = check_keypad(length)   # Auf länge prüfen




#-------------------------------------------------------Schleife--------------------------------------------------#

while True:
    if result == password:      #Passwort abfrage
        print(result)
        print("Korrekt ")
        time.sleep(3)
        runpy.run_path(path_name='tp_keypad.py')  #Starten der (MAIN) Datei
    else:
        print(result)
        time.sleep(1)
        print(wrong) 
        runpy.run_path(path_name='start_keypad.py')   #Starten der (BOOT) Datei

#-------------------------------------------------------Schleife (END)--------------------------------------------------#


#------------------------------ENDE-------------------------------#
