# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 18:44:03 2023

@author: Federico Checozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from scipy.signal import decimate

datasetpath = r"D:\Tesis\Datasets"; 

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files

##########################################
# Train Data
##########################################
start = time.time()
trainFile = h5py.File("train_processed.h5",'r')     

wavelengths = trainFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]][()]

for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
   
    if "trainData" not in locals():
        trainData = decimate(tempData.transpose(),3,axis = 1)
    else:
        trainData = np.append(trainData, decimate(tempData.transpose(),3,axis = 1), axis = 0)

trainClass = trainFile["Class"]["1"][()]

trainFile.close()
del tempData, sample
end = time.time()
print('Execution time is:')
print(end - start)
#184.1315200328827s
##########################################
# End of loading script
##########################################

#Escritura en un nuevo archivo
trainFile = h5py.File('train_downsampled.h5','w')

grp_spectra = trainFile.create_group("Spectra")
grp_wavelength = trainFile.create_group("Wavelengths")
grp_class = trainFile.create_group("Class")

for i in range(0,100):
    grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(trainData[500*i:500*(i+1),:]), chunks = (13334, 500), compression="gzip", compression_opts=7)
grp_wavelength.create_dataset('1', data = wavelengths[0::3], chunks = (13334,), compression="gzip", compression_opts=7)
grp_class.create_dataset('1', data = trainClass, chunks = (50000,), compression="gzip", compression_opts=7)

trainFile.close()