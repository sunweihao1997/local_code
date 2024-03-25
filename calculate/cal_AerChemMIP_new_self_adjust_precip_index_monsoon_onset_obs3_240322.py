'''
2024-3-23
This script is to calculate a new monsoon onset criterion based on the precipitation

The new criterion is based on the Zeng (2004), https://journals.ametsoc.org/view/journals/clim/17/11/1520-0442_2004_017_2241_gumoar_2.0.co_2.xml
'''

import xarray as xr
import numpy as np
from scipy.fft import fft, ifft

data_mod = xr.open_dataset('/home/sun/data/process/analysis/AerChem/multiple_model_climate_prect_daily.nc')
data_obs = xr.open_dataset('/home/sun/data/download_data/CMAP/precip.mon.ltm.1981-2010.nc')
data_obs = data_obs.interp(lat = data_mod.lat.data, lon=data_mod.lon.data)

#print(data_obs.precip.data[0, :, 50])

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
    # The range
    max_n = np.nanmax(arr)
    min_n = np.nanmin(arr)

    percentile0 = (number - min_n) / (max_n - min_n)

    return percentile0

def calculate_the_percentile(array):
    ''' array should be 1D '''

    jan_avg = np.average(array[0])

    # 3. threshold is the sum of Jan-avg and 5 mm/day
    percentile_num = 5 + jan_avg

    return find_percentile_of_number(array, percentile_num)

def cal_moving_average(x, w):
    return np.convolve(x, np.ones(w), "same") / w

def calculate_the_percentile_whole_year(array):
    ''' This function is to generate the models percentile array '''
    percentile_array = np.zeros((360))

    harmonic_array = cal_moving_average(array, 5)

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
#            if array[start_day + dddd] < reference:
            if array[start_day + dddd: start_day + dddd +3] < 0.618:
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

ncfile.to_netcdf('/home/sun/data/process/analysis/AerChem/' + 'NCEP_AerChemMIP_monsoon_percentile_onsetdate_Zeng.nc')