# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 11:07:07 2025

@author: Federico Checozzi
"""

#Dataset: https://figshare.com/articles/dataset/LIBS_spectra_Fe-Co_certified_sample_set/21984989
#https://docs.h5py.org/en/stable/high/attr.html
#https://docs.h5py.org/en/stable/strings.html

import h5py
import pandas as pd
#import json
import numpy as np
import os
import time
from skimage.restoration import denoise_wavelet
from pybaselines import Baseline 
from scipy.signal import decimate

wdir = r"C:\Users\Federico Checozzi\Documents\Tesis\Datasets"
file_path = 'discovery_catalina_20mJ.h5'
downsampling_factor = 8
output_file = 'catalina_processed_and_downsampled_with_target.h5'

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
        data = h5_file['spectra'][:]

        # Load wavelengths (if available)
        if 'wavelengths' in h5_file.attrs:
            wavelengths = h5_file.attrs['wavelengths']
        elif 'wavelengths' in h5_file:
            wavelengths = h5_file['wavelengths'][()]
        else:
            # not found, continue
            pass

        # Load the samples from the 'samples' attribute
        samples = pd.Series(h5_file['spectra'].attrs['samples'])

        # Load the experimental parameters from the 'experimental_parameters' attribute
        exp_params = h5_file['spectra'].attrs['experimental_parameters']

    return data, samples, exp_params, wavelengths

baseline_fitter = Baseline(check_finite=False)

def normalize(row):
    return (row - np.mean(row)) / np.std(row)

def process_row(row):
    row = row - baseline_fitter.mwmv(row)[0]
    row = denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4')
    row = normalize(row)
    return row

os.chdir(wdir)

data, samples, exp_params, wavelengths = load_h5_as_df(file_path)
# print(data.shape)
# print(samples.shape) 
print(exp_params)

start = time.time()

data_processed = np.apply_along_axis(process_row, 1, data)

data_downsampled = decimate(data_processed,downsampling_factor,axis = 1)

wavelengths_downsampled = decimate(wavelengths,downsampling_factor)

end = time.time()
print('Execution time is:')
print(end - start)
#55.8403480052948s

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

samples = samples.astype(int)

frame = {
            'Samples': samples,
            'Fe_comp': samples.map(Fe_comp_dict),
            'Co_comp': samples.map(Co_comp_dict),
        }

target = pd.DataFrame(frame)

#Escritura en un nuevo archivo
FeCoFile = h5py.File(output_file,'w')

spectra_dst = FeCoFile.create_dataset('spectra', data = data_downsampled)
FeCoFile.create_dataset('target', data = target)
#spectra_dst.attrs['samples'] = samples
spectra_dst.attrs['experimental_parameters'] = exp_params
FeCoFile.create_dataset('wavelengths', data = wavelengths_downsampled)

FeCoFile.close()