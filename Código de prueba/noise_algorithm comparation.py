# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:34:14 2023

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
import os
from skimage.restoration import denoise_wavelet

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df_simulated = pd.read_csv('simulated.csv', sep = ';', decimal = ',')
df_simulated_noisy = pd.read_csv('simulated_noisy.csv', sep = ';', decimal = ',')

df_wavbayes = df_simulated_noisy.apply(lambda row: denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_wavvisu  = df_simulated_noisy.apply(lambda row: denoise_wavelet(row, method='VisuShrink' , mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_wavbayes.columns = df_simulated_noisy.columns
df_wavvisu.columns = df_simulated_noisy.columns

wavelengths = [float(wavelength) for wavelength in df_simulated_noisy.columns]
