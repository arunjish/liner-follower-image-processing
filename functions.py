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
	
def initial_skip():

	if initial_skip >0:
			initial_skip-=1
			print "initial skip"
			rawCapture.truncate(0)
			continue
		#skip_frame_count=0

def skip_frame():

	if skip_frame_count>0:
			skip_frame_count-=1
			#print "skipp frame"
			rawCapture.truncate(0)
			continue	
def initialise():
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

			

