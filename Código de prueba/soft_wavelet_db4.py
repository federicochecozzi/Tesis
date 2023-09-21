# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:18:12 2023

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
import os
import time
from skimage.restoration import denoise_wavelet

#import pywt 
#w = pywt.Wavelet('sym7')
#pywt.dwt_max_level(data_len=40002, filter_len=w.dec_len)

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('train_samples.csv', sep = ';', decimal = ',')

start = time.time()
df_wav3 = df.apply(lambda row: denoise_wavelet(row, method='BayesShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#0.6037743091583252s

start = time.time()
df_wav4 = df.apply(lambda row: denoise_wavelet(row, method='VisuShrink', mode='soft', wavelet_levels=None, wavelet='db4'), axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#0.5653069019317627s

df_wav3.to_csv('wav3.csv', sep = ';', decimal = ',', index = False)
df_wav4.to_csv('wav4.csv', sep = ';', decimal = ',', index = False)
