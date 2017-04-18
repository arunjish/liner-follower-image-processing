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


def forward(num):
	GPIO.output(ML1, True)
	GPIO.output(MR1, False)

	for i in range(0,num*200):
        	GPIO.output(ML2, True)
        	GPIO.output(MR2, True)

        	time.sleep(.004)
        	GPIO.output(ML2, False)
        	GPIO.output(MR2, False)

        	time.sleep(.004)
        print "forward"
forward(2)

"""
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
	time.sleep(delay)
        print "left"

def right(delay):
        GPIO.output(ML1, False)
        GPIO.output(ML2, False)

        GPIO.output(MR1, True)
        GPIO.output(MR2, False)

	time.sleep(delay)
        print "right"

def stop(delay):
        GPIO.output(ML1, False)
        GPIO.output(ML2, False)

        GPIO.output(MR1, False)
        GPIO.output(MR2, False)
        print "Stop"
	time.sleep(delay)

def diffLeft(delay):
	GPIO.output(ML1, True)
        GPIO.output(ML2, False)

        GPIO.output(MR1, False)
        GPIO.output(MR2, True)
        print "\t diff---left"
	time.sleep(delay)

def diffRight(delay):
        GPIO.output(ML1, False)
        GPIO.output(ML2, True)

        GPIO.output(MR1, True)
        GPIO.output(MR2, False)
        print "\t diff---Right"
        time.sleep(delay)


def follow_previous_direction(direction):
                        if direction=="r":
                                right(0)
                                time.sleep(0.05)
                                stop()
                        elif direction=="l":
                                left(0)
                                time.sleep(0.05)
                                stop()



def directRobot(count_b_top,count_b_bottom,count_b_left,count_b_right,skipped_frame,direction):

                print "\n\n-------------------------------------------------------------------------------------------------------------\n"
                print "\t\t\t top = "+ str(count_b_top)
                print "left = "+str(count_b_left)
                print "\t\t\t\t\t\tright =  "+ str(count_b_right)
                print "\t\t\tbottom = "+str(count_b_bottom)

                

                if count_b_top > 70 and count_b_bottom > 70 and count_b_left < 70 and count_b_right < 70:
                        forward(0)
                        direcrion="f"
                elif count_b_bottom>70 and count_b_right>70 and skipped_frame:
                        right(0)
                        direction="r"
                elif  count_b_left>70 and not skipped_frame:
                        left(0)
                        direction="l"
                        time.sleep(0.05)
                        stop()
                elif count_b_right>70 and not skipped_frame:
                        right(0)
                        direction="r"
                        time.sleep(0.05)
                        stop()
                elif count_b_top < 70 and count_b_bottom < 70 and count_b_left < 70 and count_b_right < 70:
                        print "full white"
                        follow_previous_direction()

                else :
                        print "unkonwn condition"
                        follow_previous_direction()
                       # stop()


                print "\n\n-------------------------------------------------------------------------------------------------------------\n\n"

                
"""

