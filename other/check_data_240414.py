'''
2024-4-14
This script is to check the data integrity
'''
import xarray as xr
import numpy as np
import os

pathin = '/home/sun/data/download_data/AerChemMIP/tasmin/'
datalist = os.listdir(pathin)

for ff in datalist:
    if ff[0] != '.'  and ff[-2:] == 'nc':
        f0 = xr.open_dataset(pathin + ff)

        print(f'Successfully read {ff}')
    else:
        continue