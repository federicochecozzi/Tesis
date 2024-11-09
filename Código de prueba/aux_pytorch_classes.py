# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 18:55:37 2024

@author: federicochecozzi
"""

#Versión pensada para  computadoras con RAM limitada

import h5py
import numpy as np
import os
import torch
from torch.utils.data import Dataset
from torchvision.transforms.v2 import Lambda

def convert_to_2dtensor(array):
    return torch.tensor(np.expand_dims(array.reshape((226,177)),axis = 0))

class EMSLIBS2019Dataset(Dataset):
    
    def __init__(self, path, spectra_file, label_file = None, transform = None, target_transform = None):
        
        self.spectra_file = spectra_file
        self.path = path
        os.chdir(path)
        with h5py.File(self.spectra_file,'r') as spectra_dataset:
            
            #Las etiquetas pueden estar en un archivo csv separado o dentro del hdf5
            if label_file: 
                self.labels = np.loadtxt(label_file, dtype = 'int')
            else:
                self.labels = spectra_dataset["Class"]["1"][()]
            
            #Extraigo nombre del grupo con los espectros, puede variar según el archivo
            key_set = set(spectra_dataset.keys())
            self.spectra_key = tuple(key_set - {"Wavelengths","Class"})[0]
            
            #Cuento la cantidad de espectros en el archivo
            counter = 0
            for sample in list(spectra_dataset[self.spectra_key].keys()):
                counter += spectra_dataset[self.spectra_key][sample].shape[1]
            self.length = counter
            
            #también extraigo el número de datasets, lo necesito para hacer aritmética de índices
            self.spectra_per_dataset = counter // len(spectra_dataset[self.spectra_key].keys())
        
        self.transform = transform
        self.target_transform = target_transform
        
    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        os.chdir(self.path)
        with h5py.File(self.spectra_file,'r') as spectra_dataset:
            if self.spectra_key == "Spectra":
                sample = "%03d"%(idx // self.spectra_per_dataset + 1)
            else:
                sample = str(idx // self.spectra_per_dataset + 1)
            tempData = spectra_dataset[self.spectra_key][sample][()]
            spectra = tempData[:,idx % self.spectra_per_dataset].transpose()
        
        label = self.labels[idx]
        if self.transform:
            spectra = self.transform(spectra)
        if self.target_transform:
            label = self.target_transform(label)
        return spectra, label
    
path = r"C:\Users\tiama\OneDrive\Documentos\Dataset EMSLIBS2019"
spectra_file = "test.h5"
label_file = "test_labels.csv"
data = EMSLIBS2019Dataset(path = path, spectra_file = spectra_file, label_file = label_file, 
                          transform = Lambda(convert_to_2dtensor),
                          target_transform = Lambda(torch.tensor))
print(len(data))
spectra,label = data[1]