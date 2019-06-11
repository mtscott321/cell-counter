# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:18:36 2019
Following the FCT tutorial. 
For more information, go to

https://eyurtsev.github.io/FlowCytometryTools/tutorial.html

@author: mtsco
"""

import FlowCytometryTools as fct
from FlowCytometryTools import test_data_dir, test_data_file, FCMeasurement
datadir = test_data_dir
datafile = test_data_file
sample = FCMeasurement(ID = 'Test Sample', datafile = datafile)
print(sample.channel_names)
print(sample.channels)
print(type(sample.meta))
print(sample.meta.keys())
print(sample.meta['$SRC'])
print(type(sample.data)) #pandas.DataFrame
print(type(sample.data.values)) #numpy array
#when working with DataFrame
data= sample.data
#how many events?
print(data.shape[0])
#median fluorescence on the Y2-A channel?
print(data['Y2-A'].median())
#transforming FS data 
#if the range is small, make b smaller. adjust to tranform differently
tsample = sample. transform('hlog', channels=['Y2-A', 'B1-A'], b=500)

#plotting
from pylab import *
#figure()
#alpha controls how dark the color is (this is 70% dark). Not needed.
tsample.plot(['Y2-A'], color = 'green', alpha = 0.7, bins = 100)
#makes a new figure
figure()
tsample.plot(['B1-A', 'Y2-A'])
figure()
#makes the second orange plot.
tsample.plot(['B1-A', 'Y2-A'], cmap=cm.Oranges, colorbar=False);
#view interactively DONT RUN BC IT'S TERRIBLE
#tsample.view_interactively(backend='wx')
#2d scatter plot
figure()
#red plot
tsample.plot(['B1-A', 'Y2-A'], kind='scatter', color='red', s=1, alpha=0.3);

#gating
from FlowCytometryTools import ThresholdGate, PolyGate
#to create a gate, need: coordinates, channel name, region
y2_gate = ThresholdGate(1000.0, ['Y2-A'], region='above')
#plot the gate we applied
figure()
tsample.plot(['Y2-A'], gates=[y2_gate], bins=100);
title('Gate Plotted')
#apply the gate
gated_sample = tsample.gate(y2_gate)
print(gated_sample.get_data().shape[0])
figure()
gated_sample.plot(['Y2-A'], color = 'y', bins = 100)
title('Gated Sample')
#more information on how to compare the gates available here
#https://eyurtsev.github.io/FlowCytometryTools/tutorial.html

#loading data
from FlowCytometryTools import FCPlate
sample1 = FCMeasurement('B1', datafile = datafile)
sample2 = FCMeasurement('D2', datafile = datafile)
#use the sample ID as their position on the plate
plate1 = FCPlate('demo plate', [sample1, sample2], 'name', shape = (4,3))
print(plate1)
#better way to import
plate = FCPlate.from_dir(ID='Demo Plate', path=datadir, parser='name')
print(plate)
#this transform is very important!!!
plate = plate.transform('hlog', channels=['Y2-A', 'B1-A'])
#drop empty rows and columns
plate = plate.dropna()
print(plate)
#to plot the whole plate, use this
figure()
plate.plot(['Y2-A'], bins = 100)
#or this more complex version
plate.plot(['B1-A', 'Y2-A'], bins=100, wspace=0.2, hspace=0.2)
#access single wells on a plate
figure()
plate['A3'].plot(['Y2-A'], color = 'b', bins = 100)

#counting
total_counts = plate.counts()
y2_count = plate.gate(y2_gate).counts()
#to get outside of the gate
outside_y2 = plate.gate(~y2_gate).counts()

#median fluorescence
def calc_median(well):
    data= well.get_data()
    return data['Y2-A'].median()

print(plate.apply(calc_median))
