'''
2024-8-10
This script is to calculate the spatial onset dates based on BinWang (2002) criterion

cititation: Onset of the summer monsoon over the Indochina Peninsula: Climatology and interannual variations

'''
import xarray as xr
import numpy as np
from scipy.fft import fft, ifft

import matplotlib.pyplot as plt

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'MPI-ESM-1-2-HAM', 'MIROC6', ]
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'MPI-ESM-1-2-HAM', 'MIROC6', ]


f0 = xr.open_dataset('/home/sun/data/process/analysis/AerChem/multiple_model_eachyear_prect_daily.nc')
#print(f0)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def harmonics_sum_f(x, num):
    precipitation_fft = fft(x)
    #print(precipitation_fft.shape)

    n = len(x)
    harmonics_sum = np.zeros(n, dtype=complex)

    harmonics_sum[1:1 + num] = precipitation_fft[1:1 + num]  # first 12 harmonics
    harmonics_sum[-num:] = precipitation_fft[-num:]  

    reconstructed_signal = ifft(harmonics_sum).real

    return reconstructed_signal + np.average(x)

#print(f0)
# ------- The length of the time axis is 12600, which is not divisible for 365 -------
def return_1year_data(f0, year_num):
    f0_year = f0.sel(time=f0.time.dt.year.isin([year_num]))

    return f0_year

def judge_monsoon_onset(pr_series, start=90, threshold=5, thresholdday=10):
    '''
        The input is series of precipitation, start from the 90th day
    '''
    for i in range(0, 220):
#        if pr_series[start + i] -  np.average(pr_series[0:30])< threshold:
#            continue
        if np.average(pr_series[start + i - 2 : start + i + 3]) - np.average(pr_series[0:30]) < threshold :
            continue
#        elif np.sum(pr_series[start +i : start + i + 20] > threshold) < 5:
#            continue
#        elif (np.average(pr_series[start + i : start + i +5]) - np.average(pr_series[0:30])) < 4.:
#            continue

        else:
            break

    return start + i
            
def generate_onset_array(f0,):

    onset_array = np.zeros((len(models_label), int(len(f0.lat.data)), int(len(f0.lon.data))))

    return onset_array

def show_format_of_year(f0):
    '''
        This is because the total number of each year in model is not the same, e.g. 360 days in UKESM
    '''

threshold0 = 4
onset_array_hist = np.zeros((30, len(models_label), int(len(f0.lat.data)), int(len(f0.lon.data))))
onset_array_ssp3 = np.zeros((20, len(models_label), int(len(f0.lat.data)), int(len(f0.lon.data))))
onset_array_ntcf = np.zeros((20, len(models_label), int(len(f0.lat.data)), int(len(f0.lon.data))))

j = 0
num = 10
# 1. calculate for hist - 20 year
print(f'Now it is dealing with historical')
for yy in range(30):
    for mm in range(len(models_label)):
        for latt in range(len(f0.lat.data)):
            for lonn in range(len(f0.lon.data)): 
                #onset_array[latt, lonn] = judge_monsoon_onset(moving_average(f0['EC-Earth3-AerChem_hist'].data[:, latt, lonn] * 86400, 5), threshold=threshold0)
                onset_array_hist[yy, mm, latt, lonn] = judge_monsoon_onset(harmonics_sum_f(f0['{}_hist'.format(models_label[mm])].data[yy, :, latt, lonn] * 86400, num), threshold=threshold0)

print(f'Now it is dealing with future')
for yy in range(20):
    for mm in range(len(models_label)):
        for latt in range(len(f0.lat.data)):
            for lonn in range(len(f0.lon.data)): 
                #onset_array[latt, lonn] = judge_monsoon_onset(moving_average(f0['EC-Earth3-AerChem_hist'].data[:, latt, lonn] * 86400, 5), threshold=threshold0)
                onset_array_ssp3[yy, mm, latt, lonn] = judge_monsoon_onset(harmonics_sum_f(f0['{}_ssp'.format(models_label[mm])].data[yy, :, latt, lonn] * 86400, num), threshold=threshold0)
                onset_array_ntcf[yy, mm, latt, lonn] = judge_monsoon_onset(harmonics_sum_f(f0['{}_sspntcf'.format(models_label[mm])].data[yy, :, latt, lonn] * 86400, num), threshold=threshold0)

#sys.exit()

    #print(f1.pr)
#onset_array[onset_array == 70] = np.nan
#onset_hist = np.nanmean(onset_array_hist, axis=0)
#onset_ssp3 = np.nanmean(onset_array_ssp3, axis=0)
#onset_ntcf = np.nanmean(onset_array_ntcf, axis=0)
onset_hist = onset_array_hist
onset_ssp3 = onset_array_ssp3
onset_ntcf = onset_array_ntcf

ncfile  =  xr.Dataset(
    {
        "onset_hist":     (["hist_year", "model", "lat", "lon"], onset_hist),       
        "onset_ssp3":     (["furt_year", "model", "lat", "lon"], onset_ssp3),       
        "onset_ntcf":     (["furt_year", "model", "lat", "lon"], onset_ntcf),       
    },
    coords={
        "lat":  (["lat"],  f0.lat.data),
        "lon":  (["lon"],  f0.lon.data),
        "hist_year":  (["hist_year"],  f0.year_hist.data),
        "furt_year":  (["furt_year"],  f0.year_furt.data),
        "model":      (["model"],      models_label),
    },
    )

ncfile.attrs['description'] = 'This file includes single models every years onset date'
ncfile.to_netcdf('/home/sun/data/process/analysis/AerChem/' + 'singlemodel_onset_day_threshold4_10_harmonics_each_year.nc')

#f0 = xr.open_dataset('/home/sun/data/process/analysis/AerChem/multiple_model_climate_prect_daily.nc').sel(lat=slice(10, 30), lon=slice(105, 120))

#area_prect = np.zeros((360))
#for i in range(360):
#    area_prect[i] = np.average(f0['MIROC6_hist'].data[i]) * 86400
#
#fig, ax1 = plt.subplots()
#
#t = np.linspace(1, 360, 360)
#ax1.plot(t, area_prect, color='black', linewidth=1.5)
##ax1.plot(t[2:-2], moving_average(area_prect, 5), color='red', linewidth=1.5)
#ax1.plot(t, harmonics_sum_f(area_prect, 12), color='blue', linewidth=1.5)
#
#plt.savefig('origin_line_Huanan.png')
#plt.close()

#climate_prect = np.zeros((360, len(f0.lat.data), len(f0.lon.data)))
#for tt in range(35):
#    for j in range(len(f0.lat.data)):
#        for k in range(len(f0.lon.data)):
#            for dd in range(360):
#                climate_prect[dd, j, k] += np.average(f0.pr.data[tt * 360 + dd, j, k]) / 35
#
#climate_prect_area = np.zeros((360))
#
#for dd in range(360):
#    climate_prect_area[dd] = np.average(climate_prect[dd]) * 86400
#
#fig, ax1 = plt.subplots()
##
#t = np.linspace(1, 360, 360)
##ax1.plot(t, area_prect, color='black', linewidth=1.5)
##ax1.plot(t[2:-2], moving_average(area_prect, 5), color='red', linewidth=1.5)
#ax1.plot(t, climate_prect_area, color='black', linewidth=1.5)
#ax1.plot(t, harmonics_sum_f(climate_prect_area, 12), color='blue', linewidth=1.5)
#
#
#plt.savefig('origin_line_BOB_climate.png')
#plt.close()