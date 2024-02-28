'''
2024-2-27
This script is to calculate the SSP370 and SSP370NTCF period between 2031-2050, representing the future scenarios
'''
import xarray as xr
import numpy as np
import os

os.system('rm -rf /Volumes/Untitled/AerChemMIP/post_process_samegrids/CMIP6_model_SSP370_monthly_precipitation_1985-2014.nc')
os.system('rm -rf /Volumes/Untitled/AerChemMIP/post_process_samegrids/CMIP6_model_SSP370NTCF_monthly_precipitation_1985-2014.nc')
os.system('rm -rf /Volumes/Untitled/AerChemMIP/post_process_samegrids/CMIP6_model_SSP370-SSP370NTCF_monthly_precipitation_1985-2014.nc')

src_path = '/Volumes/Untitled/AerChemMIP/post_process_samegrids/'

models_label = ['UKESM1-0-LL', 'NorESM2-LM', 'MPI-ESM-1-2-HAM', 'IPSL-CM5A2', 'EC-Earth3-AerChem', 'CNRM-ESM', 'CESM2-WACCM', 'BCC-ESM1']

files_all = os.listdir(src_path)

# screen out the target models and historical experiments
ssp370_files      = []
ssp370NTCF_files  = []

for ffff in files_all:
    if 'SSP370' in ffff and 'NTCF' not in ffff:
        ssp370_files.append(ffff)
    elif 'SSP370NTCF' in ffff:
        ssp370NTCF_files.append(ffff)

#!!! Notice that the IPSL starts from 1950 !!!

# Calculate the muti-models average
ssp370_pr_avg      =  np.zeros((240, 121, 241))
ssp370ntcf_pr_avg  =  np.zeros((240, 121, 241))

model_numbers_ssp370      =  len(ssp370_files)
model_numbers_ssp370NTCF  =  len(ssp370NTCF_files)

for ff in ssp370_files:
    f0 = xr.open_dataset(src_path + ff)

    f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2031, 2050, 20)))

    #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
    #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
    ssp370_pr_avg += f0_select['pr'].data * 86400 / model_numbers_ssp370

for ff in ssp370NTCF_files:
    f0 = xr.open_dataset(src_path + ff)

    f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2031, 2050, 20)))

    #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
    #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
    ssp370ntcf_pr_avg += f0_select['pr'].data * 86400 / model_numbers_ssp370NTCF


# Write to ncfile
ncfile1  =  xr.Dataset(
    {
        'pr': (["time", "lat", "lon"], ssp370_pr_avg),
    },
    coords={
        "time": (["time"], f0_select.time.data),
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
    },
    )

ncfile1['pr'].attrs['units'] = 'mm day-1'

ncfile1.attrs['description'] = 'Created on 2024-2-27. This file save the CMIP6 SSP370 monthly precipitation data. The result is the multi-model average value'
ncfile1.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_period_average_prect_240227.py'
#

ncfile1.to_netcdf(src_path + 'CMIP6_model_SSP370_monthly_precipitation_1985-2014.nc')


ncfile2  =  xr.Dataset(
    {
        'pr': (["time", "lat", "lon"], ssp370ntcf_pr_avg),
    },
    coords={
        "time": (["time"], f0_select.time.data),
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
    },
    )

ncfile2['pr'].attrs['units'] = 'mm day-1'

ncfile2.attrs['description'] = 'Created on 2024-2-27. This file save the CMIP6 SSP370NTCF monthly precipitation data. The result is the multi-model average value'
ncfile2.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_period_average_prect_240227.py'
#

ncfile2.to_netcdf(src_path + 'CMIP6_model_SSP370NTCF_monthly_precipitation_1985-2014.nc')

ncfile1_May = ncfile1.sel(time=ncfile1.time.dt.month.isin([5, ])) ; ncfile2_May = ncfile2.sel(time=ncfile2.time.dt.month.isin([5, ]))
ncfile1_Jun = ncfile1.sel(time=ncfile1.time.dt.month.isin([6, ])) ; ncfile2_Jun = ncfile2.sel(time=ncfile2.time.dt.month.isin([6, ]))

ncfile  =  xr.Dataset(
    {
        'pr_May': (["lat", "lon"], np.average(ncfile1_May['pr'].data, axis=0) - np.average(ncfile2_May['pr'].data, axis=0)),
    },
    coords={
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
    },
    )

#ncfile['pr'].attrs['units'] = 'mm day-1'

ncfile.attrs['description'] = 'Created on 2024-2-27. This file save the CMIP6 SSP370 subtract SSP370NTCF monthly precipitation data. The result is the multi-model average value'
ncfile.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_period_average_prect_240227.py'
#

ncfile.to_netcdf(src_path + 'CMIP6_model_SSP370-SSP370NTCF_monthly_precipitation_1985-2014.nc')