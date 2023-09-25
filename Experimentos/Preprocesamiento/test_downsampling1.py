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

datasetpath = r"C:\Users\federicochecozzi\Documents\Tesis\Datasets"; 

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files

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
        testData = decimate(tempData.transpose(),3,axis = 1)
    else:
        testData = np.append(testData, decimate(tempData.transpose(),3,axis = 1), axis = 0)


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
testFile = h5py.File('test_downsampled.h5','w')

grp_unknown = testFile.create_group("UNKNOWN")
#grp_unknown1 = grp_unknown.create_group("1")
#grp_unknown2 = grp_unknown.create_group("2")
grp_wavelength = testFile.create_group("Wavelengths")

grp_unknown.create_dataset('1', data = np.transpose(testData[0:10000,:]), chunks = (13334, 10000), compression="gzip", compression_opts=7)
grp_unknown.create_dataset('2', data = np.transpose(testData[10000:,:]), chunks = (13334, 10000), compression="gzip", compression_opts=7)
grp_wavelength.create_dataset('1', data = wavelengths[0::3], chunks = (1, 13334), compression="gzip", compression_opts=7)

testFile.close()

