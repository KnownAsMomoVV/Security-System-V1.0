import RPi.GPIO as GPIO
import time
import blynklib
import runpy

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

print(st)
time.sleep(4)

IRC = 11

#GPIO Konfigurieren
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT) 
GPIO.setup(IRC, GPIO.IN)
GPIO.input(IRC)
GPIO.setup(13,GPIO.OUT)
GPIO.output(3, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
#GPIO Konfigurieren (END)

# Keypad inputs bestimmen
SL = [40,38,36,32] # Die GPIO inputs für die Vertikale achse (Für das Keypad)
RH = [37,35,33,31] # Die GPIO inputs für die Horizontale achse (Für das Keypad)
# Keypad inputs bestimmen (END)

# Eine variable 
for j in range(4):
    GPIO.setup(SL[j], GPIO.OUT)
    GPIO.output(SL[j], 1)
for i in range(4):
    GPIO.setup(RH[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)



def check_keypad(length):
    COL = [40,38,36,32]
    ROW = [37,35,33,31]
    MATRIX = [ [1,4,7,"*"],
               [2,5,8,0],
               [3,6,9,"#"],
               ["A","B","c","D"] ]
    result = ""
    while(True):
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
            elif GPIO.input(IRC) == 0:
                  print("test")
                  time.sleep(1)



password = "1337"
length = len(password)
print(psw_ab)
result = check_keypad(length)
#BACK TO START FILE-----------------------------------------------------------------------------------
#BACK TO START FILE-----------------------------------------------------------------------------------
txt = ""
e_txt="Alarm wurde AUSGELÖST"

while True:
  if result == password:
    print(result)
    print(r_psw)
    GPIO.output(3,1)
    time.sleep(3)
    GPIO.output(3,0)
    runpy.run_path(path_name='start_keypad.py')
  elif result != password:
    print ("Restarting code")
    print (result)
    runpy.run_path(path_name="tp_keypad.py")
    

