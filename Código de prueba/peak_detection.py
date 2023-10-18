# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 15:05:41 2023

@author: Federico Checozzi
"""

#https://scikit-image.org/docs/stable/api/skimage.restoration.html#skimage.restoration.estimate_sigma

import pandas as pd
import numpy as np
import os
from pybaselines import Baseline
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks, find_peaks_cwt
from skimage.restoration import denoise_wavelet

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('train_samples.csv', sep = ';', decimal = ',')

baseline_fitter = Baseline(check_finite=False)

df_mwmv = df.apply(lambda row: row - baseline_fitter.mwmv(row)[0], axis = 1, result_type = 'expand')

df_wavbayes = df_mwmv.apply(lambda row: denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_wavvisu  = df_mwmv.apply(lambda row: denoise_wavelet(row, method='VisuShrink' , mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_mwmv.columns = df.columns
df_wavbayes.columns = df.columns
df_wavvisu.columns = df.columns

wavelengths = [float(wavelength) for wavelength in df.columns]

sns.lineplot(x = wavelengths, y = df_mwmv.loc[0])
sns.lineplot(x = wavelengths[30700:31000], y = df_mwmv.loc[0][30700:31000])

#peaks = find_peaks_cwt(df_mwmv.loc[0][30000:35000],np.arange(10,500))
#peaks = find_peaks(df_mwmv.loc[0][30000:35000], height = 250)
#is_peak = np.zeros((5000,))
#is_peak[peaks] = 1
#sns.lineplot(x = wavelengths[30000:35000], y = df_mwmv.loc[0][30000:35000], hue = is_peak)
peaks = find_peaks(df_mwmv.loc[0][30700:31000], height = 400, width = 1)
is_peak = np.zeros((300,))
is_peak[peaks[0]] = 1
ax = sns.lineplot(x = wavelengths[30700:31000], y = df_mwmv.loc[0][30700:31000])
sns.scatterplot(x = [wavelengths[30700 + index] for index in peaks[0]],y = df_mwmv.loc[0].iloc[30700 + peaks[0]],color = 'orange',ax = ax)
ax.hlines(y=peaks[1]["width_heights"], xmin= np.interp(peaks[1]["left_ips"], list(range(0,300)), wavelengths[30700:31000]),
           xmax=np.interp(peaks[1]["right_ips"], list(range(0,300)), wavelengths[30700:31000]), color = "C1")

peaks = find_peaks(df_wavbayes.loc[0][30700:31000], height = 400, width = 1)
is_peak = np.zeros((300,))
is_peak[peaks[0]] = 1
ax = sns.lineplot(x = wavelengths[30700:31000], y = df_wavbayes.loc[0][30700:31000])
sns.scatterplot(x = [wavelengths[30700 + index] for index in peaks[0]],y = df_wavbayes.loc[0].iloc[30700 + peaks[0]],color = 'orange',ax = ax)
ax.hlines(y=peaks[1]["width_heights"], xmin= np.interp(peaks[1]["left_ips"], list(range(0,300)), wavelengths[30700:31000]),
           xmax=np.interp(peaks[1]["right_ips"], list(range(0,300)), wavelengths[30700:31000]), color = "C1")

peaks = find_peaks(df_wavvisu.loc[0][30700:31000], height = 400, width = 1)
is_peak = np.zeros((300,))
is_peak[peaks[0]] = 1
ax = sns.lineplot(x = wavelengths[30700:31000], y = df_wavvisu.loc[0][30700:31000])
sns.scatterplot(x = [wavelengths[30700 + index] for index in peaks[0]],y = df_wavvisu.loc[0].iloc[30700 + peaks[0]],color = 'orange',ax = ax)
ax.hlines(y=peaks[1]["width_heights"], xmin= np.interp(peaks[1]["left_ips"], list(range(0,300)), wavelengths[30700:31000]),
           xmax=np.interp(peaks[1]["right_ips"], list(range(0,300)), wavelengths[30700:31000]), color = "C1")
#ax.hlines(y=peaks[1]["width_heights"], xmin=(peaks[1]["left_ips"] + 30700) * (max(wavelengths) - min(wavelengths)) / 40002,
#           xmax=(peaks[1]["right_ips"] + 30700) * (max(wavelengths) - min(wavelengths)) / 40002, color = "C1")