## My Writeup

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./camera_cal/calibration2.jpg "Distorted"
[image2]: ./camera_cal/tmp/undist_calibration2.jpg "Undistorted"
[image3]: ./test_images/test3.jpg "Road Image"
[image4]: ./output_images/undistorted_test3.jpg "Undistorted Road Image"
[image5]: ./output_images/binary_test3.jpg "Binary Road Image"
[image6]: ./output_images/masked_binary_test3.jpg "Masked Binary Road Image"
[image7]: ./output_images/binary_lines_test3.jpg "Binary Lines (birds eye view)"
[image8]: ./output_images/lines_test3.jpg "Road Image with Lines"
[image9]: ./output_images/final_test3.jpg "Road Image with Lines and Curvature"

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one

You're reading it!

###Camera Calibration

####1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in `project/launch_camera_calibration.py`.  (lines 67 through 94).

See `project/README.md` for information about the parameters and command line for this script.

First I start by listing all the files available for camera calibration that match to image files (*.jpg, *.png) (contained in `camera_cal/`).
For the selected files, I try to find a chessboard with size (9,6) in gray images.

I use cv2.findChessboardCorners() function : 

```python 
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
```

If a chessboard is found, I add 'image' and 'object' points to 2 lists. 

_Note_ : In some images, there is no chessboard with this exact shape (9,6). Those files are excluded. 

Then with the 'image' and 'object' points, we can compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.
I applied this distortion correction to the test image using the cv2.undistort() function and obtained this result: 

(see code between lines 105 and 112 in `project/launch_camera_calibration.py`)

The camera calibration and distortion coefficients are saved into a Pickle file. 

![alt text][image1]
![alt text][image2]

###Pipeline (single images)

####1. Provide an example of a distortion-corrected image

##### STEP 1
I apply the distortion correction to one of the test images like this one: 

![alt text][image3]
![alt text][image4]

Parameters for distortion correction are loaded from a pickle file that contains `ret, mtx, dist, rvecs, tvecs` computed by `cv2.calibrateCamera()` during the execution of `project/launch_camera_calibration.py`. 

####2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

##### STEP 2 & 3
I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines 81 through 118 in `project/utils.py`).

The threshold values are defined in `project/settings.py`.

Just after this combination of thresholds I use a ROI extraction to select only pixels in the center area of the field of vision. 

It corresponds to the STEP 2 and STEP 3 in my pipeline : `make_binary()` and `ROI_extraction()` in `project/utils.py`.

Here's an example of my output for this step : 

![alt text][image3]
![alt text][image5]
![alt text][image6]

####3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

##### STEP 4
The code for my perspective transform includes a function called `get_lines()` in `project/utils.py`, which appears in lines 154 through 173.

`source` and `destination` points for `cv2.getPerspectiveTransform()` are hand-coded. I start with 4 corner points (`src`) and I apply an offset to get the destination points (`dest`). `corners` and `offset` are defined in `project/settings.py`. 

```python
    src = np.float32([corners[0], corners[1], corners[2], corners[3]])
    dst = np.float32([corners[0] + offset, new_top_left + offset, new_top_right - offset, corners[3] - offset])

    M = cv2.getPerspectiveTransform(src, dst)
```

`get_lines()` returns the warped image, and src and dst points for unwarping step a the end of the pipeline. 

![alt text][image6]
![alt text][image7]

####4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

##### STEP 5

I fit the lane lines with a 2nd order polynomial in STEP 5. 
It' s done within `fit_draw_lines()` function in `project/utils.py` (lines 176 through 340). 

This function takes as arguments the undistorted image, the binary lines from birds eye view, and (dst, src) from the previous step. 

It fits 2 polynomials (for the right and left lines). 

`fit_draw_lines()` returns the coefficients for the two polynomials, and the unwarped image where space between lines is green. 


For example : 

![alt text][image8]
 

####5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

##### STEP 6

I did this in `compute_display_curvature() `(lines 445 through 472) in my code in `project/utils.py`.

It uses the fitted polynomials to compute the curvature. 

It prints the curvature and the position of the vehicule with respect to center.

![alt text][image9]


####6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

##### STEPS 1 to 6

`pipeline()` from `project/utils.py` (lines 9 through 79) applies the 6 steps to images (to an image file, or to an image already loaded into a numpy array). 

It combines all the steps. 

![alt text][image3]
![alt text][image9]

---

###Pipeline (video)

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

See `project/README.md` for instructions and command line to run `project/launch_video_pipeline.py`.

This script apply the 6 steps of the pipeline to a video stream. 

Here's a [link to my video result](./output_project_video.mp4)

---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?


I wrote a Jupyter notebook (`NOTEBOOK_SelectParameters.ipynb`) that helps to select the parameters for the pipeline (saved in `project/settings.py`). 

However, my pipeline is not robust. It works well on `project_video.mp4`, but it fails on `challenge_video.mp4` and `harder_challenge_video.mp4`. 

I'm still tuning the parameters .. but I think I have to use a more complex/robust technique to fit the lines. 
It will be easy with my source code, I just need to replace code for step 5. 

But I prefer to submit my project now. 



