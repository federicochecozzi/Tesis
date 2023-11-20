# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 11:13:16 2023

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
import os
from skimage.restoration import denoise_wavelet
from pybaselines import Baseline
from scipy.signal import find_peaks
from math import pi

def simulate_spectre(model,wavelengths,peak_locations,**kwargs):
    locations = wavelengths[peak_locations]#[wavelengths[index] for index in peak_locations]
    heights = kwargs['peak_heights']#np.interp(kwargs['peak_heights'],list(range(len(peak_locations))),wavelengths)
    FWHM = np.interp(kwargs["right_ips"], list(range(len(wavelengths))), wavelengths) - np.interp(kwargs["left_ips"], list(range(len(wavelengths))), wavelengths)#kwargs['widths']
    spectre = np.zeros(len(wavelengths))
    for i in range(len(peak_locations)):
        if (model == 'Guo2017'):
        #Guo 2017
            spectre += heights[i] * FWHM[i]**2/(4*(wavelengths-locations[i])**2 + FWHM[i]**2)
        elif(model == 'Yang2018'):
        #Yang 2018
            spectre += heights[i] * 2 / pi * FWHM[i]**2/(4*(wavelengths-locations[i])**2 + FWHM[i]**2)
        else:
        #Zhang 2013
            spectre += heights[i] * FWHM[i]**2/((wavelengths-locations[i])**2 + FWHM[i]**2)

    #spectre = heights[0] * FWHM[0]**2/((wavelengths-locations[0])**2 + FWHM[0]**2)
    return spectre

def analyze_and_simulate_spectre(spectre, wavelengths,model):
    peaks = find_peaks(spectre, height = 750, width = 1)
    return simulate_spectre("default",np.array(wavelengths),peaks[0],**peaks[1])  

def estimate_sigma(spectre):
    #row['sigma'] = np.std(spectre[0:2500])
    return np.std(spectre[0:2500])

def add_noise(row): 
    return row[0:40002] + np.random.normal(0,row['sigma'],40002)

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('train_samples.csv', sep = ';', decimal = ',')

baseline_fitter = Baseline(check_finite=False)

df_mwmv = df.apply(lambda row: row - baseline_fitter.mwmv(row)[0], axis = 1, result_type = 'expand')

df_wavvisu  = df_mwmv.apply(lambda row: denoise_wavelet(row, method='VisuShrink' , mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_mwmv.columns = df.columns
df_wavvisu.columns = df.columns

wavelengths = [float(wavelength) for wavelength in df.columns]

df_simulated = df_wavvisu.apply(lambda row: analyze_and_simulate_spectre(row, wavelengths,"Guo2017"), axis = 1, result_type = 'expand')

df_simulated.columns = df.columns

df_sigma = df_wavvisu.apply(estimate_sigma, axis = 1)

df_simulated_noisy = df_simulated.assign(sigma = df_sigma).apply(add_noise, axis = 1, result_type = 'expand')

df_simulated_noisy.columns = df.columns

df_simulated.to_csv('simulated.csv', sep = ';', decimal = ',', index = False)
df_simulated_noisy.to_csv('simulated_noisy.csv', sep = ';', decimal = ',', index = False)
