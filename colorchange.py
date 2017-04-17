from datetime import datetime 
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
import numpy as np

from motorControl import *
import sys

fdelay=0
tdelay=0

turn = False
turnDir="k"
turn_bottom_edge_count=0
turnLoop=False
np.set_printoptions(threshold=np.nan)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (250,250)
camera.framerate = 14
rawCapture = PiRGBArray(camera, size=(250, 250))
# allow the camera to warmup
time.sleep(1)
count=0
skipped_frame=False
initial_skip=5
skip_frame_count=0
direction="k"


def checkFrame(edgex):
      	m_y1=0
       	m_y2=0
        mid_edge_count=0
	top_l_edge_count=0
	top_r_edge_count=0
	top_line_edge_count=0
	top_r_centre=0
	top_l_centre=0
	bottom_line_edge_count=0
        for i in range(0,240):
                if edgex[125][i]==255:
                        mid_edge_count+=1
                        if mid_edge_count==1:
                               m_y1=i
                        elif mid_edge_count==2:
                               m_y2=i
		if edgex[i+10][10]==255:
                        top_l_edge_count+=1
			if top_l_edge_count==1:
                               top_l_centre=i
                        elif top_l_edge_count==2:
                		top_l_centre=int((top_l_centre+i)/2)
		if edgex[i+10][240]==255:
                        top_r_edge_count+=1
			if top_r_edge_count==1:
                               top_r_centre=i
                        elif top_r_edge_count==2:
                                top_r_centre=int((top_r_centre+i)/2)

		if edgex[0][i]==255:
			top_line_edge_count+=1
		if edgex[249][i]==255:
                        bottom_line_edge_count+=1

	mid_centre=int((m_y1+m_y2)/2)
	return ((top_l_edge_count,top_l_centre),(mid_edge_count,mid_centre),(top_r_edge_count,top_r_centre),top_line_edge_count,bottom_line_edge_count)


def directBot(frame_res):
	top_l,mid,top_r,top_line_edge_count,bottom_line_edge_count=frame_res
	mid_edge_count,mid_centre=mid
	top_l_edge_count,top_l_centre=top_l
	top_r_edge_count,top_r_centre=top_r
	global turn
	global turnDir
	global turn_bottom_edge_count
	#if  not 0<mid_edge_count<=2:
	#	print " previous"

	#	stop(0)
	if top_l_edge_count==2 and top_r_edge_count==2 and top_line_edge_count==2 :
		print "plus junction"
		forward(fdelay)
                #stop(2)
                diffRight(tdelay)
                stop(0)

		stop(2)
	elif top_l_edge_count==2 and top_line_edge_count==2 and top_r_edge_count==0:
                print "left T junction"
		forward(fdelay)
                #stop(3)
                diffLeft(tdelay)
                stop(0)

                stop(2)
	elif top_r_edge_count==2 and top_line_edge_count==2 and top_l_edge_count==0 :
                print "right T junction"
		forward(fdelay)
                #stop(2)

	elif top_l_edge_count==2 and top_line_edge_count==2 and top_r_edge_count==2:
		print "T junction"
		forward(fdelay)
                #stop(2)
                diffLeft(tdelay)
                stop(0)

	elif top_l_edge_count==2 and top_r_edge_count==0  :
		print "left turn Ahead"
		turn=True
		turnDir="l"
		turn_bottom_edge_count=0
		forward(0)
	elif top_l_edge_count ==0 and  top_r_edge_count==2:
		print "right turn detected"
		forward(fdelay)
                #stop(2)
                diffRight(tdelay)
                turn=True

	elif 0<mid_centre<=83:
		left(.2)
		stop(0)
	elif 83<mid_centre<=166:
		forward(0)
	elif 166<mid_centre<=249:
		right(.2)
		stop(0)
		


def printFrame(im_bw):
	for x in range(0,250):
		
		row_count_black=0
		row_count_white=0
		sys.stdout.write(str(x)+ " : ")
        	for y in range(0,250):
                	if im_bw[x][y] == 0 :
                        	sys.stdout.write("#")
				row_count_black+=1
                        else:
                        	sys.stdout.write(".")
				row_count_white+=1
		sys.stdout.write(" : W = "+str(row_count_white)+": B =  "+str(row_count_black))
                sys.stdout.write("\n")
	sys.stdout.write("\n----------------------------------------------------------------------------------> \n\n")
try:
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		t1 = datetime.now()
		
		if initial_skip >0:
			initial_skip-=1
			print "initial skip"
			rawCapture.truncate(0)
			continue
		#skip_frame_count=0
		if skip_frame_count>0:
			skip_frame_count-=1
			print "skipp frame"
			rawCapture.truncate(0)
			continue	
		
		img_RGB = frame.array
		edge=cv2.Canny(img_RGB,100,200)
		
		#printFrame(edge)
		frame_res= checkFrame(edge)
		print frame_res

		top_l,mid,top_r,top_line_edge_count,bottom_line_edge_count=frame_res
	        mid_edge_count,mid_centre=mid
	        top_l_edge_count,top_l_centre=top_l
	        top_r_edge_count,top_r_centre=top_r

		
		if turn==True :
			if bottom_line_edge_count ==0 :
				turn_bottom_edge_count+=1
				if turn_bottom_edge_count>8:
					diffLeft(0)
					turnLoop=True
					turn=False
			
		if turnLoop==True:
			print frame_res
			if  top_l_edge_count>0 or top_r_edge_count>0:
				stop(0)
				print " Turn over"
				turnLoop=False
				
	
		if turn==False and turnLoop==False:
			directBot(frame_res)
		t2 = datetime.now()
                delta=t2-t1
		
		skip_frame_count=int(delta.microseconds/100000)
		
               # print "\n\n\n"+str(skip_frame_count)+"\n\n\n"

		#img_gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)
		#print img_gray
		#(thresh, im_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		#(thresh1, im_bw1) = cv2.threshold(img_gray,70, 255, cv2.THRESH_BINARY)
		#processimage(image_RGB)
	
		#clear the stream in preparation for the next frame
		rawCapture.truncate(0)

except KeyboardInterrupt:
	print "Goodbye"
	stop(0)
	exit()

