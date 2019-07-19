"""
Created on Fri Jul 19 12:37:53 2019
Madeline Scott
This program is designed to read in images of protoplasts and return information on the 
density, average cell size, number of cells, and standard deviation of cell numbers in each image
(which will be used to determine the error in density)
"""
#%%
#importing needed packages

import cv2
import numpy as np
import os
import sys
import argparse

#%%

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--read_dir", type=str, default = os.getcwd(), \
                help="The directory in which the images are saved")
args = vars(ap.parse_args())

#%%
#data to be inputted by the user of the program
read_dir = args['read_dir']
im_area = 0.00625 * 11.158163 * 0.001 #volume of a square (uL) * number of squares per image * mL/uL

#%%
def count_circles(im):
    
    circles = cv2.HoughCircles(im,cv2.HOUGH_GRADIENT,1, minDist = 40,
                                param1=50, param2=35, minRadius = 30, maxRadius=70)
    
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(im,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(im,(i[0],i[1]), 2,(0,0,255),3)
    
    #resize so full image can be rendered in imshow
    h, w = gray.shape
    resize_gray = cv2.resize(im, (int(w/4), int(h/4)))
    
    #comment/uncomment to hide/show images of identified circles
#    cv2.imshow('detected circles', resize_gray)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    
    #return number of circles found
    return len(circles[0,:])


#%% 
found_circles = []
total_cells = 0
for image in os.listdir(read_dir):
    #read in the image
    im_dir = read_dir + '/' + image
    im = cv2.imread(im_dir)
    
    #convert to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    #count the cells and add it to the data array and the sum
    circs = count_circles(gray)
    found_circles.append(circs)
    total_cells = total_cells + circs
    

#%%
#calculate the density
vols = []
for image in found_circles:
    vols.append(image/im_area)

print("There are %.0f +/- %.0f protplasts/mL in your sample." % (np.average(vols), np.std(vols)))
    