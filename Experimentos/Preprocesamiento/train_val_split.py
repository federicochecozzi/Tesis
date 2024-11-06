# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:16:15 2024

@author: federicochecozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time

datasetpath = r"D:\Tesis\Datasets";  
spectraCount = 10                           # selecting the number of spectra for each sample (maximum of 500)§

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
            trainData = tempData.transpose()
        else:
            trainData = np.append(trainData, tempData.transpose(), axis = 0)
        if "trainClass" not in locals():
            trainClass = tempClass
        else:
            trainClass = np.append(trainClass, tempClass)
    else:
        if "valData" not in locals():
            valData = tempData.transpose()
        else:
            valData = np.append(valData, tempData.transpose(), axis = 0)
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
with h5py.File('train_splitted.h5','w') as trainFile:

    grp_spectra = trainFile.create_group("Spectra")
    grp_wavelength = trainFile.create_group("Wavelengths")
    grp_class = trainFile.create_group("Class")

    for i in range(0,88):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(trainData[spectraCount*i:spectraCount*(i+1),:]), chunks = (40002, spectraCount), compression="gzip", compression_opts=7)
    grp_wavelength.create_dataset('1', data = wavelengths, chunks = (40002,), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = trainClass, chunks = (88*spectraCount,), compression="gzip", compression_opts=7)

with h5py.File('val_splitted.h5','w') as valFile:

    grp_spectra = valFile.create_group("Spectra")
    grp_wavelength = valFile.create_group("Wavelengths")
    grp_class = valFile.create_group("Class")

    for i in range(0,12):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(valData[spectraCount*i:spectraCount*(i+1),:]), chunks = (40002, spectraCount), compression="gzip", compression_opts=7)
    grp_wavelength.create_dataset('1', data = wavelengths, chunks = (40002,), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = valClass, chunks = (12*spectraCount,), compression="gzip", compression_opts=7)
