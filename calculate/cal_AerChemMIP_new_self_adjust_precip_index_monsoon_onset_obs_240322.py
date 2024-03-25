'''
2024-3-22
This script is to calculate a new monsoon onset criterion based on the precipitation

The new criterion is based on the percentile, which empahsize the percentile of the 5mm/day on each grid
'''

import xarray as xr
import numpy as np
from scipy.fft import fft, ifft

data_mod = xr.open_dataset('/home/sun/data/process/analysis/AerChem/multiple_model_climate_prect_daily.nc')
data_obs = xr.open_dataset('/home/sun/data/process/analysis/AerChem/observation/NCEP2_precipitation_climate_annual_evolution_1980_2014.nc')

harmonic_number = 12

#print(data_obs.time.data) # All the variable use the same time-axis, which is 2000 year 365 days, but it is 1980-2014 for the hist, 2031-2050 for the SSP370

# calculate the first serveral harmonics
def harmonics_sum_f(x, num):
    precipitation_fft = fft(x)
    #print(precipitation_fft.shape)

    n = len(x)
    harmonics_sum = np.zeros(n, dtype=complex)

    harmonics_sum[1:1 + num] = precipitation_fft[1:1 + num]  # first 12 harmonics
    harmonics_sum[-num:] = precipitation_fft[-num:]  

    reconstructed_signal = ifft(harmonics_sum).real

    return reconstructed_signal + np.average(x)

def find_percentile_of_number(arr, number):
    '''from chatgpt'''
    # 确保数组是有序的
    sorted_arr = np.sort(arr)
    
    # 找出数字在数组中的位置，如果数字不在数组中，则返回应插入的位置
    index = np.searchsorted(sorted_arr, number)
    
    # 计算百分位数
    # 注意：由于`searchsorted`可能返回的是数组长度（即number比数组中所有元素都大的情况），需要处理这一特殊情况
    if index >= len(arr):
        percentile = 100
    else:
        percentile = (index / len(arr)) * 100
        
    return percentile

def calculate_the_percentile(array):
    ''' array should be 1D '''
    # 1. Calculate the January average

    # 2. calculate the harmonic of the series
    harmonic_array = harmonics_sum_f(array, harmonic_number)

    jan_avg = np.average(array[:30])

    # 3. threshold is the sum of Jan-avg and 5 mm/day
    percentile_num = 5 + jan_avg

    return find_percentile_of_number(array, percentile_num)

def calculate_the_percentile_whole_year(array):
    ''' This function is to generate the models percentile array '''
    percentile_array = np.zeros((360))

    harmonic_array = harmonics_sum_f(array, harmonic_number)

    for i in range(len(array)):
        percentile_array[i] = find_percentile_of_number(harmonic_array, harmonic_array[i])

    return percentile_array

def calculate_onset(array, reference):
    precentile0 = reference

    if np.isnan(reference):
        return 0
    else:
        start_day   = 70
        for dddd in range(265):
            if array[start_day + dddd] < reference:
#            if np.sum(array[start_day + dddd: start_day + dddd + 5] > reference) < 4:
                continue
            else:

                break

        return start_day + dddd



# --- Test the harmonic ---
#testa = harmonics_sum_f(data_obs['precip'].data[:, 0, 100], 12)
#print(testa.shape) #it generates an array of length of 365
#print(np.nanmax(data_obs.precip.data))

# === Claim the percentile array ===
percentile_obs = np.zeros((len(data_obs.lat.data), len(data_obs.lon.data)))

for i in range(len(data_obs.lat.data)):
    for j in range(len(data_obs.lon.data)):
        percentile_obs[i, j] = calculate_the_percentile(data_obs['precip'].data[:, i, j])

percentile_obs[percentile_obs >= 99] = np.nan

ncfile  =  xr.Dataset(
        {
            "percentile_obs":     (["lat", "lon"], percentile_obs),          
        },
        coords={
            "lat":  (["lat"],  data_obs.lat.data),
            "lon":  (["lon"],  data_obs.lon.data),
        },
        )


# ================= Calculate each model/experiment percentile =======================
models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'NorESM2-LM', 'MPI-ESM-1-2-HAM', 'MIROC6',] # except GISS
for mm in models_label:

    for ee in ['hist', 'ssp', 'sspntcf']:
        percentile_model0 = np.zeros((360, len(data_obs.lat.data), len(data_obs.lon.data)))

        onset_model0      = np.zeros((len(data_obs.lat.data), len(data_obs.lon.data)))

        for i in range(len(data_obs.lat.data)):
            for j in range(len(data_obs.lon.data)):
                percentile_model0[:, i, j] = calculate_the_percentile_whole_year(data_mod[mm + '_' + ee].data[:, i, j])

                onset_model0[i, j]         = calculate_onset(percentile_model0[:, i, j], percentile_obs[i, j])


        ncfile['percentile_' + mm + '_' + ee] = xr.DataArray(data=percentile_model0, dims=["time", "lat", "lon"], coords=dict(lon=(["lon"], data_mod.lon.data), lat=(["lat"], data_mod.lat.data), time=data_mod.time.data))
        ncfile['onsetdate_' + mm + '_' + ee] = xr.DataArray(data=onset_model0, dims=["lat", "lon"], coords=dict(lon=(["lon"], data_mod.lon.data), lat=(["lat"], data_mod.lat.data),))
    
    print(f'Finish the {mm}')

ncfile.attrs['description'] = 'Created on 2024-3-22. This data saves the percentile of the precipitation on each grid. For the obs it is 2-D array which is the percentile of the monsoon onset criterion (Jan + 5). For the models it is the 3-D array which is the time-evolution'

ncfile.to_netcdf('/home/sun/data/process/analysis/AerChem/' + 'NCEP_AerChemMIP_monsoon_percentile_onsetdate.nc')