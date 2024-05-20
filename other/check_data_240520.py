'''
2024-5-20
This script is to check data
'''
import xarray as xr

import os

path0 = "/Volumes/Untitled/AerChemMIP/process/post-process/ua/"

list0 = os.listdir(path0)

for ff in list0:
    print(ff)
    f0 = xr.open_dataset(path0 + ff)