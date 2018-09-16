# face color analysis given eye center position

import sys
import os
import numpy as np
import cv2
from scipy.spatial import distance as dist
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

class_name = ("Blue       ", "Blue Gray  ", "Brown      ", "Brown Gray ", "Brown Black", "Green      ", "Green Gray ", "Other")

# define eye color category rules in HSV space
def find_class(hsv):
    if (hsv[0] >= Blue[0][0]) and (hsv[0] <= Blue[1][0]) and (hsv[1] >= Blue[0][1]) and hsv[1] <= Blue[1][1] and (hsv[2] >= Blue[0][2]) and (hsv[2] <= Blue[1][2]):
        return 0
    elif (hsv[0] >= BlueGray[0][0]) and (hsv[0] <= BlueGray[1][0]) and (hsv[1] >= BlueGray[0][1]) and hsv[1] <= BlueGray[1][1] and (hsv[2] >= BlueGray[0][2]) and (hsv[2] <= BlueGray[1][2]):
        return 1
    elif (hsv[0] >= Brown[0][0]) and (hsv[0] <= Brown[1][0]) and (hsv[1] >= Brown[0][1]) and hsv[1] <= Brown[1][1] and (hsv[2] >= Brown[0][2]) and (hsv[2] <= Brown[1][2]):
        return 2
    elif (hsv[0] >= BrownGray[0][0]) and (hsv[0] <= BrownGray[1][0]) and (hsv[1] >= BrownGray[0][1]) and hsv[1] <= BrownGray[1][1] and (hsv[2] >= BrownGray[0][2]) and (hsv[2] <= BrownGray[1][2]):    
        return 3
    elif (hsv[0] >= BrownBlack[0][0]) and (hsv[0] <= BrownBlack[1][0]) and (hsv[1] >= BrownBlack[0][1]) and hsv[1] <= BrownBlack[1][1] and (hsv[2] >= BrownBlack[0][2]) and (hsv[2] <= BrownBlack[1][2]):
        return 4
    elif (hsv[0] >= Green[0][0]) and (hsv[0] <= Green[1][0]) and (hsv[1] >= Green[0][1]) and hsv[1] <= Green[1][1] and (hsv[2] >= Green[0][2]) and (hsv[2] <= Green[1][2]):
        return 5
    elif (hsv[0] >= GreenGray[0][0]) and (hsv[0] <= GreenGray[1][0]) and (hsv[1] >= GreenGray[0][1]) and hsv[1] <= GreenGray[1][1] and (hsv[2] >= GreenGray[0][2]) and (hsv[2] <= GreenGray[1][2]):
        return 6
    else:
        return 7

def eye_color(image, lcenter, rcenter):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imgMask = np.zeros((image.shape[0], image.shape[1], 1))
    
    eye_radius = dist.euclidean(lcenter, rcenter)
    eye_radius = eye_radius/15

    #cv2.circle(image, lcenter, int(eye_radius), (255,0,0), 2)
    #cv2.circle(image, rcenter, int(eye_radius), (255,0,0), 2)
    #cv2.imwrite("eye_roi.jpg", image)
   
    cv2.circle(imgMask, lcenter, int(eye_radius), (255,255,255), -1)
    cv2.circle(imgMask, rcenter, int(eye_radius), (255,255,255), -1)
    #cv2.imwrite("eye_roi_mask.jpg", imgMask)

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

    print "\n **** Eyes Color Percentage **** \n"
    for i in range(7):
        print class_name[i], ": ", round(float((eye_class[i])/float(total_vote))*100,2), "%"

if __name__ == '__main__':
    # read image 
    image = cv2.imread(args.image_path, cv2.IMREAD_COLOR)    

    # detect color percentage
    eye_color(image, (args.lx, args.ly), (args.rx, args.ry))