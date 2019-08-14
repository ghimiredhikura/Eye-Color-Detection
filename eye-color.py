# face color analysis given eye center position

import sys
import os
import numpy as np
import cv2
import argparse
import time

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

# define HSV color ranges for eyes colors
Blue        =   ((166, 21, 50), (240, 100, 85))
BlueGray    =   ((166, 2, 25), (300, 20, 75))
Brown       =   ((2, 20, 20), (40, 100, 60))
BrownGray   =   ((20, 3, 30), (65, 60, 60))
BrownBlack  =   ((0, 10, 5), (40, 40, 25))
Green       =   ((60, 21, 50), (165, 100, 85))
GreenGray   =   ((60, 2, 25), (165, 20, 65))

class_name = ("Blue       ", "Blue Gray  ", "Brown      ", "Brown Gray ", "Brown Black", "Green      ", "Green Gray ", "Other")

def check_color(hsv, color):
    if (hsv[0] >= color[0][0]) and (hsv[0] <= color[1][0]) and (hsv[1] >= color[0][1]) and hsv[1] <= color[1][1] and (hsv[2] >= color[0][2]) and (hsv[2] <= color[1][2]):
        return True
    else:
        return False

# define eye color category rules in HSV space
def find_class(hsv):
    if check_color(hsv, Blue):
        return 0
    elif check_color(hsv, BlueGray):
        return 1
    elif check_color(hsv, Brown):
        return 2
    elif check_color(hsv, BrownGray):
        return 3
    elif check_color(hsv, BrownBlack):
        return 4
    elif check_color(hsv, Green):
        return 5
    elif check_color(hsv, GreenGray):
        return 6
    else:
        return 7

def eye_color(image, lc, rc):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imgMask = np.zeros((image.shape[0], image.shape[1], 1))
    
    eye_radius = np.linalg.norm(np.array(lc)-np.array(rc))
    eye_radius = eye_radius/15
   
    cv2.circle(imgMask, lc, int(eye_radius), (255,255,255), -1)
    cv2.circle(imgMask, rc, int(eye_radius), (255,255,255), -1)

    h = image.shape[0]
    w = image.shape[1]

    eye_class = []
    for i in range(8):
        eye_class.append(0)
    
    for y in range(0, h):
        for x in range(0, w):
            mask_val = imgMask[y, x]
            if mask_val != 0:
                eye_color_class = find_class(imgHSV[y,x])
                if eye_color_class != -1:
                    eye_class[eye_color_class] += 1

    total_vote = 0
    for i in range(7):
        total_vote = total_vote+eye_class[i]

    print("\n **** Eyes Color Percentage **** \n")
    for i in range(7):
        print(class_name[i], ": ", round(float((eye_class[i])/float(total_vote))*100,2), "%")

if __name__ == '__main__':
    # read image 
    image = cv2.imread(args.image_path, cv2.IMREAD_COLOR)    

    # detect color percentage
    eye_color(image, (args.lx, args.ly), (args.rx, args.ry))