# import sys
# if '/data/seeot-model/openpose' not in sys.path:
#     sys.path.append('/data/seeot-model/openpose')
import csv

import cv2
from PIL import Image
import shutil
import os

from .src.body import Body


def get_keypoints(img_path):
    # body_estimation = Body('models/openpose/model/body_pose_model.pth')
    #
    # # copy image into input/
    # shutil.copy(img_path, 'models/openpose/input/test.jpg')
    #
    # # set img_path
    # test_image = './models/openpose/input/test.jpg'
    #
    # # image resize
    # img = Image.open(test_image)
    # img_resize = img.resize((176, 256))
    # img_resize.save(test_image)
    #
    # # extract keypoints
    # oriImg = cv2.imread(test_image)
    # candidate, subset, keypoints_x, keypoints_y = body_estimation(oriImg)
    #
    # # print(len(candidate)) # number of keypoints
    # # print(len(subset))    # number of person
    #
    #
    # name==filename인 행이 있다면 해당 행 삭제
    with open('/data/seeot-server/models/dior/DATA_ROOT/fasion-annotation-test.csv', 'r') as file:
        reader = csv.reader(file, delimiter=':')
        for line in reader:
            print(line)
    #
    # # name:keypoints_y:keypoints_x
    # filename = img_path.split('/')[-1]
    # with open('/data/seeot-server/models/dior/DATA_ROOT/fasion-annotation-test.csv', 'a') as file:
    #     file.write(':'.join([filename, str([int(i) for i in keypoints_x]), str([int(i) for i in keypoints_y])]))
    #     file.writelines('\n')
    #
    # # print([int(i) for i in keypoints_x])
    # # print([int(i) for i in keypoints_y])

