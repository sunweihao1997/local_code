'''
2024-4-29
This script is to calculate the regional averaged series for power spectra analysis

Here I select three regions:
1. SA: (70-85E, 15-25N)
2. Indochina: (95-110E, 10-20N)
3. EA: (105-120E, 22.5-32.5N)
'''
import xarray as xr
import numpy as np
import os

# ================= File Information =====================

data_path = '/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid_linear/'
out_path  = '/home/sun/data/process/analysis/AerChem/regional_pr_MJJAS/'

mask_file    = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid2x2.nc')

# Region division
region_SA = [15, 25, 70, 85]
region_ID = [10, 20, 95, 110]
region_EA = [22.5, 32.5, 105, 120]

file_list = os.listdir(data_path) ; file_list.sort()

# ========================================================


for ff0 in file_list:
    f0    = xr.open_dataset(data_path + ff0)

    # 1. Select out the MJJAS data
    f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))

    # 2. Regional selection
    f0_MJJAS_SA = f0_MJJAS.sel(lat=slice(region_SA[0], region_SA[1]), lon=slice(region_SA[2], region_SA[3])) ; mask_file_SA = mask_file.sel(latitude=slice(region_SA[0], region_SA[1]), longitude=slice(region_SA[2], region_SA[3]))
    f0_MJJAS_ID = f0_MJJAS.sel(lat=slice(region_ID[0], region_ID[1]), lon=slice(region_ID[2], region_ID[3])) ; mask_file_ID = mask_file.sel(latitude=slice(region_ID[0], region_ID[1]), longitude=slice(region_ID[2], region_ID[3]))
    f0_MJJAS_EA = f0_MJJAS.sel(lat=slice(region_EA[0], region_EA[1]), lon=slice(region_EA[2], region_EA[3])) ; mask_file_EA = mask_file.sel(latitude=slice(region_EA[0], region_EA[1]), longitude=slice(region_EA[2], region_EA[3]))

    # 3. calculate the series for the regional precipitation
    f0_MJJAS_SA['pr'].data[:, mask_file_SA['lsm'].data[0] < 0.05] = np.nan
    prect_SA    = np.nanmean(np.nanmean(f0_MJJAS_SA['pr'].data, axis=1), axis=1)
    #print(np.average(prect_SA)*86400)

    f0_MJJAS_ID['pr'].data[:, mask_file_ID['lsm'].data[0] < 0.05] = np.nan
    prect_ID    = np.nanmean(np.nanmean(f0_MJJAS_ID['pr'].data, axis=1), axis=1)

    f0_MJJAS_EA['pr'].data[:, mask_file_EA['lsm'].data[0] < 0.05] = np.nan
    prect_EA    = np.nanmean(np.nanmean(f0_MJJAS_EA['pr'].data, axis=1), axis=1)

    # Write three regional series to ncfile
    time        = f0_MJJAS.time.data

    ncfile  =  xr.Dataset(
        {
            "prect_SA":     (["time"], (prect_SA*86400)),
            "prect_ID":     (["time"], (prect_ID*86400)),
            "prect_EA":     (["time"], (prect_EA*86400)),     
        },
        coords={
            "time":         (["time"], time),
        },
        )

    ncfile.attrs['description'] = 'Created on 2024-4-29. This file save the regional precipitation series, while the ocean data have been masked. The script is cal_AerChemMIP_power_spetra_prework_regional_series_precipitation_240429.py, in which the regional devision was noted, for Indian, Indochina and East Asia'

    ncfile['prect_SA'].attrs['units'] = 'mm day**-1' ; ncfile['prect_SA'].attrs['description'] = 'Precipitation over South Asia'
    ncfile['prect_ID'].attrs['units'] = 'mm day**-1' ; ncfile['prect_ID'].attrs['description'] = 'Precipitation over Indochina'
    ncfile['prect_EA'].attrs['units'] = 'mm day**-1' ; ncfile['prect_EA'].attrs['description'] = 'Precipitation over East Asia'

    ncfile.to_netcdf(out_path + ff0)

    print(f'Successfully calculated the regional precipitation for {ff0}')