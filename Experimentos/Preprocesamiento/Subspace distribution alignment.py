# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 11:29:10 2024

@author: Federico Checozzi
"""

import os
import h5py
import numpy as np
from sklearn.decomposition import PCA

path = r"C:\Users\tiama\OneDrive\Documentos\Dataset EMSLIBS2019"
train_file = "train_d8_sc250_harder.h5"
val_file = "val_d8_sc250_harder.h5"
test_file = "test_d8_sc250.h5"

spectraCount = 250

with h5py.File(os.path.join(path,train_file),'r') as trainFile:
  for sample in list(trainFile["Spectra"].keys()):
    print(sample)
    tempData = trainFile["Spectra"][sample][()]
    if "trainData" not in locals():
        trainData = tempData.transpose()
    else:
        trainData = np.append(trainData, tempData.transpose(), axis = 0)

  trainClass = trainFile["Class"]["1"][()]

with h5py.File(os.path.join(path,val_file),'r') as valFile:
  for sample in list(valFile["Spectra"].keys()):
    print(sample)
    tempData = valFile["Spectra"][sample][()]
    if "valData" not in locals():
        valData = tempData.transpose()
    else:
        valData = np.append(valData, tempData.transpose(), axis = 0)

  valClass = valFile["Class"]["1"][()]

with h5py.File(os.path.join(path,test_file),'r') as testFile:
  for sample in list(testFile["Spectra"].keys()):
    print(sample)
    tempData = testFile["Spectra"][sample][()]
    if "testData" not in locals():
        testData = tempData.transpose()
    else:
        testData = np.append(testData, tempData.transpose(), axis = 0)

  testClass = testFile["Class"]["1"][()]

del tempData, sample

#Subpace distribution alignment, basado en https://github.com/sentaochen/Subspace-Distribution-Adaptation-Frameworks/blob/main/sa2013.py
#Para evitar tener que pensar demasiado sobre los centros de los datasets dejo que Scikit se encargue
#La implementación de Scikit centra/reconstruye los datos en base a lo que se usó en fit
#El original se queda en el espacio de componentes principales del target:
#pca = PCA(n_components=self.dimension)Adaptation
#Xs = pca.fit(Source_Data).components_.T
#Xt = pca.fit(Target_Data).components_.T
#Target_Aligned_Source_Data = Source_Data.dot(Xs).dot(Xs.T).dot(Xt)
#Target_Projected_Data = Target_Data.dot(Xt)
        
pca_s = PCA()
pca_t = PCA()

train_val_scores = pca_s.fit_transform(np.concatenate((trainData,valData), axis = 0))
pca_t.fit(testData)
#Ss = pca_s.components_.T
#St = pca_t.components_.T
Tts = pca_s.components_ @ pca_t.components_.T #Ss.T @ St
Ats = np.diag(np.sqrt(1/pca_s.singular_values_)) @ np.diag(np.sqrt(pca_t.singular_values_))#Es^-1/2 @ Et^1/2
#Transformación final, sin considerar los centros: Ss @ Tts @ Ats @ St.T
Target_Aligned_train_valData = pca_t.inverse_transform(train_val_scores @ Tts @ Ats) 

new_trainData = Target_Aligned_train_valData[:22000,]
new_valData = Target_Aligned_train_valData[22000:,]

with h5py.File(os.path.join(path,'train_d8_sc250_corrected.h5'),'w') as trainFile:

    grp_spectra = trainFile.create_group("Spectra")
    grp_class = trainFile.create_group("Class")

    for i in range(0,88):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(new_trainData[spectraCount*i:spectraCount*(i+1),:]), chunks = (new_trainData.shape[1], spectraCount), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = trainClass, chunks = (len(trainClass),), compression="gzip", compression_opts=7)

with h5py.File(os.path.join(path,'val_d8_sc250_corrected.h5'),'w') as valFile:

    grp_spectra = valFile.create_group("Spectra")
    grp_class = valFile.create_group("Class")

    for i in range(0,12):
        grp_spectra.create_dataset("%03d"%(i+1), data = np.transpose(new_valData[spectraCount*i:spectraCount*(i+1),:]), chunks = (new_valData.shape[1], spectraCount), compression="gzip", compression_opts=7)
    grp_class.create_dataset('1', data = valClass, chunks = (len(valClass),), compression="gzip", compression_opts=7)