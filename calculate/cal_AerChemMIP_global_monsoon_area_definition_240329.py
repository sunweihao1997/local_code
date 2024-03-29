'''
2024-3-29
This script is to calculate the area of the global monsoon under SSP370 and SSP370lowNTCF experiment

The reference:
https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1002/jgrd.50258
difference between MJJAS and NDJFM
'''
import xarray as xr
import numpy as np

data_path = '/data/AerChemMIP/LLNL_download/model_average/'
data_name = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_precipitation_2015-2050_new.nc'

f0        = xr.open_dataset(data_path + data_name)
f0_20year = f0.sel(time=f0.time.dt.year.isin(np.linspace(2031, 2050, 20)))

# Select the MJJAS and NDJFM respectively
f0_winter = f0_20year.sel(time=f0_20year.time.dt.month.isin([11, 12, 1, 2, 3]))
f0_summer = f0_20year.sel(time=f0_20year.time.dt.month.isin([5, 6, 7, 8, 9]))

# coordinate information
lat       = f0.lat.data
lon       = f0.lon.data

def cal_global_monsoon_area(file_win, file_sum, tag, threshold):
    '''
        function for calculating the area of the global monsoon area
        the tag means experiments label
    '''
    # Claim the array for the result
    area_array = np.zeros((len(lat), len(lon)))

    winter_avg = area_array.copy()
    summer_avg = area_array.copy()

    # calculate average between 2031-2050
    for yyyy in np.linspace(2031, 2050, 20):
        file_win_1year = file_win.sel(time=file_win.time.dt.year.isin([yyyy]))
        file_sum_1year = file_sum.sel(time=file_sum.time.dt.year.isin([yyyy]))

        if len(file_win_1year.time.data) != 5:
            print(f'It is year {yyyy}, the length of this year is {len(file0_1year.time.data)}')

        winter_avg += (np.average(file_win_1year['pr' + tag].data, axis=0) / 20)
        summer_avg += (np.average(file_sum_1year['pr' + tag].data, axis=0) / 20)

    for i in range(len(lat)):
        for j in range(len(lon)):
            area_array[i, j] = cal_global_monsoon_justify(summer_avg[i, j], winter_avg[i, j], threshold)

    return area_array

def cal_global_monsoon_justify(summer, winter, threshold):
    '''
    The input should be 1-D array
    '''
    range0 = abs(summer - winter)

    if range0 > 2.25:
        return 1
    else:
        return 0

#print(f0_summer)

hist_area = cal_global_monsoon_area(f0_winter, f0_summer, '_hist', 2.)
ssp_area  = cal_global_monsoon_area(f0_winter, f0_summer, '_ssp', 2.)
ntcf_area = cal_global_monsoon_area(f0_winter, f0_summer, '_ntcf', 2.)
diff_area = np.zeros((121, 241))


for i in range(121):
    for j in range(241):
        if ntcf_area[i, j] == 1 and ssp_area[i, j] != 1:
            diff_area[i, j] = 1


ncfile  =  xr.Dataset(
        {
            "hist_area":     (["lat", "lon"], hist_area),     
            "ssp_area":      (["lat", "lon"], ssp_area),     
            "ntcf_area":     (["lat", "lon"], ntcf_area), 
            "diff_area":     (["lat", "lon"], diff_area),          
        },
        coords={
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
        },
        )

ncfile.attrs['description'] = 'Created on 2024-3-29. This file save the area definition of the global monsoon, while 1 indicates it fullfil the criterion. The script is cal_AerChemMIP_global_monsoon_area_definition_240329.py'
ncfile.to_netcdf(data_path + 'globalmonsoon_area_modelmean_hist_ssp370_ssp370ntcf.nc')