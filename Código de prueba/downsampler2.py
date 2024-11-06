# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 15:36:02 2024

@author: Federico Checozzi
"""

import pandas as pd
import numpy as np
import os
import time
from scipy.signal import decimate

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('SNV1.csv', sep = ';', decimal = ',')

start = time.time()
df_downsampled1 = pd.DataFrame(data = decimate(df,4,axis = 1))
df_downsampled2 = pd.DataFrame(data = decimate(df,5,axis = 1))
df_downsampled3 = pd.DataFrame(data = decimate(df,6,axis = 1))
df_downsampled4 = pd.DataFrame(data = decimate(df,8,axis = 1))
df_downsampled5 = pd.DataFrame(data = decimate(df,10,axis = 1))
df_downsampled6 = pd.DataFrame(data = decimate(df,20,axis = 1))
df_downsampled7 = pd.DataFrame(data = decimate(df,30,axis = 1))
df_downsampled8 = pd.DataFrame(data = decimate(df,39,axis = 1))
end = time.time()
print('Execution time is:')
print(end - start)
#1.2656171321868896s

df_downsampled1.to_csv('SNV1_downsampledby4.csv', sep = ';', decimal = ',', index = False)
df_downsampled2.to_csv('SNV1_downsampledby5.csv', sep = ';', decimal = ',', index = False)
df_downsampled3.to_csv('SNV1_downsampledby6.csv', sep = ';', decimal = ',', index = False)
df_downsampled4.to_csv('SNV1_downsampledby8.csv', sep = ';', decimal = ',', index = False)
df_downsampled5.to_csv('SNV1_downsampledby10.csv', sep = ';', decimal = ',', index = False)
df_downsampled6.to_csv('SNV1_downsampledby20.csv', sep = ';', decimal = ',', index = False)
df_downsampled7.to_csv('SNV1_downsampledby30.csv', sep = ';', decimal = ',', index = False)
df_downsampled8.to_csv('SNV1_downsampledby39.csv', sep = ';', decimal = ',', index = False)