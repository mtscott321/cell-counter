#%%
"""
Import needed modules (ideally will have an environment.yml file but that comes later)
"""
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
All of the hard-coded things that need to be edited each time
"""
aq_username = "delangeo"
aq_password = "Dextrins8!"
aq_url = "http://52.27.43.242/" #Leave as is for UW BIOFAB server. 
plan_id = 37132
job_id = 113002
host_folder = os.getcwd() #Folder that will host a new directory with the data files and figures for this analaysis
new_folder_name = 'protoplast_17_Dec' #Name for new directory, which will be a subdirectory of 'host folder'

#%%
prod = AqSession(aq_username, aq_password, aq_url ) # Production Database

#Enter a plan ID, get a list of operations.
plan = prod.Plan.find(plan_id)
job = prod.Job.find(job_id)
# for file in job.uploads:
#     file.async_download(outdir=dir_path,overwrite=True)
cwd = os.getcwd()
dir_path= cwd + '/' + new_folder_name
os.mkdir(dir_path)

# uploads = job.uploads
job_uploads=prod.Upload.where({'job': job.id})
# prod.Upload._download_files(job_uploads, dir_path, overwrite)
for u in job_uploads:
    u.download(outdir=dir_path, filename = u.name, overwrite=False)
    
