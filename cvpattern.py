from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from motorControl import *

np.set_printoptions(threshold=np.nan) 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (250, 250)
camera.framerate = 1
rawCapture = PiRGBArray(camera, size=(250, 250))
 
# allow the camera to warmup
time.sleep(0.1)
count=0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image_RGB = frame.array
	print "image RGB"
	img_gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)
	print "Image GREY"
	(thresh, im_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cv2.imwrite('rgb_image'+str(count)+'.jpg', image_RGB)
	count +=1

	

	# clear the stream in preparation for the next frame
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
 
	

