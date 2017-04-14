from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from motorControl import *
import sys
np.set_printoptions(threshold=np.nan) 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (250, 250)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(250, 250))
 
# allow the camera to warmup
time.sleep(0.1)
count=0
skipped_frame=False
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image_RGB = frame.array
	#print "image RGB"
	img_gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)
	#print "Image GREY"
	(thresh, im_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	


	count+=1

	# checking for incompleate frames by taking the count of 10 th row 
	w_count=0

	count_b_top=0
	count_b_bottom=0
	count_b_left=0
	count_b_right=0

	for i in range(0,250):
		if im_bw[10][i]== 255:
			w_count+= 1
		if im_bw[10][i]==0:
			count_b_top+=1
		if im_bw[240][i]==0:
			count_b_bottom+=1
		if im_bw[i][10]==0:
			count_b_left+=1
		if im_bw[i][240]==0:
			count_b_right+=1
	#print "count of w = " + str(w_count)
	
	if w_count < 150:
		skipped_frame= True
		print "\t\t\tskipped frame\n"
		 # clear the stream in preparation for the next frame
		#cv2.imwrite("skipped_Frame"+str(count)+".jpg",image_RGB)

	        rawCapture.truncate(0)

		continue

	print "\n\n-------------------------------------------------------------------------------------------------------------\n\n"
	print "\t\t\t top = "+ str(count_b_top)
        print "left = "+str(count_b_left)
        print "\t\t\t\t\t\tright =  "+ str(count_b_right)
        print "\t\t\tbottom = "+str(count_b_bottom)
	
	if count_b_top > 70 and count_b_bottom > 70 and count_b_left < 70 and count_b_right < 70:
		forward()
	elif count_b_bottom>70 and count_b_right>70 and skipped_frame:
		right()
	else :
		stop()
		break
	
	print "\n\n-------------------------------------------------------------------------------------------------------------\n\n"
	skipped_frame=False

	"""
		
	for x in range(0,250):
		for y in range(0,250):
			if im_bw[x][y] == 0 :			
				sys.stdout.write("#")
			else:
				sys.stdout.write(".")		
		sys.stdout.write("\n")
	"""
	#clear the stream in preparation for the next frame
        rawCapture.truncate(0)


	
'''	template = cv2.imread('left.jpg',0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8

	loc = np.where( res >= threshold)
	print loc[0]
	#if len(loc) == 0:
	#	print "."
	#else :
	#	print "left"
	for pt in zip(*loc[::-1]):
    		cv2.rectangle(image_RGB, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
		print "match"
	#cv2.imwrite("Frame"+str(count)+".jpg",image_RGB)
	
	count= count + 1  
'''	
 
	

