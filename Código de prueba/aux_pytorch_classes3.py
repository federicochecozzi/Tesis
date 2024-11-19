# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 19:18:13 2024

@author: federicochecozzi
"""

#Versión que carga todo el dataset en memoria y usa pseudoetiquetas para aprendizaje semisupervisado

import h5py
import numpy as np
import os
import torch
from torch.utils.data import Dataset
from torchvision.transforms.v2 import Lambda

def convert_to_2dtensor(array,index,shape):
    return torch.tensor(np.expand_dims(array[index[0]:index[1]].reshape(shape),axis = 0))

class psEMSLIBS2019Dataset(Dataset):
    
    def __init__(self, path, spectra_file, label_file, transform = None, target_transform = None):
        
        #Las etiquetas pueden estar en un archivo csv separado o dentro del hdf5
        self.labels = np.loadtxt(os.path.join(path,label_file), dtype = 'int')
        #en un archivo con pseudoetiquetas, los espectros que no van a usarse valen 0
        self.indexes = np.nonzero(self.labels)[0]
        
        with h5py.File(os.path.join(path,spectra_file),'r') as spectra_dataset:
            
            #Extraigo nombre del grupo con los espectros, puede variar según el archivo
            key_set = set(spectra_dataset.keys())
            spectra_key = tuple(key_set - {"Wavelengths","Class"})[0]
            
            first_chunk = True
            
            #Cargo en los espectros
            for sample in list(spectra_dataset[spectra_key].keys()):
                tempData = spectra_dataset[spectra_key][sample][()]
                if first_chunk:
                    self.spectraData = tempData.transpose()
                    first_chunk = False
                else:
                    self.spectraData = np.append(self.spectraData, tempData.transpose(), axis = 0)
        
        self.transform = transform
        self.target_transform = target_transform
        
    def __len__(self):
        return len(self.indexes)

    def __getitem__(self, idx):
        spectra = self.spectraData[self.indexes[idx]]        
        label = self.labels[self.indexes[idx]]
        if self.transform:
            spectra = self.transform(spectra)
        if self.target_transform:
            label = self.target_transform(label)
        return spectra, label
    
path = "D:\Tesis\Datasets"#r"C:\Users\tiama\OneDrive\Documentos\Dataset EMSLIBS2019"
spectra_file = "test_d8_sc250.h5"
label_file = "testpred_e15_16112024.txt"
index = (0,-1)
shape = (100,50)
data = psEMSLIBS2019Dataset(path = path, spectra_file = spectra_file, label_file = label_file, 
                          transform = Lambda(lambda array: convert_to_2dtensor(array,index,shape)),
                          target_transform = Lambda(torch.tensor))
print(len(data))
spectra,label = data[1]
