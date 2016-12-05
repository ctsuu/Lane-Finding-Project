import numpy as np
import cv2
from lane_finding_processing import *

# initial apexs Left and Right settings 
apex_L_x = 600
apex_L_y = 450
apex_R_x = 720
apex_R_y = 450
apex_L = []
apex_R = []
delta = 250

 
i = 0
cap = cv2.VideoCapture("challenge.mp4")

while(cv2.waitKey(10) != ord('q')):
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Define a kernel size and apply Gaussian smoothing
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    # Define our parameters for Canny and apply
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    # This time we are defining a four sided polygon to mask
    imshape = image.shape
    vertices = np.array([[(20,imshape[0]-80),(apex_L_x,int(0.6*imshape[0])), (apex_R_x, int(0.6*imshape[0])), (imshape[1]-20,imshape[0]-80)]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)
# Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 1 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 10     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40 #minimum number of pixels making up a line
    max_line_gap = 12    # maximum gap in pixels between connectable line segments
    # line_image = np.copy(image)*0 # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    slope = [-0.7,0.7]

    for line in lines:
        for x1,y1,x2,y2 in line:
            slope.append((y2-y1)/(x2-x1))
    # Create a "color" binary image to combine with line image
    # color_edges = np.dstack((edges, edges, edges)) 
    bottom_L_x, bottom_R_x = int(apex_L_x+delta/min(slope)-90),int(apex_R_x+delta/max(slope)+40)
    cv2.line(image,(apex_L_x, apex_L_y),(bottom_L_x,apex_L_y+delta-2),(0,0,255),10)
    cv2.line(image,(apex_R_x, apex_R_y+5),(bottom_R_x,apex_R_y+delta),(0,0,255),10)
    #lines_edges = cv2.addWeighted(color_edges, 0.8, image, 1, 0)
    cv2.imshow('image', image)
    
    
cap.release()
cv2.destroyAllWindows()
