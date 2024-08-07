'''
2024-7-3
This script is to deal with hourly data and convert to daily mean

This script is to test the groupby method
'''
import xarray as xr
import numpy as np

f0 = xr.open_dataset("/home/sun/mydown/ERA5/1940-2023_hourly_single_OLR-SW-ST/skin_temperature_1982.nc")

f1 = f0.resample(time='5D').mean()
print(f1)