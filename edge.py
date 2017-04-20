from datetime import datetime 
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
import numpy as np
from motorControl import *
import sys
from functions import *
initialise()

try:
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		t1 = datetime.now()
		initial_skip()
		skip_frame()
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
		"""
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

			
		if turn==False and turnLoop==False and turnOver==False:
			directBot(frame_res)
		"""
		t2 = datetime.now()
                delta=t2-t1
		
		skip_frame_count=int(delta.microseconds/100000)
		
	
		rawCapture.truncate(0)

except KeyboardInterrupt:
	print "Goodbye"
	exit()

