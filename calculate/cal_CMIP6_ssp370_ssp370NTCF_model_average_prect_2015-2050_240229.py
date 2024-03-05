'''
2024-2-27
This script is to calculate the SSP370 and SSP370NTCF period between 2031-2050, representing the future scenarios
'''
import xarray as xr
import numpy as np
import os

#
src_path = '/data/AerChemMIP/LLNL_download/postprocess_samegrids/'
out_path = '/data/AerChemMIP/LLNL_download/model_average/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'MIROC6']
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G',  'MIROC6', 'CNRM-ESM']
#models_label = ['EC-Earth3-AerChem', 'GISS-E2-1-G',]
#models_label = ['GISS-E2-1-G',]

files_all = os.listdir(src_path)

# screen out the target models and historical experiments
ssp370_files      = []
ssp370NTCF_files  = []

for ffff in files_all:
    name_list = ffff.split("_")
    modelname = name_list[0]
    if 'SSP370' in ffff and 'NTCF' not in ffff and 'CMIP6' not in ffff and modelname in models_label:
        ssp370_files.append(ffff)
    elif 'SSP370NTCF' in ffff and 'CMIP6' not in ffff and modelname in models_label:
        ssp370NTCF_files.append(ffff)

#!!! Notice that the IPSL starts from 1950 !!!

# Calculate the muti-models average
ssp370_pr_avg      =  np.zeros((36 * 12, 121, 241)) # 2015-2050, 36year
ssp370ntcf_pr_avg  =  np.zeros((36 * 12, 121, 241)) # 2015-2050, 36year

model_numbers_ssp370      =  len(ssp370_files) ; print(model_numbers_ssp370)
model_numbers_ssp370NTCF  =  len(ssp370NTCF_files)  ; print(model_numbers_ssp370NTCF)

for ff in ssp370_files:
    f0 = xr.open_dataset(src_path + ff)

    f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2015, 2050, 36)))
    #print(f0_select)


    #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
    #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
    ssp370_pr_avg += (f0_select['pr'].data * 86400 / model_numbers_ssp370)

for ff in ssp370NTCF_files:
    f0 = xr.open_dataset(src_path + ff)

    f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2015, 2050, 36)))

    #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
    #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
    ssp370ntcf_pr_avg += (f0_select['pr'].data * 86400 / model_numbers_ssp370NTCF)


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

ncfile1.attrs['description'] = 'Created on 2024-2-29. This file save the CMIP6 SSP370 monthly precipitation data. The result is the multi-model average value'
ncfile1.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_model_average_prect_2015-2050_240229.py'
#

ncfile1.to_netcdf(out_path + 'CMIP6_model_SSP370_monthly_precipitation_2015-2050.nc')


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

ncfile2.attrs['description'] = 'Created on 2024-2-29. This file save the CMIP6 SSP370NTCF monthly precipitation data. The result is the multi-model average value'
ncfile2.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_model_average_prect_2015-2050_240229.py'
#

ncfile2.to_netcdf(out_path + 'CMIP6_model_SSP370NTCF_monthly_precipitation_2015-2050.nc')
#print(ncfile2)
ncfile1_May = ncfile1.sel(time=ncfile1.time.dt.month.isin([5, ])) ; ncfile2_May = ncfile2.sel(time=ncfile2.time.dt.month.isin([5, ]))
ncfile1_Jun = ncfile1.sel(time=ncfile1.time.dt.month.isin([6, ])) ; ncfile2_Jun = ncfile2.sel(time=ncfile2.time.dt.month.isin([6, ]))

ncfile  =  xr.Dataset(
    {
        "pr_May_SSP370":     (["time1", "lat", "lon"], ncfile1_May['pr'].data),
        "pr_May_SSP370NTCF": (["time1", "lat", "lon"], ncfile2_May['pr'].data),
        "pr_Jun_SSP370":     (["time2", "lat", "lon"], ncfile1_Jun['pr'].data),
        "pr_Jun_SSP370NTCF": (["time2", "lat", "lon"], ncfile2_Jun['pr'].data),
    },
    coords={
        "time1":(["time1"],ncfile1_May.time.data),
        "time2":(["time2"],ncfile1_Jun.time.data),
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
    },
    )

#ncfile['pr'].attrs['units'] = 'mm day-1'

ncfile.attrs['description'] = 'Created on 2024-2-29. This file save the CMIP6 SSP370 and SSP370NTCF May and June monthly precipitation data, for the period 2015-2050'
ncfile.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_model_average_prect_2015-2050_240229.py'
#

ncfile.to_netcdf(out_path + 'CMIP6_model_SSP370_SSP370NTCF_month56_precipitation_2015-2050.nc')