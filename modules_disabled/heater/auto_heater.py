import datetime, time
from models import Sensors

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


min_temp = 21.5
max_temp = 23
gpioID = 24





#set relay config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioID, GPIO.OUT)

lastStatus = True
setEnable = False

while True:
  date = datetime.datetime.today()

  #turn off during the night
  silenthours = range(0,11)
  silenthours = silenthours + range(20,24)


  if date.weekday() not in [5,6]:
     silenthours = silenthours + range(11,13)
  print silenthours

  print date
  if date.hour not in silenthours:
     internal_temp = Sensors().getLast();
     internal_temp = internal_temp[1]

     print internal_temp
     
     if setEnable:
         if internal_temp > max_temp-1:
            setEnable = False
     else:
         if internal_temp < min_temp:
            setEnable = True
  else:
     setEnable = False
     print "offline time"

  print setEnable

  if setEnable != lastStatus :
     if setEnable:
        GPIO.output(gpioID, GPIO.LOW)
     else:
        GPIO.output(gpioID, GPIO.HIGH)
     lastStatus = setEnable

  time.sleep(60 * 5)
     
  
