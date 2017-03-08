import time
import re
import os
import pickle
import numpy as np
import cv2
import argparse


if __name__ == '__main__':
    start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="path to the folder that contains all images for calibration",
                        default='camera_cal/')
    parser.add_argument("--nx", help="chessboard configuration w.r.t. X", type=int, default=9)
    parser.add_argument("--ny", help="chessboard configuration w.r.t. X", type=int, default=6)
    parser.add_argument("--save_images", help="save intermediate images (optional)", action='store_true')
    parser.add_argument("--output_dir", help="path to the folder that contains all images for calibration",
                        default='tmp')
    args = parser.parse_args()

    # ############################# ARGUMENTS ##############################
    # folder with images for calibration
    input_dir = args.input_dir
    output_dir = args.output_dir
    save_undistorted_images = args.save_images

    # chessboard coniguration
    nx = args.nx
    ny = args.ny

    output_dir = os.path.join(input_dir, output_dir)
    if not os.path.isdir(output_dir) and save_undistorted_images:
        os.mkdir(output_dir)

    print("=================================")
    print("input_dir : {}".format(input_dir))
    print("save_images : {}".format(save_undistorted_images))
    print("output_dir : {}".format(output_dir))
    print("nx : {}".format(nx))
    print("ny : {}".format(ny))
    print("=================================")
    # #####################################################################

    # regex pattern to image file
    image_regex = re.compile(r'.*\.(jpg|png|gif)$')

    # list files into `input_dir` that match to the correct regex form
    # using regex (instead of glog.glob) can handle multiple file formats.
    list_files = [filename for filename in os.listdir(os.path.abspath(input_dir))
                  if image_regex.match(filename) is not None]

    # Add 'input_dir'
    list_files = [os.path.join(input_dir, file) for file in list_files]

    print("Files are : ")
    [print("\t{}".format(file)) for file in list_files]

    objp = np.zeros((ny * nx, 3), np.float32)
    objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)
    # (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0) : all possibles corners

    img_points = []
    obj_points = []

    for file in list_files:
        # load image
        img = cv2.imread(file)
        img_shape = img.shape[:2]
        # convert to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        if ret :
            img_points.append(corners)
            obj_points.append(objp)

            if save_undistorted_images:
                # Draw the corners and save image
                cv2.drawChessboardCorners(img, (nx, ny), corners, ret)

                # save image
                image_name = os.path.split(file)[-1]
                cv2.imwrite(os.path.join(output_dir, 'corners_' + image_name), img)

        else:
            print("Corners not found for {}".format(file))

    # compute calibration matrix and distortion coefficients
    print("Image shape is : {}".format(img_shape))
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, img_shape, None, None)

    # Save calibration coefficients into input_dir as pickled dict.
    calibration_dict = dict()
    calibration_dict["img_shape"] = img_shape
    calibration_dict["mtx"] = mtx
    calibration_dict["dist"] = dist
    calibration_dict["rvecs"] = rvecs
    calibration_dict["tvecs"] = tvecs

    pickle.dump(calibration_dict, open(os.path.join(input_dir, "camera_calibration.pkl"), "wb"))

    if save_undistorted_images:
        for file in list_files:
            # load image
            img = cv2.imread(file)
            undist = cv2.undistort(img, mtx, dist, None, mtx)
            # save image
            image_name = os.path.split(file)[-1]
            cv2.imwrite(os.path.join(output_dir, 'undist_' + image_name), undist)

    print("\nScript took {} seconds\n\n".format(time.time() - start))
