## Advanced Lane Finding


The goal of this project was to write a software pipeline to identify the lane boundaries in a video.


The steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.


## Project structure

- `camera_cal/` : images for camera calibration provided by Udacity
- `tes_images/` : images (from Udacity) for testing the pipeline and select hyper-parameters
- `examples/` : screenshots from Udacity
- `output_images/` : folder where intermediate outputs will be stored (when executing `project/launch_image_pipeline.py`)
- `project/` : my work, see `project/README.md` for more information
- `challenge_video.mp4` and `harder_video_challenge.mp4` : videos for applying the pipeline
- `NOTEBOOK_SelectParameters.ipynb` : Jupyter notebook that helps to select the right parameters
- `NOTEBOOK_AdvancedLaneLines.ipynb` : it's my first draft for this project, it might contain some debug lines.


## Launch the pipeline on images or videos 

(see `project/README.md` for more information)

**PYTHONPATH** :
When you are at the root of the project, add this path to `PYTHONPATH` !

```bash
export PYTHONPATH=$PYTHONPATH:$PWD
```


There are two three main scripts in `project`:


#### Compute camera calibration matrix

```python
python project/launch_camera_calibration.py \
                --input_dir camera_cal
                \--nx 9 --ny 6 \
                --save_images
                \--output_dir tmp
```


#### Apply pipeline to images within a folder

```python
python project/launch_image_pipeline.py \
                --input_dir test_images/ \
                --camera_calib_file camera_cal/camera_calibration.pkl \
                --output_dir output_images \
                --save_inter
```


#### Apply pipeline to a video

```python
python project/launch_video_pipeline.py \
                --input_video project_video.mp4 \
                --output_video output_project_video.mp4 \
                --camera_calib_file camera_cal/camera_calibration.pkl
```



#### Notebook `NOTEBOOK_SelectParameters.ipynb`

I wrote a notebook that takes all steps from the pipeline separately.
It's useful for parameter selection.

In addition to the code comments, it explains all steps.