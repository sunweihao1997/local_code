'''
2024-4-28
This script is to use the cal_AerChemMIP_band_pass_calculation_240428 to calculate 8-70 days band-pass filter for precipitation
'''
import xarray as xr
import numpy as np
import sys
import os

sys.path.append("/home/sun/local_code/calculate/")
from cal_AerChemMIP_band_pass_calculation_240428 import band_pass_calculation

# File Information
data_path = '/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid_linear/'

out_path  = '/home/sun/data/process/model/aerchemmip-postprocess/day_prect_20_70/' # Path saves the filtered data

varname   = 'pr'

# Start calculation

file_list = os.listdir(data_path)
for ff in file_list:
    print(f'Now it is dealing with the file {ff}')
    f1    = xr.open_dataset(data_path + ff)

    time  = f1.time.data ; lat   = f1.lat.data ; lon   = f1.lon.data
    # Inilitize the array
    filter_pr = np.zeros((len(time), len(lat), len(lon)))

    # Calculation
    for i in range(len(lat)):
        for j in range(len(lon)):
            filter_pr[:, i, j] = band_pass_calculation(f1['pr'].data[:, i, j], fs=1, low_frq=70, high_frq=20, order=5,)

    # Write to ncfile
    ncfile  =  xr.Dataset(
        {
            "filter_pr":     (["time", "lat", "lon"], filter_pr),     
        },
        coords={
            "lat":  (["lat"],  f1.lat.data),
            "lon":  (["lon"],  f1.lon.data),
            "time": (["time"], f1.time.data)
        },
        )

    ncfile.attrs['description'] = 'Created on 2024-4-28. This file save the 20-70 band-pass precipitation, generated by cal_AerChemMIP_band_pass_prect_240428.py.'


    ncfile.to_netcdf(out_path + ff)


# ============================== test ====================================
# test1: does the filtered data has the same length Answer: yes

#ftest = xr.open_dataset(data_path + file_list[1])
#pr_test= ftest['pr'].data ; print(pr_test.shape)
#
#pr_test_filter = band_pass_calculation(pr_test[:, 50, 50], fs=1, low_frq=70, high_frq=8, order=5,)
#print(pr_test_filter.shape)