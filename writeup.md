# Project: Search and Sample Return

<img src="./misc/rover_autonomous.png" width="500">

This writeup the process of, based on the structure provided [(refer to the project README.md)](README.md), modifying perception and decision procedures to make the rover navigate and pick up rocks autonomously. The following steps have been done.

* ## [Try the Simulator and Jupyter Notebook](#try-the-simulator-and-jupyter-notebook)
  - Run the simulator  
  - Test out the functions in the Jupyter Notebook
* ## [Autonomous Navigation and Mapping](#autonomous-navigation-and-mapping)
----

## Try the Simulator and Jupyter Notebook

### Run the simulator

- Download the simulator and take data in "Training Mode"

### Test out the functions in the Jupyter Notebook  
Inside the Jupyter Notebook, there are functions used for perception part of codes of the autonomous rover. They can be used for testing how the functions work.

- **Perspective view to world coordinates and rove steering angle**  
In order the generate rover's steering angle from the images from rover's camera, we use `perspective_transform()` to firstly change the view to top view image, and then apply `color_thresh()` to identify the navigable terrain.  
  
  To obtain rover's steering angle, apply `rover_coords()` and `to_polar_coords()` respectively to get the angles of all navigable pixels and use the mean of them as steering angle.  
      <img src="./misc/perspective_angle.png" width="400">
  
  Use `pix_to_world()`, for transfrom pixels in rover coordinates to world coordinates for later mapping pixels to world map.  

- **To find the rocks**  
  To identify the target rocks, use the same technique in `color_thresh()`, but with different threshold parameters. That is `find_rocks`, of which the result as follows  
  <img src="./misc/find_rock.png" width="400">  

- **Generate the video**  
  Use the data gathered from simulator training mode and generate the video file required
  
## Autonomous Navigation and Mapping
I use the basic solution from [Project Walkthrough Video](https://www.youtube.com/watch?v=oJA6QHDPdQw), and do the following modifications

- **Fedelity improvement**  
After perspective transformation, the pixels at large distance are not accurate, which affect the fedelity as a result. By simple using only pixels at a certain distance, we can increase the fedelity.   

Use only the center area (black out other area). Compareed with calculating the distance, the following codes is not a fancy, but is easy and does the job well(~80% fedelity).
'''
    color_select[0:60,:] = 0
    color_select[:,0:110] = 0
    color_select[:,190:] = 0
'''

- **`stuck` mode**

- **`rock_pickup` mode**

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

![alt text][image1]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
And another! 

![alt text][image2]
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  



![alt text][image3]


