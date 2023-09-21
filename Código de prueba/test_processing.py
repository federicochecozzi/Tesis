# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 20:34:57 2023

@author: Federico Checozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from skimage.restoration import denoise_wavelet
from pybaselines import Baseline

baseline_fitter = Baseline(check_finite=False)

#Función que remueve línea de base, ruido y normaliza
def process_row(row):
    row = row - baseline_fitter.mwmv(row)[0]
    row = denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4')
    return (row - np.mean(row)) / np.std(row)

## set number of spectra and path to the data files
os.chdir(r"C:\Users\tiama\OneDrive\Documentos\Dataset EMSLIBS2019")   # selecting the directory containing the data files

##########################################
# Test Data
##########################################

testFile = h5py.File("test.h5",'r')     # testing data, unless the filename was changed

wavelengths = testFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]][()]

for sample in list(testFile["UNKNOWN"].keys()):
    tempData = testFile["UNKNOWN"][sample][()]
   
    if "testData" not in locals():
        testData = tempData.transpose()
    else:
       testData = np.append(testData, tempData.transpose(), axis = 0)


# creates a two-dimensional array (matrix) containing the testing data
# each row represents a single spectrum
testFile.close()
del tempData, sample

##########################################
# End of loading script
##########################################
# Returns 2 variables -> testData, wavelengths
##########################################

#Procesamiento
#https://stackoverflow.com/questions/45604688/apply-function-on-each-row-row-wise-of-a-numpy-array
#https://stackoverflow.com/questions/52673285/performance-of-pandas-apply-vs-np-vectorize-to-create-new-column-from-existing-c

start = time.time()
testData = np.apply_along_axis(process_row, 1, testData)
end = time.time()

print('Execution time is:')
print(end - start)
#8202.967220783234s

#Escritura en un nuevo archivo
testFile = h5py.File('test_processed.h5','w')

grp_unknown = testFile.create_group("UNKNOWN")
#grp_unknown1 = grp_unknown.create_group("1")
#grp_unknown2 = grp_unknown.create_group("2")
grp_wavelength = testFile.create_group("Wavelengths")

grp_unknown.create_dataset('1', data = np.transpose(testData[0:10000,:]), chunks = (40002, 10000), compression="gzip", compression_opts=7)
grp_unknown.create_dataset('2', data = np.transpose(testData[10000:,:]), chunks = (40002, 10000), compression="gzip", compression_opts=7)
grp_wavelength.create_dataset('1', data = wavelengths, chunks = (1, 40002), compression="gzip", compression_opts=7)

testFile.close()