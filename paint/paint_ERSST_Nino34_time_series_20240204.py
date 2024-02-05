'''
2024-2-4
This script is to calculate the Nino34 index using ERSST data
'''
import xarray as xr
import numpy as np

ersst = xr.open_dataset('/home/sun/data/download_data/ERSST/sst.mnmean.nc')

# time selection is 1980-2014
ersst_time = ersst.sel(time=ersst.time.dt.year.isin(np.linspace(1980, 2014, 35)))

ersst_time_nino34 = ersst_time.sel(lat=slice(5, -5), lon=slice(190, 240))

#print(ersst_time_nino34)

Nino34 = np.array([])

for yy in range(420):
    Nino34 = np.append(Nino34, np.nanmean(ersst_time_nino34['sst'].data[yy]))

print(Nino34)