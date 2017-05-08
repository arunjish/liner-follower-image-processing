from datetime import datetime 
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
import numpy as np
from motorControl import *
import sys
from functions import *

fdelay=0
tdelay=0

turn = False
turnDir="k"
turn_bottom_edge_count=0
turnLoop=False
turnOver=False

np.set_printoptions(threshold=np.nan)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
#camera.resolution = (250,250)
camera.resolution = (640,480)
camera.framerate = 14
#rawCapture = PiRGBArray(camera, size=(250, 250))
rawCapture = PiRGBArray(camera, size=(640,480))
# allow the camera to warmup
time.sleep(1)
count=0
skipped_frame=False
initial_skip=5
skip_frame_count=0
direction="k"

path=['l','s','r','s']
front=0


rta=0
lta=0
pj=0
tj=0
rtj=0
ltg=0

def junctionControl():
	global front
	global turn
	global turnDir
	print " *********************************************************** junction control *************************************" + path[front]
	if path[front]=='r':
		turn=True
                turnDir="r"
	elif path[front]=='l':
                turn=True
                turnDir="l"
	elif path[front]=='s':
		forward(1)
		stop(0)

	front+=1

def directBot(frame_res,edge):
        top_l,mid,top_r,top_line,bottom_line=frame_res
        mid_edge_count,mid_centre=mid
        top_l_edge_count,top_l_centre=top_l
        top_r_edge_count,top_r_centre=top_r
        top_line_edge_count,top_line_centre=top_line
        bottom_line_edge_count,bottom_line_centre=bottom_line
        global turn
        global turnDir
        global turn_bottom_edge_count
        global mid1corrected
        global bottom1corrected
        global mid2corrected
	global rta
	global lta
	global pj
        global tj
        global rtj
        global ltj

        if top_l_edge_count>0 and 0< top_r_edge_count <=2 and top_line_edge_count==2 :
                printFrame(edge)
	
		print "plus junction"
		junctionControl()
		#exit()
                #forward(fdelay)

               # diffRight(tdelay)
        elif top_l_edge_count==2 and  top_line_edge_count ==2 and top_r_edge_count==0:
		rta=0
		lta=0
		pj=0
		tj=0
		rtj=0
		ltj+=1

		printFrame(edge)
		if ltj>2:
			print "left T junction"
			ltj=0
			junctionControl()
		#exit()
                


        elif top_r_edge_count==2 and top_line_edge_count==2 and top_l_edge_count==0 :
		rta=0
                lta=0
                pj=0
                tj=0
                rtj+=1
                ltj=0
		printFrame(edge)
		if rtj>2:
			print "right T junction"
			rtj=0
			junctionControl()
		#exit()
                
        elif top_l_edge_count>0  and top_r_edge_count>0:
                printFrame(edge)
		rta=0
                lta=0
                pj=0
                tj+=1
                rtj=0
                ltj=0
 		if tj>2:
			print "T junction"
			tj=0
			junctionControl()
	
        elif top_l_edge_count>1  and bottom_line_edge_count>0 and top_r_edge_count==0  :
		rta+=1
		lta=0
                printFrame(edge)
		print "rta ==            ===     " + str(rta)
		print "arunnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
		if rta>2: 
			print "\t\t\\t\t\t\t\t\t\t\t\t\t\tleft turn Ahead"
		
                	turn=True
                	turnDir="l"
			rta=0
        elif top_l_edge_count ==0 and bottom_line_edge_count>0 and top_r_edge_count>1 :
		lta+=1
		rta=0
		printFrame(edge)

		if lta>2:
			print "\t\t\t\t\t\t\t\t\t\t\t\tright turn detected"
		
                	turn=True
                	turnDir="r"
			lta=0
	
        elif 0<bottom_line_centre<200:
                diffLeft(.01)
                stop(0)
        elif 200<=bottom_line_centre<=210:
                forward(.15)
                stop(0)
        elif 210<bottom_line_centre<=400:
                diffRight(.01)
                stop(0)

	else :
		rta=0
		lta=0


def makeBottomOk():

	if 0<bottom_line_centre<190:
                diffLeft(.01)
                stop(0)
        elif 210<bottom_line_centre<=400:
                diffRight(.01)
                stop(0)
