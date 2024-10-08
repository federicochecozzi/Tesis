# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:02:57 2024

@author: federicochecozzi
"""

## import libraries
import os
import h5py
import time

datasetpath = r"D:\Tesis\Datasets";  

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files

##########################################
# Train Data
##########################################

start = time.time()

trainFile = h5py.File("train.h5",'r')     

counter = 0
for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    counter += trainFile["Spectra"][sample].shape[1]

print(counter)

trainFile.close()
del counter, sample

end = time.time()

print('Execution time is:')
print(end - start)