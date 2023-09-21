# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 15:05:28 2023

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
df_downsampled = pd.DataFrame(data = decimate(df,3,axis = 1))
end = time.time()
print('Execution time is:')
print(end - start)
#0.25447797775268555s

df_downsampled.to_csv('SNV1_downsampled.csv', sep = ';', decimal = ',', index = False)