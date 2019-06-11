# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:47:06 2019

@author: mtsco
"""

from pydent import AqSession
import lmfit
from FlowCytometryTools import FCPlate
import os
import csv
from pylab import *
import pprint
import numpy


#open password file
f = open("Aquarium_password.txt", "r")
if f.mode != "r":
    raise Exception('Lol ur file aint where it should be')
pw = f.read();
session = AqSession("maddyscott", pw, "http://52.27.43.242/")


plan_id = 33688
job_id = 100065

"""
plan = session.Plan.find(plan_id)

job = session.Job.find(job_id)
# for file in job.uploads:
#     file.async_download(outdir=dir_path,overwrite=True)
cwd = os.getcwd()
dir_path= cwd + '/' + str(job.id)
os.mkdir(dir_path)

job_uploads=session.Upload.where({'job': job.id})
# prod.Upload._download_files(job_uploads, dir_path, overwrite)
for u in job_uploads:
    u.download(outdir=dir_path, filename = u.name, overwrite=False)
"""

#Enter a plan ID, get a list of operations.
plan = session.Plan.find(plan_id)
ops = plan.operations
yd_ops = filter(lambda x: x.operation_type_id == 563 and x.status == 'done', ops)

#2. Define the metadata table
plate_metadata = []

for op in yd_ops:
    op_metadata = []
    wells = filter(lambda x: x.key == 'sample_plate_location', op.data_associations)
    for well in wells:
        op_metadata.append(well.object['sample_plate_location'])
    overnite = (filter(lambda x: x.name == 'Overnight', op.field_values))
    for on in overnite:
        op_metadata.append(on.sid)
    role =  (filter(lambda x: x.name == 'Sample_role', op.field_values))
    for r in role:
        op_metadata.append(r.value)
    plate_metadata.append(op_metadata)

for dat in plate_metadata:
    if len(dat[0][0]) < 3:
        dat[0][0] = dat[0][0][0] + '0' + dat[0][0][1]
    if len(dat[0][1]) < 3:
        dat[0][1] = dat[0][1][0] + '0' + dat[0][1][1]
    if len(dat[0]) > 2:
        if len(dat[0][2]) < 3:
            dat[0][2] = dat[0][2][0] + '0' + dat[0][2][1]
        if len(dat[0][3]) < 3:
            dat[0][3] = dat[0][3][0] + '0' + dat[0][3][1]

well_info = {}

for dat in plate_metadata:
    well_info[dat[0][0]] = [dat[1],dat[2]]
    well_info[dat[0][1]] = [dat[1],dat[2]]
    if len(dat[0]) > 2:
        well_info[dat[0][2]] = [dat[1],dat[2]]
        well_info[dat[0][3]] = [dat[1],dat[2]]
    
pprint.pprint(well_info)

cwd = os.getcwd()
dir_path= cwd + '/' + str(job_id)
for file in os.listdir(dir_path):
    if '.fcs' in file and 'Well_' not in file:
        file_path = dir_path + '/' + file
        rename_file_path = dir_path + '/' + 'Well_' + file
        os.rename(file_path, rename_file_path)
        print('{} was changed to Well_{}'.format(file, file))
        
plate = FCPlate.from_dir(ID='Test Plate', path=dir_path, parser='name')
plate = plate.dropna()
print(plate)

for well in plate:
    for info in well_info:
        if well == info:
            plate[well].meta["Sample ID"] = well_info[info][0]
            plate[well].meta["Role"] = well_info[info][1]

tplate = plate.transform('hlog', channels=['FSC-A', 'SSC-A'])

figure(figsize=(20,10));
title('FSC vs SSC - {}'.format(plate.ID))
tplate.plot(['FSC-A','SSC-A'], bins=100, wspace=0.2, hspace=0.2, alpha=0.9);
tplate = plate.transform('hlog', channels=['FL1-A'])
figure(figsize=(20,10));
tplate.plot(['FL1-A'], xlim=(0,10000),bins = 100, color = 'green')


sample_ids = []

for well in plate:
    sample_ids.append(plate[well].meta["Sample ID"])

uniq_ids = list(set(sample_ids))

array_of_medians = []

for i in uniq_ids:
    medians = []
    for well in plate:
        if plate[well].meta["Sample ID"] == i:
            medians.append(plate[well]['FL1-A'].median())
    array_of_medians.append(medians)
    
mean_of_medians = []
stdev_of_medians = []
for m in array_of_medians:
    mean_of_medians.append(np.mean(m).round(2))
    stdev_of_medians.append(np.std(m).round(1))
    
print(mean_of_medians)
print(stdev_of_medians)

d = {'Mean': mean_of_medians,'StDev': stdev_of_medians}


medians = pd.DataFrame(data = array_of_medians, index= uniq_ids, columns=['Median FL1-A 1', 'Median FL1-A2','Median FL1-A3'])
means = pd.DataFrame(d, index= uniq_ids)


print(medians)
print(means)

figure()
means.plot.bar(y='Mean',yerr='StDev', legend = False, figsize = (15,15)).set(xlabel="Sample ID", ylabel="Mean FL1-A from n = 3, bars are StDev");
savefig('YeastDisplay_190116.png')