def makeMidOk():

	if 0<mid_centre<190:
                diffLeft(.01)
                stop(0)
        elif 210<mid_centre<=400:
                diffRight(.01)
                stop(0)

def isMidOk():
        if 190<=mid_centre<=210:
                return True
        else:
                return False



def isBottomOk():
	if 190<=bottom_line_centre<=210:
		return True       
        else:
        	return False

def isBottomOk_after_turn(dir):
	
        if 190<=bottom_line_centre and bottom_line_edge_count==2:
                return True
        else:
                return False



try:
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		t1 = datetime.now()

		if initial_skip >0:
			initial_skip-=1
			print "initial skip"
			rawCapture.truncate(0)
			continue
		if skip_frame_count>0:
			skip_frame_count-=1
			rawCapture.truncate(0)
			continue		

		img_RGB = frame.array
		img_RGB=cv2.resize(img_RGB,(400,400))
		img_RGB = img_RGB[0:220, 0:400]
		edge=cv2.Canny(img_RGB,100,200)
		#printFrame(edge)
		frame_res= checkFrame(edge)
		print "\n\n\t\t Top-L |  Mid | Top-R | Top-Line |  Bottom Line  "
		print "\t\t"+ str(frame_res)+"\n\n"
		#rawCapture.truncate(0)
		#continue
		top_l,mid,top_r,top_line,bottom_line=frame_res
	        mid_edge_count,mid_centre=mid
	        top_l_edge_count,top_l_centre=top_l
	        top_r_edge_count,top_r_centre=top_r
		top_line_edge_count,top_line_centre=top_line
		bottom_line_edge_count,bottom_line_centre=bottom_line
		#directBot(frame_res)

		if turn==True :
			if  isBottomOk():
                                print "\t\t\t\t\t\t\tPre Turn Correction compleated"
				if turnDir=="l":
					dist= (float(bottom_line_centre-top_l_centre))/200
					if dist<.4:
						dist=.4
					if dist>.7:
						dist=.6				
	                                print dist
        	                        forward(dist)
                	                stop(0)

                                	diffLeft(.4)
					forward(.2)
                                	stop(0)
                        	if turnDir=="r":
					dist= (float(bottom_line_centre-top_r_centre))/200
	                                if dist<.4:
                                                dist=.4
                                        if dist>.7:
                                                dist=.6

					print dist
        	                        forward(dist)
                	                stop(0)

                                	diffRight(.4)
					forward(.2)
                                	stop(0)
				turn=False
				turnLoop=True
                                t2 = datetime.now()
                                delta=t2-t1 
                                skip_frame_count=int(delta.microseconds/100000)+2
			

                                rawCapture.truncate(0)
                                continue
                        else:
                                print "\t\t\t\t\t\tPre turn bottom  correcting...."
				makeBottomOk()

              
		if turnLoop==True:
			print turnDir
			if isBottomOk_after_turn(turnDir):
                                turnLoop=False
                                turnOver=True
                                print "\t\t\t\t\t\t\tTurn over"
                           
			if turnDir=="l":
				diffLeft(.02)   
                        	stop(0)   	
			if turnDir=="r":
                                diffRight(.02)
				stop(0)
			t2 = datetime.now()
	                delta=t2-t1

        	        skip_frame_count=int(delta.microseconds/100000)

			rawCapture.truncate(0)
                        continue

		if turnOver==True:
			
			if  isMidOk():
                                print "\t\t\t\t\t\t\t\t\t\t\tPost Turn Correction compleated"
                                turnOver=False
                                t2 = datetime.now()
                                delta=t2-t1

                                skip_frame_count=int(delta.microseconds/100000)


                                rawCapture.truncate(0)
                                continue
                        else:
                                print "\t\t\t\t\t\t\t\t\t\t\tPost turn bottom  correcting...."

                                makeMidOk()

						
		if not turn and not turnLoop and not turnOver:
			directBot(frame_res,edge)
	
		t2 = datetime.now()
                delta=t2-t1
		
		skip_frame_count=int(delta.microseconds/100000)
		
	
		rawCapture.truncate(0)

except KeyboardInterrupt:
	print "Goodbye"
	stop(0)
	exit()
		
