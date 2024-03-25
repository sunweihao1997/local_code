'''
2024-3-22
This script is to calculate a new monsoon onset criterion based on the precipitation

The new criterion is based on the percentile, which empahsize the percentile of the 5mm/day on each grid
The percentile number based on NCEP has been generated
'''

import xarray as xr
import numpy as np
from scipy.fft import fft, ifft

data_mod = xr.open_dataset('/home/sun/data/process/analysis/AerChem/multiple_model_climate_prect_daily.nc')
data_obs = xr.open_dataset('/home/sun/data/process/analysis/AerChem/observation/NCEP_precipitation_climate_annual_evolution_1980_2014.nc')
obs_precentile = xr.open_dataset('/home/sun/data/process/analysis/AerChem/' + 'NCEP_monsoon_percentile.nc')

harmonic_number = 10

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
    percentile_num = 4 + jan_avg

    return find_percentile_of_number(array, percentile_num)

