# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 15:37:36 2025

@author: federicochecozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from scipy.signal import decimate

datasetpath = r"D:\Tesis\Datasets"; 
downsampling_factor = 4
output_file = 'train_downsampled_d4.h5'

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
        trainData = decimate(tempData.transpose(),downsampling_factor,axis = 1)
    else:
        trainData = np.append(trainData, decimate(tempData.transpose(),downsampling_factor,axis = 1), axis = 0)

trainClass = trainFile["Class"]["1"][()]

trainFile.close()
del tempData, sample
end = time.time()
print('Execution time is:')
print(end - start)
#264.80650663375854s
##########################################
# End of loading script
##########################################

#Escritura en un nuevo archivo
trainFile = h5py.File(output_file,'w')

grp_spectra = trainFile.create_group("Spectra")
grp_wavelength = trainFile.create_group("Wavelengths")
grp_class = trainFile.create_group("Class")

for i in range(0,100):
    grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(trainData[500*i:500*(i+1),:]), chunks = (int(np.ceil(40002/downsampling_factor)), 500), compression="gzip", compression_opts=7)
grp_wavelength.create_dataset('1', data = wavelengths[0::downsampling_factor], chunks = (int(np.ceil(40002/downsampling_factor)),), compression="gzip", compression_opts=7)
grp_class.create_dataset('1', data = trainClass, chunks = (50000,), compression="gzip", compression_opts=7)

trainFile.close()
