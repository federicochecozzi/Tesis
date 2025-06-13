# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 15:00:53 2025

@author: Federico Checozzi
"""

#Dataset: https://figshare.com/articles/dataset/LIBS_spectra_Fe-Co_certified_sample_set/21984989
#https://docs.h5py.org/en/stable/high/attr.html
#https://docs.h5py.org/en/stable/strings.html

import h5py
#import pandas as pd
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
output_file = 'catalina_processed_and_downsampled.h5'

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
        samples = h5_file['spectra'].attrs['samples']

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

#Escritura en un nuevo archivo
FeCoFile = h5py.File(output_file,'w')

spectra_dst = FeCoFile.create_dataset('spectra', data = data_downsampled)
spectra_dst.attrs['samples'] = samples
spectra_dst.attrs['experimental_parameters'] = exp_params
FeCoFile.create_dataset('wavelengths', data = wavelengths_downsampled)

FeCoFile.close()