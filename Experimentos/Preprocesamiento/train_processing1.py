# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 15:18:00 2023

@author: Federico Checozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from skimage.restoration import denoise_wavelet
from pybaselines import Baseline

datasetpath = r"C:\Users\federicochecozzi\Documents\Tesis\Datasets"; 

baseline_fitter = Baseline(check_finite=False)

#Función que remueve línea de base, ruido y normaliza
def process_row(row):
    row = row - baseline_fitter.mwmv(row)[0]
    row = denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4')
    return (row - np.mean(row)) / np.std(row)

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files

##########################################
# Test Data
##########################################

start = time.time()

trainFile = h5py.File("train.h5",'r')     # testing data, unless the filename was changed

wavelengths = trainFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]][()]

for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
    if "trainData" not in locals():
        trainData = np.apply_along_axis(process_row, 1, tempData.transpose())
    else:
        trainData = np.append(trainData, np.apply_along_axis(process_row, 1, tempData.transpose()), axis = 0)
# creates a two-dimensional array (matrix) containing the training data
# each row represents a single spectrum

trainClass = trainFile["Class"]["1"][()]

# creates a two-dimensional array (matrix) containing the testing data
# each row represents a single spectrum
trainFile.close()
del tempData, sample

end = time.time()

print('Execution time is:')
print(end - start)

##########################################
# End of loading script
##########################################
# Returns 2 variables -> testData, wavelengths
##########################################

#Procesamiento
#https://stackoverflow.com/questions/45604688/apply-function-on-each-row-row-wise-of-a-numpy-array
#https://stackoverflow.com/questions/52673285/performance-of-pandas-apply-vs-np-vectorize-to-create-new-column-from-existing-c

#start = time.time()
#testData = np.apply_along_axis(process_row, 1, testData)
#end = time.time()

#print('Execution time is:')
#print(end - start)
#8202.967220783234s

#Escritura en un nuevo archivo
trainFile = h5py.File('train_processed.h5','w')

grp_spectra = trainFile.create_group("Spectra")
grp_wavelength = trainFile.create_group("Wavelengths")
grp_class = trainFile.create_group("Class")

for i in range(0,100):
    grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(trainData[500*i:500*(i+1),:]), chunks = (40002, 500), compression="gzip", compression_opts=7)
grp_wavelength.create_dataset('1', data = wavelengths, chunks = (1, 40002), compression="gzip", compression_opts=7)
grp_class.create_dataset('1', data = trainClass, chunks = (1, 50000), compression="gzip", compression_opts=7)

trainFile.close()

