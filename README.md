# Lane-Finding-Project
Udacity Self-Driving Car Engineer Class Project, due on Dec 6th, 2016

# Reflection

Image processing pipeline decription: 
* 1. grayscale
* 2. Canny edge
* 3. Masking
* 4. Hough Transform
* 5. Initialize left and right slope values
* 6. Append updated lane section slopes into slope list
* 7. Drawing Left and Right lane makers

1. OpenCV Grayscale

2. Canny Edge Settings:

3. Masking edges, regain setting
In this project, the masking point is fixed according to the input image size. 
For future developmetn, maybe can generate the masking corners by the trained neuron network. 

4. Hough Transform involves lot of calculation. 
Try to keep the masked area as small as possible. 

5. Hough transform sometimes can't return lines. Therefore, assign averaged slope value into slope list can provent the error by print or draw from empty list. 

6. Take max slope for the left line maker, and min slope for the right maker. 

7. Apex point is near the middle of the image, for image shape 960 x 540, set delta = 1000, will move the left and right bottom point out of the image. 

Challenge Video:
The provided challenge.mp4 is a challenge. 
The existing code is not working for this video yet. 

Future work:
* Dynamic masking
* Add CNN detection for dynamic masking 
