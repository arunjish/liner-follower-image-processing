from datetime import datetime 
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
import numpy as np

from step import *
import sys

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

mid1corrected=False
bottom1corrected=False
mid2corrected=False
def checkFrame(edgex):
	h,w=edgex.shape
	h=h-100
      	m_y1=0
       	m_y2=0
        mid_edge_count=0
	mid_centre=0	
	top_l_edge_count=0
	top_r_edge_count=0
	top_line_edge_count=0
	top_line_centre=0
	top_r_centre=0
	top_l_centre=0
	bottom_line_edge_count=0
	bottom_line_centre=0
        for i in range(0,h-10):
                if edgex[h/2][i]==255:
                        mid_edge_count+=1
                        if mid_edge_count==1:
                               mid_centre=i
                        elif mid_edge_count==2:
                                mid_centre=int((mid_centre+i)/2)
			



		if edgex[i+10][40]==255:
                        top_l_edge_count+=1
			if top_l_edge_count==1:
                               top_l_centre=i
                        elif top_l_edge_count==2:
                		top_l_centre=int((top_l_centre+i)/2)
			

		if edgex[i+10][w-40]==255:
                        top_r_edge_count+=1
			if top_r_edge_count==1:
                               top_r_centre=i
                        elif top_r_edge_count==2:
                                top_r_centre=int((top_r_centre+i)/2)
			

		if edgex[30][i]==255:
			top_line_edge_count+=1
			if top_line_edge_count==1:
                               top_line_centre=i
                        elif top_line_edge_count==2:
                                top_line_centre=int((top_line_centre+i)/2)
                        


		if edgex[h-30][i]==255:
                        bottom_line_edge_count+=1
			if bottom_line_edge_count==1:
                               bottom_line_centre=i
                        elif bottom_line_edge_count==2:
                                bottom_line_centre=int((bottom_line_centre+i)/2)
				
			
	
	return ((top_l_edge_count,top_l_centre),(mid_edge_count,mid_centre),(top_r_edge_count,top_r_centre),(top_line_edge_count,top_line_centre),(bottom_line_edge_count,bottom_line_centre))


def directBot(frame_res):
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

	
	if top_l_edge_count==2 and top_r_edge_count==2 and top_line_edge_count==2 :
		print "plus junction"
		#forward(fdelay)
               
               # diffRight(tdelay)
	elif top_l_edge_count==2 and top_line_edge_count==2 and top_r_edge_count==0:
                print "left T junction"
		#forward(fdelay)
                #diffLeft(tdelay)
               

                
	elif top_r_edge_count==2 and top_line_edge_count==2 and top_l_edge_count==0 :
                print "right T junction"
		#forward(fdelay)
                #stop(2)

	elif top_l_edge_count==2 and top_line_edge_count==2 and top_r_edge_count==2:
		print "T junction"
		#forward(fdelay)
                #diffLeft(tdelay)
               
	elif top_l_edge_count==2 and top_r_edge_count==0  :
		print "\t\t\tleft turn Ahead"
		turn=True
		turnDir="l"
		mid1corrected=False
		bottom1corrected=False
		mid2corrected=False

		#exit(True)
		#turn_bottom_edge_count=0
		#forward(0)
	elif top_l_edge_count ==0 and  top_r_edge_count==2 :
		print "\t\t\tright turn detected"
		turn=True
                turnDir="r"
		mid1corrected=False
		bottom1corrected=False
		mid2corrected=False

		
	elif 0<mid_centre<200:
		left(5,0.001)		
	elif 200<=mid_centre<=210:
		forward(40,0.003)
	elif 210<mid_centre<=400:
		right(5,0.001)
	
		


