# face color analysis given eye center position

import sys
import os
import numpy as np
import cv2
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image_path', default='data/2.jpg')
parser.add_argument('--lx', type=int, default=200)
parser.add_argument('--ly', type=int, default=220)
parser.add_argument('--rx', type=int, default=305)
parser.add_argument('--ry', type=int, default=213)
args = parser.parse_args()

def eye_color(image1, lcenter, rcenter):
    imgHSV = cv2.cvtColor(image1, cv2.COLOR_BGR2HLS)

    cv2.circle(image, lcenter, 10, (0, 255, 0), 1)
    cv2.circle(image, rcenter, 10, (0, 255, 0), 1)
    cv2.imshow("img", image)
    #cv2.waitKey(0)
    cv2.imwrite("test.jpg", imgHSV)

if __name__ == '__main__':
    # read image 
    image_path = args.image_path
    lcenter = (args.lx, args.ly)
    rcenter = (args.rx, args.ry)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)    
    eye_color(image, lcenter, rcenter)