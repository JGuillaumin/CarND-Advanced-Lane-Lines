import pickle
import os
import time
import argparse
import re

import cv2

# main function of the pipeline
from project.utils import pipeline

if __name__ == '__main__':
    start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="path to the folder that contains all images for calibration",
                        default='test_images/')
    parser.add_argument("--camera_calib_file", help="path to a .pkl file that contains calibration information",
                        default='camera_cal/camera_calibration.pkl')
    parser.add_argument("--output_dir", help="path to the folder that contains all images for calibration",
                        default='output_images')
    parser.add_argument("--save_inter", help="save intermediate images (optional)", action='store_true')

    args = parser.parse_args()

    # ###################################### ARGUMENTS ######################################
    input_dir = args.input_dir
    output_dir = args.output_dir
    save_inter = args.save_inter
    camera_calibration_file = args.camera_calib_file

    print("=================================")
    print("input_dir : {}".format(input_dir))
    print("save_inter : {}".format(save_inter))
    print("output_dir : {}".format(output_dir))
    print("camera file : {}".format(camera_calibration_file))
    print("=================================")
    ###########################################################################################

    # regex pattern to image file
    image_regex = re.compile(r'.*\.(jpg|png|gif)$')

    # list files into `input_dir` that match to the correct regex form
    # using regex (instead of glog.glob) can handle multiple file formats.
    input_files = [filename for filename in os.listdir(os.path.abspath(input_dir))
                  if image_regex.match(filename) is not None]

    # Add 'input_dir'
    input_files = [os.path.join(input_dir, file) for file in input_files]

    print("Files are : ")
    [print("\t{}".format(file)) for file in input_files]

    # load calibration coeff
    with open(camera_calibration_file, mode='rb') as f:
        camera_calib = pickle.load(f)
    mtx = camera_calib["mtx"]
    dist = camera_calib["dist"]

    for file in input_files:
        # apply the pipeline
        # `filepath` is set to 'True'
        combined_image = pipeline(file, output_dir, save_inter, mtx=mtx,dist=dist, filepath=True)

        # save combined image
        image_name = os.path.split(file)[-1]
        cv2.imwrite(os.path.join(output_dir, 'final_' + image_name), combined_image)

    print("\nScript took {} seconds\n\n".format(time.time() - start))
