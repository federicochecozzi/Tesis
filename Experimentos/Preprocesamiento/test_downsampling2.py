# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:13:40 2024

@author: federicochecozzi
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
downsampling_factor = 8

##########################################
# Test Data
##########################################
start = time.time()
testFile = h5py.File("test_processed.h5",'r')     # testing data, unless the filename was changed

wavelengths = testFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]][()]

for sample in list(testFile["UNKNOWN"].keys()):
    tempData = testFile["UNKNOWN"][sample][()]
   
    if "testData" not in locals():
        testData = decimate(tempData.transpose(),q = downsampling_factor,axis = 1)
    else:
        testData = np.append(testData, decimate(tempData.transpose(),q = downsampling_factor,axis = 1), axis = 0)


# creates a two-dimensional array (matrix) containing the testing data
# each row represents a single spectrum
testFile.close()
del tempData, sample
end = time.time()
print('Execution time is:')
print(end - start)
#96.65290451049805
##########################################
# End of loading script
##########################################
# Returns 2 variables -> testData, wavelengths
##########################################

#Escritura en un nuevo archivo
testFile = h5py.File('test_d8_sc250.h5','w')

grp_unknown = testFile.create_group("Spectra")

grp_unknown.create_dataset('1', data = np.transpose(testData), compression="gzip", compression_opts=7)

testFile.close()
