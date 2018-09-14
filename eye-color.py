# face color analysis given eye center position

import sys
import os
import numpy as np
import cv2
import time
import argparse

# img1 l(200, 220) | r(305, 213)
# img2 l(295, 440) | r(595, 420)
# img3 l(128, 186) | r(260, 190)

parser = argparse.ArgumentParser()
parser.add_argument('--image_path', default='data/2.jpg')
parser.add_argument('--lx', type=int, default=295)
parser.add_argument('--ly', type=int, default=440)
parser.add_argument('--rx', type=int, default=595)
parser.add_argument('--ry', type=int, default=420)
args = parser.parse_args()

# define HSV color ranges for eyes color
Blue        =   ((166, 21, 50), (240, 100, 85))
BlueGray    =   ((166, 2, 25), (300, 20, 75))
Brown       =   ((2, 20, 20), (40, 100, 60))
BrownGray   =   ((20, 3, 30), (65, 60, 60))
BrownBlack  =   ((0, 10, 5), (40, 40, 25))
Green       =   ((60, 21, 50), (165, 100, 85))
GreenGray   =   ((60, 2, 25), (165, 20, 65))

def eye_color(image1, lcenter, rcenter):
    imgHSV = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    imgMask = np.zeros((image1.shape[0], image1.shape[1], 1))
    cv2.circle(imgMask, lcenter, 25, (255,255,255), -1)
    cv2.circle(imgMask, rcenter, 25, (255,255,255), -1)

    cv2.imwrite("mask.jpg", imgMask)

    h, s, v = cv2.split(imgHSV)

    cv2.circle(image, lcenter, 25, (0, 255, 0), 1)
    cv2.circle(image, rcenter, 25, (0, 255, 0), 1)
    cv2.imshow("img", image)
    #cv2.waitKey(0)
    cv2.imwrite("test.jpg", image)



if __name__ == '__main__':
    # read image 
    image_path = args.image_path
    lcenter = (args.lx, args.ly)
    rcenter = (args.rx, args.ry)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)    
    eye_color(image, lcenter, rcenter)