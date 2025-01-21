# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:26:18 2024

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
spectraCount = 250                           # selecting the number of spectra for each sample (maximum of 500)§

##########################################
# Train Data
##########################################
trainFile = h5py.File("train_d8_sc250_harder.h5",'r')     

for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
   
    if "trainData" not in locals():
        trainData = tempData.transpose()
    else:
        trainData = np.append(trainData, tempData.transpose(), axis = 0)

trainClass = trainFile["Class"]["1"][()]

trainFile.close()

##########################################
# Val Data
##########################################
valFile = h5py.File("val_d8_sc250_harder.h5",'r')     

for sample in list(valFile["Spectra"].keys()):
    print(sample)
    tempData = valFile["Spectra"][sample][()]
   
    if "valData" not in locals():
        valData = tempData.transpose()
    else:
        valData = np.append(valData, tempData.transpose(), axis = 0)

valClass = valFile["Class"]["1"][()]

valFile.close()

##########################################
# test Data
##########################################
testFile = h5py.File("test_d8_sc250.h5",'r')     # testing data, unless the filename was changed

for sample in list(testFile["Spectra"].keys()):
    tempData = testFile["Spectra"][sample][()]
   
    if "testData" not in locals():
        testData = tempData.transpose()
    else:
       testData = np.append(testData, tempData.transpose(), axis = 0)

testClass = testFile["Class"]["1"][()]

testFile.close()

del tempData, sample

##########################################
# End of loading script
##########################################

start = time.time()
pca = PCA().fit(trainData)
train_pca = pca.transform(trainData)
val_pca   = pca.transform(valData)
test_pca  = pca.transform(testData)

train_pca_median = np.median(train_pca, axis = 0)
val_pca_median = np.median(val_pca, axis = 0)
test_pca_median = np.median(test_pca, axis = 0)

new_val_pca = val_pca - val_pca_median + train_pca_median
new_test_pca = test_pca - test_pca_median + train_pca_median

new_valData = pca.inverse_transform(new_val_pca)
new_testData = pca.inverse_transform(new_test_pca)

end = time.time()
print('Execution time is:')
print(end - start) #45.132824420928955s

with h5py.File('val_d8_sc250_harder_corrected.h5','w') as valFile:

    grp_spectra = valFile.create_group("Spectra")
    grp_class = valFile.create_group("Class")

    for i in range(0,12):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(new_valData[spectraCount*i:spectraCount*(i+1),:]), chunks = (new_valData.shape[1], spectraCount), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = valClass, chunks = (len(valClass),), compression="gzip", compression_opts=7)

with h5py.File('test_d8_sc250_corrected.h5','w') as testFile:

    grp_unknown = testFile.create_group("Spectra")
    grp_class = testFile.create_group("Class")

    grp_unknown.create_dataset('1', data = np.transpose(new_testData), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = testClass, chunks = (len(testClass),), compression="gzip", compression_opts=7)
