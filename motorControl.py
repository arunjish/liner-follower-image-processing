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

def forward(delay):
	GPIO.output(ML1, True)
        GPIO.output(ML2, False)

        GPIO.output(MR1, True)
        GPIO.output(MR2, False)
	time.sleep(delay)
        print "forward"
def backward(delay):
	GPIO.output(ML2, True)
        GPIO.output(ML1, False)

        GPIO.output(MR2, True)
        GPIO.output(MR1, False)

	time.sleep(delay)
        print "Backwords"

def left(delay):
        GPIO.output(ML1, True)
        GPIO.output(ML2, False)

        GPIO.output(MR1, False)
        GPIO.output(MR2, False)
        print "left"

def right(delay):
        GPIO.output(ML1, False)
        GPIO.output(ML2, False)

        GPIO.output(MR1, True)
        GPIO.output(MR2, False)

	time.sleep(delay)
        print "right"

def stop():
        GPIO.output(ML1, False)
        GPIO.output(ML2, False)

        GPIO.output(MR1, False)
        GPIO.output(MR2, False)
        print "Stop"

