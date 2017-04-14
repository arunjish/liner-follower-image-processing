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

def forward():
	GPIO.output(ML1, True)
        GPIO.output(ML2, False)

        GPIO.output(MR1, True)
        GPIO.output(MR2, False)
        print "forward"
def backward():
	GPIO.output(ML2, True)
        GPIO.output(ML1, False)

        GPIO.output(MR2, True)
        GPIO.output(MR1, False)
        print "Backwords"

def right():
        GPIO.output(ML1, True)
        GPIO.output(ML2, False)

        GPIO.output(MR1, False)
        GPIO.output(MR2, False)
        print "Right"

def left():
        GPIO.output(ML1, False)
        GPIO.output(ML2, False)

        GPIO.output(MR1, True)
        GPIO.output(MR2, False)
        print "left"

def stop():
        GPIO.output(ML1, False)
        GPIO.output(ML2, False)

        GPIO.output(MR1, False)
        GPIO.output(MR2, False)
        print "Stop"

