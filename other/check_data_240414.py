'''
2024-4-14
This script is to check the data integrity
'''
import xarray as xr
import numpy as np
import os

pathin = '/home/sun/wd_disk/AerChemMIP/download/mon_cdnc/'
datalist = os.listdir(pathin)

for ff in datalist:
    if ff[0] != '.'  and ff[-2:] == 'nc':
        f0 = xr.open_dataset(pathin + ff)

        print(f'Successfully read {ff}')
        f0['cdnc'].to_netcdf('/home/sun/wd_disk/AerChemMIP/download/mon_cdnc_extract/' + ff)
    else:
        continue