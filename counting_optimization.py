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

#%%
"""
This section is for static parameters that can be changed manually
"""
read_dir = r"C:\Users\mtsco\OneDrive\Documents\2019 Summer Klavins Lab\cell-counter\113002"
xl_in_path = r"C:\Users\mtsco\OneDrive\Documents\2019 Summer Klavins Lab\cell-counter\26Dec_Comparing_Manual_vs_Program_Cell_Counts.xls"


"""
PLAN:
get new parameters
    go thru each image
        count the circles 
        add to array
find the difference in the actual counts vs the counted and get the percent error and then std dev in error, then an array of how many standard deviations from the average each value is
minimize the above function, changing the parameters
repeat until done
"""
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
print(actual_vals)

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
    found_circles = count_circles(params['p1'], params['p2'])
    errors = [a-b for a, b in zip(actual_vals, found_circles)]
    #percent in decimal form because God is dead and we killed her
    percent_errs = [(b-a)/b for a, b in zip(actual_vals, errors)]
    mean_perc_err = np.mean(percent_errs)
    
#%%
"""
Function that goes through all the images in the directory
and calls the count_circles function on them
"""
def count_all_cells(p1, p2):
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
  
#%%
def count_circles(im, p1, p2):
    
    #annotate this better and the parameters!!!
    circles = cv2.HoughCircles(im,cv2.HOUGH_GRADIENT,1, minDist = 40,
                                param1=p1, param2=p2, minRadius = 30, maxRadius=70)
    
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(im,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(im,(i[0],i[1]), 2,(0,0,255),3)
    #return number of circles found
    return len(circles[0,:])

#%%
"""
Defining the residual to be minimized. This residual will minimize for the standard deviation between
the percent error in each sample. 
"""
def residual(params, x, y):
    def f(x):
        #returning f(x), based on the current parameters
        #x is an array of all the x values
        
        return 
    yval = f(x)
    errs = 
    return errs

#%%
p = Parameters()
    p.add('p1', min = 0, value=10)
    p.add('p2', min = 0, value=5)
          
result = minimize(residual,p,args=(xdata,ydata, errors))
results.append(result)  

