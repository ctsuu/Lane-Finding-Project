# Lane-Finding-Project
Udacity Self-Driving Car Engineer Class Project, due on Dec 6th, 2016

# Reflection

Image processing pipeline decription: 
* Grayscale
* Canny edge
* Masking
* Hough Transform
* Initialize left and right slope values
* Append updated lane section slopes into slope list
* Drawing Left and Right lane makers

1. OpenCV Grayscale
The OpenCV command from BGR color to gray scale is:
```
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
2. Canny Edge Settings:
```
low_threshold = 50
high_threshold = 150
canny = cv2.Canny(grayscale, low_threshold, high_threshold)
```
3. Masking edges, regain setting
In this project, the masking point is fixed according to the input image size. 
For future developmetn, maybe can generate the masking corners by the trained neuron network. 

4. Hough Transform involves lot of calculation, try to keep the masked area as small as possible. 
```
rho = 1           # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 40 #15    # minimum number of points on a line (intersections in Hough grid cell)
min_line_len = 100 #20  # minimum number of pixels making up a line
max_line_gap = 160 #20  # maximum gap in pixels between connectable line segments

hough_lines_img = hough_lines(masked_edges, rho, theta, threshold, min_line_len, max_line_gap)
```
5. Hough transform sometimes can't return lines. Therefore, assign averaged slope value into slope list can provent the error while print or draw from empty list. 

6. Take max slope for the left line maker, and min slope for the right maker. 

7. Apex point is near the middle of the image, for image shape 960 x 540, set delta = 1000, will move the left and right bottom point out of the image. 

Challenge Video:
The provided challenge.mp4 is a challenge. 
The existing code is not working for this video yet. 

Future work:
* Dynamic masking
* Add CNN detection for dynamic masking 
