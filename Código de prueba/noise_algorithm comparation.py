# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:34:14 2023

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import os
from skimage.restoration import denoise_wavelet
import seaborn as sns
import pingouin as pg

def calculate_MSE(df1,df2):
    df_merged = pd.concat([df1, df2], axis = 1)
    return df_merged.apply(lambda row: mean_squared_error(row[0:40002],row[40002:]),axis = 1)

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df_simulated = pd.read_csv('simulated.csv', sep = ';', decimal = ',')
df_simulated_noisy = pd.read_csv('simulated_noisy.csv', sep = ';', decimal = ',')

df_wavbayes = df_simulated_noisy.apply(lambda row: denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_wavvisu  = df_simulated_noisy.apply(lambda row: denoise_wavelet(row, method='VisuShrink' , mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')

df_wavbayes.columns = df_simulated_noisy.columns
df_wavvisu.columns = df_simulated_noisy.columns

wavelengths = [float(wavelength) for wavelength in df_simulated_noisy.columns]

MSE1 = calculate_MSE(df_simulated, df_simulated_noisy)
MSE2 = calculate_MSE(df_simulated, df_wavbayes)
MSE3 = calculate_MSE(df_simulated, df_wavvisu)

df_MSE = data = pd.concat([MSE1,MSE2,MSE3], axis = 1).rename(columns = {0:"Señal ruidosa",1:"BayesShrink",2:"VisuShrink"})

sns.histplot(df_MSE)

friedman = pg.friedman(df_MSE)

test1 = pg.wilcoxon(MSE1,MSE2)
test2 = pg.wilcoxon(MSE1,MSE3)
test3 = pg.wilcoxon(MSE2,MSE3)

print(np.mean(MSE1),np.mean(MSE2),np.mean(MSE3))
