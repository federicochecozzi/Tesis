# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:03:44 2023

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
import os
import time
from skimage.restoration import denoise_wavelet
from pybaselines import Baseline

def normalize_row(row):
    return (row - np.mean(row)) / np.std(row)

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('train_samples.csv', sep = ';', decimal = ',')

baseline_fitter = Baseline(check_finite=False)

#Corrección de línea de base
df_mwmv = df.apply(lambda row: row - baseline_fitter.mwmv(row)[0], axis = 1, result_type = 'expand')

#Limpieza de ruido con db4
df_wavbayes = df_mwmv.apply(lambda row: denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')
df_wavvisu  = df_mwmv.apply(lambda row: denoise_wavelet(row, method='VisuShrink' , mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

#SNV
start = time.time()
df_SNV1 = df_wavbayes.apply(normalize_row, axis = 1) 
end = time.time()
print('Execution time is:')
print(end - start)
#0.25447797775268555s

start = time.time()
df_SNV2 = df_wavvisu.apply(normalize_row, axis = 1) 
end = time.time()
print('Execution time is:')
print(end - start)

df_SNV1.to_csv('SNV1.csv', sep = ';', decimal = ',', index = False)
df_SNV2.to_csv('SNV2.csv', sep = ';', decimal = ',', index = False)
