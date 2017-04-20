import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

ML1= 14
ML2= 15

MR1= 23
MR2= 24

GPIO.setup(ML1,GPIO.OUT)
GPIO.setup(ML2,GPIO.OUT)
GPIO.setup(MR1,GPIO.OUT)
GPIO.setup(MR2,GPIO.OUT)


def forward(step,step_delay):
	GPIO.output(ML1, True)
	GPIO.output(MR1, False)
	time.sleep(step_delay)

	for i in range(0,step):
        	GPIO.output(ML2, True)
        	GPIO.output(MR2, True)

        	time.sleep(step_delay)
        	GPIO.output(ML2, False)
        	GPIO.output(MR2, False)

        	time.sleep(step_delay)
        print str(step)+"  steps  forward"
def backward(step,step_delay):
        GPIO.output(ML1, False)
        GPIO.output(MR1, True)
	time.sleep(step_delay)
	
        for i in range(0,step):
                GPIO.output(ML2, True)
                GPIO.output(MR2, True)

                time.sleep(step_delay)
                GPIO.output(ML2, False)
                GPIO.output(MR2, False)

                time.sleep(step_delay)
        print "backward"

def diffRight(step,step_delay):
        GPIO.output(ML1, True)
        GPIO.output(MR1, True)
        time.sleep(step_delay)
	print str(step) + " steps diff right"

        for i in range(0,step):
                GPIO.output(ML2, True)
                GPIO.output(MR2, True)

                time.sleep(step_delay)
                GPIO.output(ML2, False)
                GPIO.output(MR2, False)

                time.sleep(step_delay)
        
def diffLeft(step,step_delay):
        GPIO.output(ML1, False)
        GPIO.output(MR1, False)
        time.sleep(step_delay)
	print str(step) +" steps diff left"
        for i in range(0,step):
		

                GPIO.output(ML2, True)
                GPIO.output(MR2, True)

                time.sleep(step_delay)
                GPIO.output(ML2, False)
                GPIO.output(MR2, False)

                time.sleep(step_delay)
        
def left(step,step_delay):
        GPIO.output(ML1, False)
        GPIO.output(MR1, False)
        time.sleep(step_delay)

        for i in range(0,step):
               # GPIO.output(ML2, True)
                GPIO.output(MR2, True)

                time.sleep(step_delay)
                #GPIO.output(ML2, False)
                GPIO.output(MR2, False)

                time.sleep(step_delay)
        print str(step) +"step left"

def right(step,step_delay):
        GPIO.output(ML1, True)
        GPIO.output(MR1, False)
        time.sleep(step_delay)

        for i in range(0,step):
               	GPIO.output(ML2, True)
                #GPIO.output(MR2, True)

                time.sleep(step_delay)
                GPIO.output(ML2, False)
                #GPIO.output(MR2, False)

                time.sleep(step_delay)
        print str(step) +"step right"



