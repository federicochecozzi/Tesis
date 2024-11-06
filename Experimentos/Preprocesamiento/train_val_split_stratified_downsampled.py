# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:48:24 2024

@author: federicochecozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from scipy.signal import decimate
from sklearn.model_selection import train_test_split

datasetpath = r"D:\Tesis\Datasets"; 

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files
spectraCount = 250                           # selecting the number of spectra for each sample (maximum of 500)
downsampling_factor = 8

##########################################
# Train Data
##########################################
start = time.time()
trainFile = h5py.File("train_processed.h5",'r')     

for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
    tempData = tempData[:,0:spectraCount]
   
    if "Data" not in locals():
        Data = decimate(tempData.transpose(),q = downsampling_factor,axis = 1)
    else:
        Data = np.append(Data, decimate(tempData.transpose(),q = downsampling_factor,axis = 1), axis = 0)

Class = trainFile["Class"]["1"][()]
for i in range(0,50000,500):
    if i == 0:
        tempClass = Class[0:spectraCount]
    else:
        tempClass = np.append(tempClass, Class[i:(i+spectraCount)])
Class = tempClass

trainFile.close()
del tempClass,tempData, sample
end = time.time()
print('Execution time is:')
print(end - start)
#184.1315200328827s
##########################################
# End of loading script
##########################################

trainData, valData, trainClass, valClass = train_test_split(Data, Class, test_size=0.3, random_state=42)

#Escritura en un nuevo archivo
trainFile = h5py.File('train_d8_sc250.h5','w')

grp_spectra = trainFile.create_group("Spectra")
grp_class = trainFile.create_group("Class")

grp_spectra.create_dataset("1", data = np.transpose(trainData), compression="gzip", compression_opts=7)
grp_class.create_dataset('1', data = trainClass, chunks = (len(trainClass),), compression="gzip", compression_opts=7)

trainFile.close()

#Escritura en un nuevo archivo
valFile = h5py.File('val_d8_sc250.h5','w')

grp_spectra = valFile.create_group("Spectra")
grp_class = valFile.create_group("Class")

grp_spectra.create_dataset("1", data = np.transpose(valData), compression="gzip", compression_opts=7)
grp_class.create_dataset('1', data = valClass, chunks = (len(valClass),), compression="gzip", compression_opts=7)

valFile.close()