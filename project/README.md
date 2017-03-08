## Project "Advanced Lane Lines"

This folder contains my solution for project 4 of the Sefl-driving car Nano-degree by Udacity.


**Files are :**

- `launch_camera_calibration.py` : compute camera calibration matrix and distortion coefficients from chessboard images.
 Matrix and other coefficients are stored as a `pickle` file inside `input_dir`
- `settings.py` : parameters for the pipeline (like boundaries for threshold steps)
- `utils.py` : methods/functions for the pipeline.
- `launch_image_pipeline.py` : apply the pipeline to several images. It uses parameters defined in `settings.py`
- `lauch_video_pipeline.py` : apply the pipeline to a video. It uses parameters defined in `settings.py`


## Camera calibration

#### How to launch the camera calibration ?

(from project root)

```python
python project/launch_camera_calibration.py \
                --input_dir camera_cal
                \--nx 9 --ny 6 \
                --save_images
                \--output_dir tmp
```

**Parameters are :**

- `--input_dir` : path to the folder that contains images of chessboards
- `--nx` and `--ny` : number of squares w.r.t. X and Y axis
- `--save_images` (_optional_) : add this flag if you want to save undistorted images and images with corners.
- `--output_dir` : name for the folder where intermediate images will be store if `--save_images` flag is present. It will create a folder within `input_dir`.

**Outputs :**

This script will save calibration matrix and distortion coefficients in python `dict` as a pickle file.
The dictionary contains elements :
- "img_shape" : image shape as a tuple
- "mtx" : camera matrix
- "dist" : distotion coefficients
- "rvecs" : rotation vectors
- "tvecs" : translation vectors

#### How it works ?

The script lists the files that match to images inside `input_dir` (*.jpg, *.png, or *.gif).

It creates two empty lists : for object points and images points.

Then for each file, we convert the image to grayscale and we try to find corners with `cv2.findChessboardCorners()`.
This OpenCV function uses `--nx` and `--ny` parameters passed as arguments to the script.
It corresponds to the chessboard size. If an image does not match to a chessboard with size `(nx ,ny)`, this imaga is skipped.

If corners are found, we add image and object points to the lists.
If `--save_images` is activated, it saves image with corners.

Then with image and object points, we can compute the camera matrix and distortion coefficients.
Those variables are save in a python dictionary which is serialized as a pickle file.

Finally, if we activated the flag `--save_images`, the script will apply `cv2.undistort()` on calibration images.


## Pipeline : Identify lane boundaries

This is the main goal of this project : define lane boundaries frame by frame.

I wrote 2 scripts that apply the pipeline :
- `launch_video_pipeline.py` : to apply the pipeline to a video
- `launch_image_pipeline.py` : to apply the pipeline to images

The different steps of this pipeline require several parameters.
They are defined in `settings.py` as python dictionary, which is imported in the pipeline.

One major improvement might consist to use configuration file (*.ini or *.cfg) with `configparser` package.
Configuration files may be used to keep records from tests.


### How to select parameters ?

I wrote a Jupyter notebook, `NOTEBOOK_SelectParameters.ipynb`, that takes each step separately and applies transformations to test images.

I used this notebook to select the best parameters for my pipeline.

In addition to the code comments, this notebook provides a complete documentation about each step.

When parameters are correctly tuned in `settings.py`, you can pply the pipeline to several images or to videos.

_(scripts must be launched from project root)_

### Apply pipeline to images within a folder

**PYTHONPATH** :
When you are at the root of the project, add this path to `PYTHONPATH` !

```bash
export PYTHONPATH=$PYTHONPATH:$PWD
```

```python
python project/launch_image_pipeline.py \
                --input_dir test_images/ \
                --camera_calib_file camera_cal/camera_calibration.pkl \
                --output_dir output_images \
                --save_inter
```

- `--input_dir` : folder with images
- `--camera_calib_file` : path to the pickle fil that contains camera calibration.
- `--output_dir` : folder where final and intermediate images will be stored
- `--save_inter` : (_boolean_) add this flag if you want to save intermediate outputs (like thresholded images)



### Apply pipeline to a video

```python
python project/launch_video_pipeline.py \
                --input_video project_video.mp4 \
                --output_video output_project_video.mp4 \
                --camera_calib_file camera_cal/camera_calibration.pkl
```

- `--input_video` : path to a video
- `--output_video` : path to the output video
- `--camera_calib_file` : path to the pickle fil that contains camera calibration.

