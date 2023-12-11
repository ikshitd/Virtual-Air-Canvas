import cv2 
import numpy as np 

def empty(a) : 
	pass 

def detectcolors() : 
	capture = cv2.VideoCapture(0) 
	capture.set(3 ,640)
	capture.set(4 , 200)
	capture.set(10 , 200) 

	cv2.namedWindow("Trackbar") 
	cv2.resizeWindow("Trackbar" , 640 , 300) 
	cv2.createTrackbar("hue min" , "Trackbar" , 0 , 179 , empty) 
	cv2.createTrackbar("hue max" , "Trackbar" , 179 , 179 , empty) 
	cv2.createTrackbar("sat min" , "Trackbar" , 0 , 255 , empty) 
	cv2.createTrackbar("sat max" , "Trackbar" , 255 , 255 , empty) 
	cv2.createTrackbar("val min" , "Trackbar" , 0 , 255 , empty) 
	cv2.createTrackbar("val max" , "Trackbar" , 255 , 255 , empty) 

	while(True) : 
		success , frame = capture.read() 
		# cv2.imshow("vid" , frame) 

		img = frame.copy()
		hsv_img = cv2.cvtColor(img , cv2.COLOR_BGR2HSV) 
		h_min = cv2.getTrackbarPos("hue min" , "Trackbar") 
		h_max = cv2.getTrackbarPos("hue max" , "Trackbar")
		s_min = cv2.getTrackbarPos("sat min" , "Trackbar")
		s_max = cv2.getTrackbarPos("sat max" , "Trackbar")
		v_min = cv2.getTrackbarPos("val min" , "Trackbar")
		v_max = cv2.getTrackbarPos("val max" , "Trackbar")

		lower = np.array([h_min , s_min , v_min])
		upper = np.array([h_max , s_max , v_max]) 
		mask = cv2.inRange(hsv_img , lower , upper) 
		result = cv2.bitwise_and(img , img , mask = mask) 

		mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) 
		final = np.hstack([img , mask , result]) 

		cv2.imshow("final" , final) 
		if(cv2.waitKey(1) & 0xFF == ord('q')) : 
			break 


my_colors = [[59 , 120 , 79 , 255 , 116 , 255] ,
    [43 , 86 , 43 , 255 , 170 , 215],
	[126 , 179 , 60 , 255 , 191 , 255] 
]
my_color_values = [[255 , 210 , 160],
	[190 , 240 , 170],
	[0 , 0 , 0]
] 


my_points = [] 
brush_thickness = 4
eraser_thickness = 40

def draw_on_canvas(my_points , my_color_values , xp , yp ) : 
	for points in my_points : 
		if(xp == 0 and yp == 0) : 
			xp ,yp = points[0] , points[1] 

		draw_color = my_color_values[points[2]]
		thickness = brush_thickness
		if(draw_color == [0 , 0 , 0]) : 
			thickness = eraser_thickness 

		print(draw_color , thickness) 
		# cv2.circle(res_img , (points[0]  , points[1]) , 10 , my_color_values[points[2]] , cv2.FILLED) 
		cv2.line(canvas_img , (xp , yp) , (points[0] , points[1]) , draw_color , thickness)
		xp , yp = points[0] , points[1] 



def getcontours(img) : 
	contours , hierarchy = cv2.findContours(img , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE) 

	x , y , w , h = 0 , 0 , 0 , 0
	for cnt in contours : 
		area = cv2.contourArea(cnt) 
		if (area > 500) : 
			# cv2.drawContours(res_img , cnt , -1 , (255 , 0 , 0) , 3) 
			perimeter = cv2.arcLength(cnt , True) 
			approx = cv2.approxPolyDP(cnt , 2 * perimeter , True) 
			x , y , w , h = cv2.boundingRect(approx) 


	return x , y

def find_color(img , my_colors , my_color_values) : 
		hsv_img = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
		cnt  =	0
		newPoints = []
		for color in my_colors :
			lower = np.array([color[0] , color[2] ,color[4]]) 
			upper = np.array([color[1] , color[3] , color[5]]) 
			mask = cv2.inRange(hsv_img , lower , upper) 
			x , y  = getcontours(mask) 
			# cv2.circle(canvas_img , (x , y) , 10 , my_color_values[cnt] , cv2.FILLED)
			if(x != 0 and y != 0) : 
				newPoints.append([x , y , cnt])
			cnt += 1 
		return newPoints

#begin
# detectcolors()

framewidth = 720 
frameheight = 480 

#reading the video
capture = cv2.VideoCapture(0) 
capture.set(3 , framewidth) 
capture.set(4 , frameheight)  
capture.set(10 , 150)
capture.set(cv2.CAP_PROP_FPS, 60)
canvas_img = np.zeros((frameheight , framewidth , 3) , np.uint8) 

while(True) : 
	success , frame = capture.read()
	res_img = frame.copy() 
	newPoints = find_color(frame , my_colors , my_color_values)  

	if(len(newPoints) != 0) : 
		for newpoints in newPoints : 
			my_points.append(newpoints) 

	xp , yp = 0 , 0
	if(len(my_points) != 0) : 
		draw_on_canvas(my_points , my_color_values , xp , yp)

	res_img = cv2.resize(res_img , (720 , 480))  

	gray_img = cv2.cvtColor(canvas_img , cv2.COLOR_BGR2GRAY)
	_, inverse_img = cv2.threshold(gray_img , 50 , 255 , cv2.THRESH_BINARY_INV) 
	inverse_img = cv2.cvtColor(inverse_img , cv2.COLOR_GRAY2BGR)
	res_img = cv2.bitwise_and(res_img , inverse_img) 


	res_img = cv2.bitwise_or(res_img , canvas_img) 

	# final = cv2.addWeighted(res_img , 0.5 , canvas_img , 0.5 , 0) 
	final = np.hstack((res_img , canvas_img))
	# cv2.imshow("video" , res_img)  
	cv2.imshow("Air Canvas" , res_img) 
	# cv2.imshow("final" , final) 

	if(cv2.waitKey(1) & 0xFF == ord('q')) : 
	    break 

cv2.destroyAllWindows() 
