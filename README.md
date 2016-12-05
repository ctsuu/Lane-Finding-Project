# Lane-Finding-Project
Udacity Self-Driving Car Engineer Class Project, due on Dec 6th, 2016
![test_image_index](https://cloud.githubusercontent.com/assets/22917810/20874031/562b0b74-ba6b-11e6-801e-1bacaa9398e6.png)

# Reflection

Image processing pipeline decription for: 
* Grayscale
* Canny edge
* Masking
* Hough Transform
* Initialize left and right slope values
* Append updated lane section slopes into slope list
* Drawing Left and Right lane makers

Additional decription for loading individual images, mp4 videos, make movies and real time play. 

# Current Image Process Pipeline
First, I create a images.csv file to list all test images in the test_images folder. Then I import the file into a list, for display all test images and results in one shot. 
```
import os
from numpy import arange 

os.listdir("test_images/")

img_list = []

#read images.csv
with open("test_images/images.csv") as images:
    for line in images:
        img_list.append(line.split()[0])

first_col = arange(1,2*len(img_list),2)
second_col = first_col+1
```
My approach is to find the left and right apex points first, then work down to the bottem of the image. The initial apex point is close to the center of the image. Apex left and right are close, but not touch each other, the openning is the vanish point, and for the curve to fit in as well.
```
# initial apexs Left and Right settings 
apex_L_x = 450
apex_L_y = 325
apex_R_x = 510
apex_R_y = 324
```

* OpenCV Grayscale
The OpenCV command from BGR color to gray scale is:
```
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
* Canny Edge Settings:
```
low_threshold = 50
high_threshold = 150
canny = cv2.Canny(grayscale, low_threshold, high_threshold)
```
* Masking edges, region of interest setting
In this project, the masking point is fixed according to the input image size. 
```
imshape = image.shape
vertices = np.array([[(20,imshape[0]),(490,int(0.6*imshape[0])), (500, int(0.6*imshape[0])), (imshape[1]-20,imshape[0])]], dtype=np.int32)
# cv2.fillPoly(mask, vertices, ignore_mask_color)
masked_edges = region_of_interest(edges, vertices)
```
* For future developmetn, maybe can generate the masking corners by the trained neuron network. 
Hough Transform involves lot of calculation, try to keep the masked area as small as possible. 

```
rho = 1           # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 40 #15    # minimum number of points on a line (intersections in Hough grid cell)
min_line_len = 100 #20  # minimum number of pixels making up a line
max_line_gap = 160 #20  # maximum gap in pixels between connectable line segments

hough_lines_img = hough_lines(masked_edges, rho, theta, threshold, min_line_len, max_line_gap)
```
* Hough transform sometimes can't return lines. Therefore, assign averaged slope value into slope list can provent the error while print or draw from empty list. 
```
lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    #print(lines)
    # Iterate over the output "lines" and draw lines on a blank image
    slope = [-0.724,0.6]

    for line in lines:
        for x1,y1,x2,y2 in line:
            slope.append((y2-y1)/(x2-x1))
```

* Take max slope for the left line maker, and min slope for the right maker. 
```
delta = 1000
bottom_L_x, bottom_R_x = int(apex_L_x+delta/min(slope)),int(apex_R_x+delta/max(slope))
```
* Apex point is near the middle of the image, for image shape 960 x 540, set delta = 1000, will move the left and right bottom point out of the image. 
```
cv2.line(image,(apex_L_x, apex_L_y),(bottom_L_x,apex_L_y+delta-2),(255,0,0),10)
cv2.line(image,(apex_R_x, apex_R_y+5),(bottom_R_x,apex_R_y+delta),(255,0,0),10)
```
* Use moviepy to make output video
It is nice to save the results in another video, but it wouldn't show the pipeline performance, the processing speed. 
```
white_output = 'white2.mp4' # output video file name
clip1 = VideoFileClip("solidWhiteRight.mp4") # open target video
white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
%time white_clip.write_videofile(white_output, audio=False)
```
* Use OpenCV to play video and process in real time
I created lane_finding_main.py to play video and review the annotated lane lines in real time.
For some reason, the openCV 3.0 could not play mp4 video, I have to switch python 3.5 back to 2.7 by modify the .bashrc file
comment the export line.
```
# added by Anaconda3 4.2.0 installer
# export PATH="/home/tfbox/anaconda3/bin:$PATH"
```
The main programe load the video, and call processing function to proceed. 
Display the output video, without saving the file.

# Potential Shortcomings of the current pipeline:
The provided challenge.mp4 is a challenge. 
The existing code is not working for this video yet. 

# Future work/Possible improvements:
* Dynamic masking
* Add CNN detection for dynamic masking 
