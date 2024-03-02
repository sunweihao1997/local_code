'''
2024-2-29
This script is to calculate and plot the trend in the May/June precipitation under SSP370/SSP370NTCF for the period 2015-2050
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import scipy.stats as stats
import pymannkendall as mk

data_path = '/data/AerChemMIP/LLNL_download/postprocess_samegrids/'
data_name = 'CMIP6_model_SSP370_SSP370NTCF_month56_precipitation_2015-2050.nc'

f0        = xr.open_dataset(data_path + data_name)

def cal_trend_mktest(data):
    trends  = np.zeros((data.shape[1], data.shape[2]))
    p_value = trends.copy()
#    print(data)
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            if np.isnan(data[0, i, j]):
                continue
            else:
                slope, intercept = np.polyfit(np.linspace(1, data.shape[0], data.shape[0]), data[:, i, j], 1)

                trends[i, j] = slope

    #            print(data[:, i, j])
                mktest       = mk.original_test(data[:, i, j])

                p_value[i, j]= mktest.p

    return trends, p_value

def main():
    # Calculate trends for May/June and SSP370/SSP370NTCF
#    print(f0['pr_May_SSP370'].data)
    May_SSP370, p_May_SSP370         = cal_trend_mktest(f0['pr_May_SSP370'].data)
    May_SSP370NTCF, p_May_SSP370NTCF = cal_trend_mktest(f0['pr_May_SSP370NTCF'].data)
    Jun_SSP370, p_Jun_SSP370         = cal_trend_mktest(f0['pr_Jun_SSP370'].data)
    Jun_SSP370NTCF, p_Jun_SSP370NTCF = cal_trend_mktest(f0['pr_Jun_SSP370NTCF'].data)

    ncfile  =  xr.Dataset(
    {
        "pr_trend_May_SSP370":     (["lat", "lon"], May_SSP370),
        "pr_trend_Jun_SSP370":     (["lat", "lon"], Jun_SSP370),
        "pr_trend_May_SSP370NTCF": (["lat", "lon"], May_SSP370NTCF),
        "pr_trend_Jun_SSP370NTCF": (["lat", "lon"], Jun_SSP370NTCF),
        "p_trend_May_SSP370":      (["lat", "lon"], p_May_SSP370),
        "p_trend_Jun_SSP370":      (["lat", "lon"], p_Jun_SSP370),
        "p_trend_May_SSP370NTCF":  (["lat", "lon"], p_May_SSP370NTCF),
        "p_trend_Jun_SSP370NTCF":  (["lat", "lon"], p_Jun_SSP370NTCF),

       
    },
    coords={
        "lat":  (["lat"],  f0.lat.data),
        "lon":  (["lon"],  f0.lon.data),
    },
    )

    #ncfile['pr'].attrs['units'] = 'mm day-1'

    ncfile.attrs['description'] = 'Created on 2024-2-29. This file save the CMIP6 SSP370 and SSP370NTCF May and June monthly precipitation trend, for the period 2015-2050'
    ncfile.attrs['Mother'] = 'local-code: paint_AerChemMIP_trends_spatial_May_June_240229.py'
    #

    ncfile.to_netcdf(data_path + 'CMIP6_model_SSP370_SSP370NTCF_month56_precipitation_trends_2015-2050.nc')

if __name__ == '__main__':
    main()