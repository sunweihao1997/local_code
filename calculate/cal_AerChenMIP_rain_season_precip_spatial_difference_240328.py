'''
2024-3-28
This script is to calculate the response of rainy-season precipitation difference between SSP370 and SSP370lowNTCF
'''
import xarray as xr
import numpy as np

data_path = '/home/sun/data/process/analysis/AerChem/'
data_name = 'multiple_model_climate_prect_daily_new.nc'

date_withdraw   = 'modelmean_withdraw_day_threshold4_reverse.nc'
date_onset      = 'modelmean_onset_day_threshold4_new.nc'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6',]

precip_f     = xr.open_dataset(data_path + data_name)
onset_f      = xr.open_dataset(data_path + date_onset)
withdraw_f   = xr.open_dataset(data_path + date_withdraw)

lat          = precip_f.lat.data ; lon        = precip_f.lon.data
time         = precip_f.time.data

def cal_rain_in_monsoon_season(onsetday, withdrawday, array):
    '''
        This input is 1D array, which will be calculate the total precipitation in this period
        it should return 2 variables: 1. total precipitation during rainy season 2. intensity of the precipitation in rainy season
    '''
    length_season = withdrawday - onsetday

    avg_precip    = np.average(array[onsetday:withdrawday])
    tot_precip    = avg_precip * length_season

    return tot_precip, avg_precip

def cal_modelmean(exp_tag):
    model_mean = np.zeros((len(time), len(lat), len(lon)))

    for mm in models_label:
        model_mean += (precip_f[mm + exp_tag].data / len(models_label))

    return model_mean

# Calculate the modelmean for hist, ssp370 and ssp370lowntcf
p_hist  =  cal_modelmean('_hist')
p_ssp3  =  cal_modelmean('_ssp')
p_ntcf  =  cal_modelmean('_sspntcf')

rain_change_total     = np.zeros((91, 181))
rain_change_intensity = np.zeros((91, 181))

for i in range(91):
    for j in range(181):
        #print(onset_f['onset_ssp3'].data[i, j])
        a1, b1 = cal_rain_in_monsoon_season(int(onset_f['onset_ssp3'].data[i, j]), int(withdraw_f['withdraw_ssp3'].data[i, j]), p_ssp3[:, i, j])
        a2, b2 = cal_rain_in_monsoon_season(int(onset_f['onset_ntcf'].data[i, j]), int(withdraw_f['withdraw_ntcf'].data[i, j]), p_ntcf[:, i, j])


        rain_change_total[i, j] = (a1 - a2) * 86400
        rain_change_intensity[i, j] = (b1 - b2) * 86400

# ------------ Write to a ncfile  ------------------
ncfile  =  xr.Dataset(
        {
            "rain_change_total_modelmean":     (["lat", "lon"], rain_change_total),     
            "rain_change_intensity_modelmean": (["lat", "lon"], rain_change_intensity),             
        },
        coords={
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
        },
        )

ncfile.attrs['description']   = 'Created on 2024-3-28. This file use daily precipitation, onset date and withdraw date to calculate the difference in the total rainy-season precipitation and intensity of which.'
ncfile.attrs['script']        = 'cal_AerChenMIP_rain_season_precip_spatial_difference_240328.py'

ncfile.to_netcdf(data_path + 'modelmean_total_precip_rainy_season_diff_SSP370_SSP370lowNTCF.nc')