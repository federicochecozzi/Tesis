# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:26:16 2024

@author: federicochecozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from scipy.signal import decimate

datasetpath = r"D:\Tesis\Datasets";  
spectraCount = 250                           # selecting the number of spectra for each sample (maximum of 500)§
downsampling_factor = 8

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files

##########################################
# Train Data
##########################################

start = time.time()

trainFile = h5py.File("train_processed.h5",'r')     

wavelengths = trainFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]][()]

nonsplittedClass = trainFile["Class"]["1"][()]

next_class_to_look = 1

for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
    tempData = tempData[:,0:spectraCount]
    i = (int(sample) - 1) * 500#índice del primer espectro de una muestra
    tempClass = nonsplittedClass[i:(i+spectraCount)]
    if tempClass[0] != next_class_to_look:#Veo la clase del primer espectro para saber la clase de la muestra
        if "trainData" not in locals():
            trainData = decimate(tempData.transpose(),q = downsampling_factor,axis = 1)
        else:
            trainData = np.append(trainData, decimate(tempData.transpose(),q = downsampling_factor,axis = 1), axis = 0)
        if "trainClass" not in locals():
            trainClass = tempClass
        else:
            trainClass = np.append(trainClass, tempClass)
    else:
        if "valData" not in locals():
            valData = decimate(tempData.transpose(),q = downsampling_factor,axis = 1)
        else:
            valData = np.append(valData, decimate(tempData.transpose(),q = downsampling_factor,axis = 1), axis = 0)
        if "valClass" not in locals():
            valClass = tempClass
        else:
            valClass = np.append(valClass, tempClass)
        next_class_to_look += 1


trainFile.close()
del tempData, tempClass, sample

end = time.time()

print('Execution time is:')
print(end - start)
#10587.120632886887s
##########################################
# End of loading script
##########################################

#Escritura en un nuevo archivo
with h5py.File('train_d8_sc250_harder.h5','w') as trainFile:

    grp_spectra = trainFile.create_group("Spectra")
    grp_class = trainFile.create_group("Class")

    for i in range(0,88):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(trainData[spectraCount*i:spectraCount*(i+1),:]), chunks = (trainData.shape[1], spectraCount), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = trainClass, chunks = (len(trainClass),), compression="gzip", compression_opts=7)

with h5py.File('val_d8_sc250_harder.h5','w') as valFile:

    grp_spectra = valFile.create_group("Spectra")
    grp_class = valFile.create_group("Class")

    for i in range(0,12):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(valData[spectraCount*i:spectraCount*(i+1),:]), chunks = (valData.shape[1], spectraCount), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = valClass, chunks = (len(valClass),), compression="gzip", compression_opts=7)