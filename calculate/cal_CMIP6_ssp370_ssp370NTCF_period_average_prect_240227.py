'''
2024-2-27
This script is to calculate the historical period between 1985-2014, representing the present-day stage
'''
import xarray as xr
import numpy as np
import os

src_path = '/Volumes/Untitled/AerChemMIP/post_process_samegrids/'

models_label = ['UKESM1-0-LL', 'NorESM2-LM', 'MPI-ESM-1-2-HAM', 'IPSL-CM5A2', 'EC-Earth3-AerChem', 'CNRM-ESM', 'CESM2-WACCM', 'BCC-ESM1']

files_all = os.listdir(src_path)

# screen out the target models and historical experiments
historical_files = []
for ffff in files_all:
    if 'historical' in ffff:
        historical_files.append(ffff)

#!!! Notice that the IPSL starts from 1950 !!!

# Calculate the muti-models average
hist_pr_avg  =  np.zeros((360, 121, 241))
model_numbers=  len(historical_files)

for ff in historical_files:
    f0 = xr.open_dataset(src_path + ff)

    f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(1985, 2014, 30)))

    #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
    #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
    hist_pr_avg += f0_select['pr'].data * 86400 / model_numbers

# Write to ncfile
ncfile  =  xr.Dataset(
    {
        'pr': (["time", "lat", "lon"], hist_pr_avg),
    },
    coords={
        "time": (["time"], f0_select.time.data),
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
    },
    )

ncfile['pr'].attrs['units'] = 'mm day-1'

ncfile.attrs['description'] = 'Created on 2024-2-27. This file save the CMIP6 historical monthly precipitation data. The result is the multi-model average value'
ncfile.attrs['Mother'] = 'local-code: cal_CMIP6_historical_period_average_prect_240227.py'
#
out_path = '/mnt/d/samssd/precipitation/CESM/ensemble_JJAS/'
ncfile.to_netcdf(src_path + 'CMIP6_model_historical_monthly_precipitation_1985-2014.nc')