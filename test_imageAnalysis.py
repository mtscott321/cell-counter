# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:07:05 2019

@author: mtsco
"""

import cv2
from IPython.display import Image, display
import numpy as np

r"""
#display(Image(filename=r'C:\Users\mtsco\OneDrive\Documents\Miscellaneous\protoplast_sample.jpg'))
#np = Image(filename=r'C:\Users\mtsco\OneDrive\Documents\Miscellaneous\protoplast_sample.jpg')

import matplotlib.pyplot as plt
avg = np.average(rgb, axis=-1)
avg.shape(16, 16)
#plt.imshow(avg, cmap=plt.get_cmap('gray'))
plt.show()
"""


image = cv2.imread(r'C:\Users\mtsco\OneDrive\Documents\Miscellaneous\5.jpg')



gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
resize_gray = cv2.resize(gray, (int(w/10), int(h/10)))
#cv2.imwrite("resizeimg.tif", resize_gray)
th2 = cv2.adaptiveThreshold(resize_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,-10)
 
#trash, no_adap = cv2.threshold(resize_gray,200,0,cv2.THRESH_BINARY)

blur = cv2.GaussianBlur(th2,(5,5),0)
#ret3, th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
 
 
kernel = np.ones((2,2),np.uint8)
for i in range (4):
    blue = cv2.erode(blur,kernel,iterations = 7)
    blur = cv2.dilate(blur,kernel,iterations = 1)
    
ret3, th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
"""
erosion = cv2.erode(th3,kernel,iterations = 1)
dilation = cv2.dilate(erosion,kernel,iterations = 3)
"""

cv2.imshow('gray', th3)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("8bit_5.jpg",resize_gray)



