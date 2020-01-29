# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 22:21:36 2019

@author: mtsco
"""
#%%
import cv2
import numpy as np
import os
import argparse
import xlwt
import xlrd
from lmfit import Parameters, minimize
import statistics as stat

#%%
"""
This section is for static parameters that can be changed manually
"""
read_dir = r"C:\Users\mtsco\OneDrive\Documents\2019 Summer Klavins Lab\cell-counter\113002"
xl_in_path = r"C:\Users\mtsco\OneDrive\Documents\2019 Summer Klavins Lab\cell-counter\26Dec_Comparing_Manual_vs_Program_Cell_Counts.xls"

#%%
"""
This section of the code is devoted to reading in the values from the excel sheet and 
saving them to an array, which will be updated each time the optimization finishes
"""
xl_in = xlrd.open_workbook(xl_in_path)
comps_sheet = xl_in.sheet_by_name("Comparisons_without_outliers")
actual_vals = []
#go through and get the actual cell counts for each image
for col in range(1, comps_sheet.ncols):
    #the actual values are on the fourth row, which is why this is kinda weird
    actual_vals.append(comps_sheet.cell(4, col).value)
print("Actual Values: " + str(actual_vals) + "\n")

#%%
"""
This function takes in an array of found cells and compares it to the global array of accepted
values for each of the images. Then, it calculates:
    *the difference between the measured and accepted values for each image
    *the percent error for each image
    *the average error
    *standard deviation of all the errors
and, finally, returns an array of the number of standard deviations from the mean of the 
average that the cell counts for each image were.
"""
def residual(params):
    """
    
    First call the function that counts all of the cells
    in all the images and returns the array of their values
    (I think this is pass by reference and local variables just don't 
    get automatically trashed in Python)
    """
    print("residual")
    found_circles = count_all_cells(params['p1'].value, params['p2'].value)
    errors = [a-b for a, b in zip(actual_vals, found_circles)]
    #percent in decimal form because God is dead and we killed her
    percent_errs = [(a-b)/a for a, b in zip(actual_vals, errors)]
    mean_perc_err = np.mean(percent_errs)
    std_dev = stat.stdev(percent_errs)
    std_dev_arr = (percent_errs - mean_perc_err)/std_dev
    return std_dev_arr
    
#%%
"""
Function that goes through all the images in the directory
and calls the count_circles function on them
"""
def count_all_cells(p1, p2):
    print(p1, p2)
    found_circles = []
    for image in os.listdir(read_dir):
        if ".jpg" in image:
            #read in the image
            im_dir = read_dir + '/' + image
            im = cv2.imread(im_dir)
            
            #convert to grayscale
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            
            #count the cells and add it to the data array
            circs = count_circles(gray, p1, p2)
            found_circles.append(circs)
    return found_circles
  
#%%
def count_circles(im, p1, p2):
    print("count circles")
    #annotate this better and the parameters!!!
    circles = cv2.HoughCircles(im,cv2.HOUGH_GRADIENT,1, minDist = 40,
                                param1=p1, param2=p2, minRadius = 30, maxRadius=70)
    
    circles = np.uint16(np.around(circles))
#    for i in circles[0,:]:
#        # draw the outer circle
#        cv2.circle(im,(i[0],i[1]),i[2],(0,255,0),2)
#        # draw the center of the circle
#        cv2.circle(im,(i[0],i[1]), 2,(0,0,255),3)
    #return number of circles found
    return len(circles[0,:])

#%%
"""
Idk how passing parameter objects works so im doing something ICKY
"""
def res(params):
    """from initial count_all_cells() fucntion"""
    found_circles = []
    for image in os.listdir(read_dir):
        if ".jpg" in image:
            #read in the image
            im_dir = read_dir + '/' + image
            im = cv2.imread(im_dir)
            
            #convert to grayscale
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            
            """from initial count_circles() function"""
            circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1, minDist = 40,
                                param1=p['p1'].value, param2=p['p2'].value, minRadius = 30, maxRadius=70)
    
            if(type(circles) is None):
                found_circles.append(0)
            else:
                circles = np.uint16(np.around(circles))
                found_circles.append(len(circles[0,:]))
            
    """from original residual function"""
    errors = [a-b for a, b in zip(actual_vals, found_circles)]
    #percent in decimal form because God is dead and we killed her
    percent_errs = [(a-b)/a for a, b in zip(actual_vals, errors)]
    mean_perc_err = np.mean(percent_errs)
    std_dev = stat.stdev(percent_errs)
    std_dev_arr = (percent_errs - mean_perc_err)/std_dev
    return std_dev_arr
#%%
p = Parameters()
    #initial values determined by the ones I determined by guessing in the previous 
    #verison of this script, 50 and 35
p.add('p1', min = 0, value=40)
p.add('p2', min = 0, value=40)
          
result = minimize(res,p)
print("p1:%.3f,   p2:%.3f\nCell Counts:" % (p['p1'], p['p2']))
result.params.pretty_print()
#%%