def printFrame(im_bw):
	h,w=im_bw.shape
	h=h-100
	for x in range(0,h):
		
		row_count_black=0
		row_count_white=0
		sys.stdout.write(str(x)+ " : ")
        	for y in range(0,w):
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
			#print "skipp frame"
			rawCapture.truncate(0)
			continue	
		
		img_RGB = frame.array
		img_RGB=cv2.resize(img_RGB,(400,400))
		
		edge=cv2.Canny(img_RGB,100,200)
		
		#printFrame(edge)
		frame_res= checkFrame(edge)
		print "\n\n\t\t Top-L | Mid | Top-R | Top-Line | Bottom Line  "
		print "\t\t"+ str(frame_res)+"\n\n"
		
		top_l,mid,top_r,top_line,bottom_line=frame_res
	        mid_edge_count,mid_centre=mid
	        top_l_edge_count,top_l_centre=top_l
	        top_r_edge_count,top_r_centre=top_r
		top_line_edge_count,top_line_centre=top_line
		bottom_line_edge_count,bottom_line_centre=bottom_line

		if 200<=mid_centre<=210:
        	        mid_ok=True
	        else:
                	mid_ok=False

		if 200<=bottom_line_centre<=210:
                        bottom_ok=True
                else:
                        bottom_ok=False

		

		if turn==True :
			
			if  bottom_ok:
                                print "\t\t\t\t\tPre Turn Correction compleated"
                                turn=False
				turnLoop=True
                                t2 = datetime.now()
                                delta=t2-t1
					
				if turnDir=="l":
                                	dist=int((270-top_l_centre)/2)   #bottom line centre - topline centre
                                	forward(dist+40,0.005)

                                
	                        if turnDir=="r":
                                	dist=int((270-top_r_centre)/2)
                                	forward(dist,0.005)

                              


                                skip_frame_count=int(delta.microseconds/100000)+2
			

                                rawCapture.truncate(0)
                                continue
                        elif not bottom_ok :
                                print "\t\t\t\tPre turn bottom  correcting...."

                                if 0<bottom_line_centre<200:
                                        diffLeft(5,0.001)

                                elif 200<bottom_line_centre<=400:
                                        diffRight(5,0.001)

		if turnLoop==True:
			#if  bottom_line_edge_count !=2:
			print turnDir
			if turnDir=="l":
				 diffLeft(100,0.001)   #bottom line centre - topline centre
                           
			if turnDir=="r":
                                diffRight(100,0.001)
			if bottom_ok:
				turnLoop=False
				turnOver=True
				print "Turn over"
			t2 = datetime.now()
	                delta=t2-t1

        	        skip_frame_count=int(delta.microseconds/100000)

			rawCapture.truncate(0)
                        continue
		
		if 200<=bottom_line_centre<=210:
                        bottom_ok=True
                else:
                        bottom_ok=False


		if turnOver==True:
			
			if  bottom_ok:
                                print "\t\t\t\t\tPost Turn Correction compleated"
                                turnOver=False
                                t2 = datetime.now()
                                delta=t2-t1

                                skip_frame_count=int(delta.microseconds/100000)


                                rawCapture.truncate(0)
                                continue
                        elif not bottom_ok :
                                print "\t\t\t\tPre turn bottom  correcting...."

                                if 0<bottom_line_centre<200:
                                        left(10,0.001)

                                elif 200<bottom_line_centre<=400:
                                        right(10,0.001)

			"""			
			if  mid_ok and  mid2corrected:
                                print "\t\t\t\t\tPost Turn Correction compleated"
                                turnOver=False
				t2 = datetime.now()
		                delta=t2-t1

		                skip_frame_count=int(delta.microseconds/100000)

				rawCapture.truncate(0)
	                        continue

                        	
                               
			elif not mid_ok and not mid1corrected:
				print "\t\t\t\tPost turn mid  correcting...."

				if 0<mid_centre<200:
                                        left(5,0.001)

                                elif 210<mid_centre<=400:
                                        right(5,0.001)
			elif  mid_ok and not mid1corrected:
				mid1corrected=True
			elif not bottom_ok and not bottom1corrected:
                                print "\t\t\t\tPost turn bottom  correcting...."

                                if 0<bottom_line_centre<200:
                                        diffLeft(5,0.001)

                                elif 200<bottom_line_centre<=400:
                                        diffRight(5,0.001)
			elif bottom_ok and not bottom1corrected:
				bottom1corrected=True

			elif not mid_ok and bottom1corrected:
				print "\t\t\t\tPost turn mid 2  correcting...."

                                if 0<mid_centre<200:
                                        diffLeft(5,0.001)

                                elif 210<mid_centre<=400:
                                        diffRight(5,0.001)
			elif mid_ok and bottom1corrected:
                                mid2corrected=True

		
			"""
		if turn==False and turnLoop==False and turnOver==False:
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
	exit()

