# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:30:41 2023

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
import os
import time
from scipy.signal import savgol_filter

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('train_samples.csv', sep = ';', decimal = ',')

# Parámetros iniciales razonables para empezar: https://nirpyresearch.com/choosing-optimal-parameters-savitzky-golay-smoothing-filter/
w = 5
p = 2

start = time.time()
df_savgol1 = df.apply(lambda row: savgol_filter(row, w, polyorder = p, deriv=0), axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#0.21021509170532227s

start = time.time()
df_savgol2 = df.apply(lambda row: savgol_filter(row, 2*w+1, polyorder = p, deriv=0), axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#0.19088220596313477s

start = time.time()
df_savgol3 = df.apply(lambda row: savgol_filter(row, 4*w+1, polyorder = 3*p, deriv=0), axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#0.26174235343933105s

df_savgol1.to_csv('savgol1.csv', sep = ';', decimal = ',', index = False)
df_savgol2.to_csv('savgol2.csv', sep = ';', decimal = ',', index = False)
df_savgol3.to_csv('savgol3.csv', sep = ';', decimal = ',', index = False)