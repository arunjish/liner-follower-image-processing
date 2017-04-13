import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

ML1= 17
ML2= 27

MR1= 23
MR2= 24

GPIO.setup(ML1,GPIO.OUT)
GPIO.setup(ML2,GPIO.OUT)
GPIO.setup(MR1,GPIO.OUT)
GPIO.setup(MR2,GPIO.OUT)

while True :

	GPIO.output(ML1, True)
	GPIO.output(ML2, False)

	GPIO.output(MR1, True)
	GPIO.output(MR2, False)
	print "forward"  
	time.sleep(5)

	GPIO.output(ML2, True)
        GPIO.output(ML1, False)

        GPIO.output(MR2, True)
        GPIO.output(MR1, False)
	print "Backwords"
	time.sleep(5)

