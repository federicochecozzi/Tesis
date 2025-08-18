# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 11:17:20 2025

@author: Federico Checozzi
"""

#Dataset: https://figshare.com/articles/dataset/LIBS_spectra_Fe-Co_certified_sample_set/21984989

import h5py
import pandas as pd
import json
import numpy as np
import os


def load_h5_as_df(filepath):
    """
    Function for loading data from an h5 file and returning it as a pandas DataFrame.

    Args:
        filepath (str or Path) : path to the h5 file.

    Returns:
        pd.DataFrame : data matrix
        pd.Series : samples vector
        dict : experimental parameters
    """
    with h5py.File(filepath, 'r') as h5_file:
        # Load the data from the 'spectra' dataset
        data = pd.DataFrame(h5_file['spectra'][:])

        # Load wavelengths (if available)
        if 'wavelengths' in h5_file.attrs:
            data.columns = h5_file.attrs['wavelengths']
        elif 'wavelengths' in h5_file:
            data.columns = h5_file['wavelengths'][()]
        else:
            # not found, continue
            pass

        # Load the samples from the 'samples' attribute
        samples = pd.Series(h5_file['spectra'].attrs['samples'])

        # Load the experimental parameters from the 'experimental_parameters' attribute
        exp_params = json.loads(h5_file['spectra'].attrs['experimental_parameters'])

    return data, samples, exp_params, data.columns.values

Fe_comp_dict ={
                0:99.6,
                1:89.8,
                2:79.9,
                3:69.7,
                4:59.9,
                5:50.2,
                6:40.1,
                7:30.1,
                8:20.0,
                9:10.4,
                10:0.1,
    }

Co_comp_dict ={
                
                0:0.0,
                1:10.0,
                2:19.9,
                3:30.2,
                4:40.0,
                5:49.7,
                6:59.9,
                7:69.9,
                8:80.0,
                9:89.6,
                10:99.9,
    }

wdir = r"C:\Users\Federico Checozzi\Documents\Tesis\Datasets"
os.chdir(wdir)

file_path = 'discovery_catalina_20mJ.h5'
#file_path = 'labtrace_avantes_7mJ.h5'
data, samples, exp_params, wavelengths = load_h5_as_df(file_path)
# print(data.shape)
# print(samples.shape) 
print(exp_params)

df = samples.to_frame(name = "sample")
df['sample'] = df['sample'].astype(int)
df['Fe_comp'] = df['sample'].map(Fe_comp_dict)
df['Co_comp'] = df['sample'].map(Co_comp_dict)

df.to_csv(r'C:\Users\Federico Checozzi\Documents\Tesis\Código de prueba\output\comp_FeCo.csv', sep = ';', decimal = ',', index = False)
