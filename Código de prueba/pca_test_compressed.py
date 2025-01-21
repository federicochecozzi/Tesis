# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:04:29 2024

@author: federicochecozzi
"""

## import libraries
import os
import h5py
import numpy as np
import time
from sklearn.decomposition import PCA

datasetpath = r"D:\Tesis\Datasets"; 

## set number of spectra and path to the data files
os.chdir(datasetpath)   # selecting the directory containing the data files

##########################################
# Train Data
##########################################
trainFile = h5py.File("train_d8_sc250_harder.h5",'r')     

for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
   
    if "Data" not in locals():
        Data = tempData.transpose()
    else:
        Data = np.append(Data, tempData.transpose(), axis = 0)

trainFile.close()
del tempData, sample

##########################################
# End of loading script
##########################################

start = time.time()
Data_reduced = PCA().fit_transform(Data)
end = time.time()
print('Execution time is:')
print(end - start) #43.29492783546448s