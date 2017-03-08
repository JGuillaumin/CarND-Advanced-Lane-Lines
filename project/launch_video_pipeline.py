import pickle
import os
import time
import argparse
import re

import cv2
from moviepy.editor import VideoFileClip

from project.settings import settings
from project.utils import pipeline

if __name__ == '__main__':
    start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_video", help="path to a video where apply the pipeline",
                        default='project_video.mp4')
    parser.add_argument("--camera_calib_file", help="path to a .pkl file that contains calibration information",
                        default='camera_cal/camera_calibration.pkl')
    parser.add_argument("--output_video", help="complete path (path + name) for the output",
                        default='output_project_video.mp4')
    args = parser.parse_args()

    # ###################################### ARGUMENTS ######################################
    input_video = args.input_video
    output_video = args.output_video
    camera_calibration_file = args.camera_calib_file

    print("=================================")
    print("input_video : {}".format(input_video))
    print("output_dir : {}".format(output_video))
    print("camera file : {}".format(camera_calibration_file))
    print("=================================")
    ###########################################################################################

    # load calibration coeff
    with open(camera_calibration_file, mode='rb') as f:
        camera_calib = pickle.load(f)
    mtx = camera_calib["mtx"]
    dist = camera_calib["dist"]

    # the function create a custom pipeline with camera matrix 'mtx' and distortion coefficients 'dist'.
    # file is set to false, the first argument 'file' represents an image as array.
    def create_image_pipeline(mtx, dist):
        def image_pipeline(img):
            return pipeline(file=img, output_dir=None, save_inter=False, dist=dist, mtx=mtx, filepath=False)
        # returns a function the pre-configurated arguments (python closure)
        return image_pipeline

    image_pipeline = create_image_pipeline(mtx, dist)

    # load input_video
    clip1 = VideoFileClip(input_video)

    # apply the pipeline to the video
    output_clip = clip1.fl_image(image_pipeline)

    # save the new video
    output_clip.write_videofile(output_video, audio=False)

    print("\nScript took {} seconds\n\n".format(time.time() - start))