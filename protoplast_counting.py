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
import argparse
import xlwt
from lmfit import Parameters, minimize
import os
import pandas as pd
import os
from FlowCytometryTools import *
from pylab import *
from FlowCytometryTools import FCPlate
import pprint
import csv
import pydent
from pydent import AqSession
from tqdm import tqdm


#%%
"""
This module is for data to be inputted by the user. All of them can also be 
inputted directly on the command line, however. It's really just whatever the user 
is more comfortable with. If I did my job right, this should be all you have to edit
to work the program.
"""

job_id = 113002
 #this is because there is no job -1. 
username = "maddyscott"
password = "Quix0tic-armadi11o"
image_area = 0.00625 * 11.158163 * 0.001 #this is actually our default image area, in mL

#%%
"""
This (disgusting, confusing) code changes any variables that were specified through the command
prompt, keeping all others the same as they are in the above module. This means the user has the option
for every variable to specify it on the command line or in the program. 
"""

#make a dictionary with all the values the user inputted assigned to variables
input_var_dict = {
        "job": job_id,
        "username": username,
        "password": password,
        "area": image_area #this is actually our default image area, in mL
        }

#create the argument parser and add arguments
ap = argparse.ArgumentParser()
ap.add_argument("-j", "--job", type=int, help = "The job ID for the protoplast transfection that produced\
                the images you want to be analyzed")
ap.add_argument("-u", "--username", type=str, help = "The Aquarium username of the user")
ap.add_argument('-p', "--password", type = str, help = "The Aquarium password of the user")
ap.add_argument("-a", "--area", type=int, help = "The area, in mL, of each image. This value must\
                be the same for each image.")
#make it into a dictionary
args = vars(ap.parse_args())

for key in args: #for every possible argument
    if type(args[key]) is not None: #if it was used
        input_var_dict[key] = args[key] #change the dictionary value to be the inputted value

#reassign the variables if they were changed through the command prompt
job_id = input_var_dict["job"] 
username = input_var_dict["username"]
password = input_var_dict["password"] 
image_area = input_var_dict["area"] 

#%%
"""
This module connects to Aquariumand downloads all the images
"""
prod = AqSession(username, password,"http://52.27.43.242/") #the URL is for the UW BIOFAB production server

#Enter a plan ID, get a list of operations.
job = prod.Job.find(job_id)
for file in job.uploads:
#     file.async_download(outdir=dir_path,overwrite=True)
cwd = os.getcwd()
dir_path= "%s/Images_%d" % (cwd, job_id)
os.mkdir(dir_path)
job_uploads=prod.Upload.where({'job': job.id})
for u in job_uploads:
    u.download(outdir=dir_path, filename = u.name, overwrite=False)

#%%
"""
Defines a dictionary with each item as key that leads to an array of the counts for each of its images
in the main code. Also, there is a function which adds a new image count value to the appropriate
item's count array
"""
items_and_counts = {}
def add_count_to_array(item_id, proto_count):
    if item_id in items_and_counts:
        items_and_counts[item_id].append(proto_count)
    else:
        items_and_counts[item_id] = []
        items_and_counts[item_id].append(proto_count)

#%%
"""
Function that parses the name of each image and returns the item number as an integer
"""
def id_parser(image_name):
    

#%%
"""
Old code for reading the images from a directory into which the images have already 
been downloaded.
"""

"""
ap.add_argument("-r", "--read_dir", type=str, default = os.getcwd(), \
                help="The directory in which the images to be read are saved")
args = vars(ap.parse_args())

#data to be inputted by the user of the program
read_dir = args['read_dir'] #would need to change reading in back to read_dir not dir_path
save_dir = str(os.getcwd()) + r"\26Dec2019"
print(save_dir)
"""
#%%
def count_circles(im, image):
    
    #annotate this better and the parameters!!!
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
    cv2.imwrite(str(save_dir) + "/" + image + "_found.jpg", resize_gray)
    #comment/uncomment to hide/show images of identified circles
#    cv2.imshow('detected circles', resize_gray)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    
    #return number of circles found
    return len(circles[0,:])


#%%
"""
making an excel sheet to track all the cells in each image so I can compare it to a
manual count and get the accuracy etc, stats stuff

wb = xlwt.Workbook()
sheet = wb.add_sheet("Comparisons")
"""
#%% 
found_circles = []
total_cells = 0
cells_in_each_image = []
col = 1
sheet.row(1).write(0, "Counted with program")

for image in os.listdir(dir_path):
    if ".jpg" in image:
        #read in the image
        im_dir = read_dir + '/' + image
        im = cv2.imread(im_dir)
        
        #convert to grayscale
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        
        #count the cells and add it to the data array and the sum
        circs = count_circles(gray, image)
        sheet.row(0).write(col, image)
        sheet.row(1).write(col, circs)
        col += 1

        found_circles.append(circs)
        total_cells = total_cells + circs
    

#wb.save("add name here")

#%%
#calculate the density
vols = []
for image in found_circles:
    vols.append(image/im_area)

print("There are %.0f +/- %.0f protplasts/mL in your sample." % (np.average(vols), np.std(vols)))


