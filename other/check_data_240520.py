'''
2024-5-20
This script is to check data
'''
import xarray as xr

import os

path0 = "/data/AerChemMIP/process/post-process/ua/"

list0 = os.listdir(path0)
list1 = []

for ff in list0:
    if ff[0] != '.' and ff[-2:] == 'nc':
        list1.append(ff)

for ff in list1:
    print(ff)
    f0 = xr.open_dataset(path0 + ff)