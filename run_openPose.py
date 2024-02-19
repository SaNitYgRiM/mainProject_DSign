import sys
import cv2
import os
import argparse
import time
from sys import platform

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../bin/python/openpose/Release')
        os.environ['PATH'] += ';' + dir_path + '/../x64/Release;' +  dir_path + '/../bin;'
        import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="DATA_PATH/All_Frames/", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--output_dir", default="DATA_PATH/All_Keys/", help="Directory to save keypoints JSON files.")
    parser.add_argument("--no_display", action="store_true", help="Enable to disable the visual display.")
    args = parser.parse_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../models/"

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames in the input directory
    imagePaths = op.get_images_on_directory(args.image_dir)
    start = time.time()

    # Process and display images
    for imagePath in imagePaths:
        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        print("Body keypoints: \n" + str(datum.poseKeypoints))

        # Save keypoints as JSON files
        output_json_path = os.path.join(args.output_dir, os.path.splitext(os.path.basename(imagePath))[0] + ".json")
        with open(output_json_path, 'w') as f:
            f.write(str(datum.poseKeypoints))

        if not args.no_display:
            cv2.imshow("OpenPose - Tutorial Python API", datum.cvOutputData)
            key = cv2.waitKey(15)
            if key == 27:
                break

    end = time.time()
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
except Exception as e:
    print(e)
    sys.exit(-1)
