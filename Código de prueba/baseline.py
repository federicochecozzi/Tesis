# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:06:50 2023

@author: Federico Checozzi
"""

#https://scikit-image.org/docs/stable/api/skimage.restoration.html#skimage.restoration.estimate_sigma

import pandas as pd
import numpy as np
import os
import time
from pybaselines import Baseline

wdir = r"C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output"
os.chdir(wdir)

df = pd.read_csv('train_samples.csv', sep = ';', decimal = ',')

baseline_fitter = Baseline(check_finite=False)

#https://stackoverflow.com/questions/23690284/pandas-apply-function-that-returns-multiple-values-to-rows-in-pandas-dataframe

start = time.time()
#cambiar el result_type reduce el tiempo de procesamiento pero no preserva los nombres de variables
df_imodpoly = df.apply(lambda row: baseline_fitter.imodpoly(row, poly_order = 10)[0], axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#default: 
#1.47953462600708s
#poly_order = 10:
#3.3308043479919434s

start = time.time()
#cambiar el result_type reduce el tiempo de procesamiento pero no preserva los nombres de variables
df_goldindec = df.apply(lambda row: baseline_fitter.goldindec(row, poly_order = 10)[0], axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#default:
#294.7231206893921s
#poly_order = 10:
#341.97199535369873s

start = time.time()
#cambiar el result_type reduce el tiempo de procesamiento pero no preserva los nombres de variables
df_mwmv = df.apply(lambda row: baseline_fitter.mwmv(row)[0], axis = 1, result_type = 'expand')
end = time.time()
print('Execution time is:')
print(end - start)
#default
#28.814282655715942s

df_imodpoly.to_csv('df_imodpoly.csv', sep = ';', decimal = ',', index = False)
df_goldindec.to_csv('df_goldindec.csv', sep = ';', decimal = ',', index = False)
df_mwmv.to_csv('df_mwmv.csv', sep = ';', decimal = ',', index = False)