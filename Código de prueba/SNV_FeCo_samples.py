# -*- coding: utf-8 -*-
"""
Created on Mon May 26 15:17:13 2025

@author: Federico Checozzi
"""

#Dataset: https://figshare.com/articles/dataset/LIBS_spectra_Fe-Co_certified_sample_set/21984989

import h5py
import pandas as pd
import json
import numpy as np
import os
import time
from skimage.restoration import denoise_wavelet
from pybaselines import Baseline 


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

def normalize_row(row):
    return (row - np.mean(row)) / np.std(row)

wdir = r"C:\Users\Federico Checozzi\Documents\Tesis\Datasets"
os.chdir(wdir)

file_path = 'discovery_catalina_20mJ.h5'
#file_path = 'labtrace_avantes_7mJ.h5'
data, samples, exp_params, wavelengths = load_h5_as_df(file_path)
# print(data.shape)
# print(samples.shape) 
print(exp_params)

start = time.time()
baseline_fitter = Baseline(check_finite=False)

#Corrección de línea de base
df_mwmv = data.apply(lambda row: row - baseline_fitter.mwmv(row)[0], axis = 1, result_type = 'expand')

#Limpieza de ruido con db4
df_wavbayes = df_mwmv.apply(lambda row: denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

#SNV
df_SNV = df_wavbayes.apply(normalize_row, axis = 1) 
end = time.time()
print('Execution time is:')
print(end - start)
#52.261263370513916s

df_SNV.columns = data.columns.astype(str)

df_SNV.to_csv(r'C:\Users\Federico Checozzi\Documents\Tesis\Código de prueba\output\SNVFeCo.csv', sep = ';', decimal = ',', index = False)
#wav = pd.DataFrame(wavelengths)
#wav.to_csv(r'C:\Users\Federico Checozzi\Documents\Tesis\Código de prueba\output\WavelengthFeCo.csv',  sep = ';', decimal = ',', index = False)
