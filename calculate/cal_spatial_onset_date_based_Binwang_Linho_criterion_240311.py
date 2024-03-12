'''
2024-3-11
This script is to calculate the spatial onset dates based on Zhang (2002) criterion

cititation: Onset of the summer monsoon over the Indochina Peninsula: Climatology and interannual variations

This is the test script
'''
import xarray as xr
import numpy as np

f0 = xr.open_dataset('/home/sun/pr_day_UKESM1-0-LL_ssp370-lowNTCF_r1i1p1f2_gn_20150101-20491230.nc')

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

#print(f0)
# ------- The length of the time axis is 12600, which is not divisible for 365 -------
def return_1year_data(f0, year_num):
    f0_year = f0.sel(time=f0.time.dt.year.isin([year_num]))

    return f0_year

def judge_monsoon_onset(pr_series, start=90, threshold=5, thresholdday=10):
    '''
        The input is series of precipitation, start from the 90th day
    '''
    for i in range(0, 180):
        if pr_series[start + i] < 5:
            continue
        elif np.average(pr_series[start + i : start + i +5]) < 5:
            continue
        elif np.sum(pr_series[start +i : start + i + 20] > 5) <10:
            continue

        else:
            break

    return start + i + 1
            
def generate_onset_array(f0, year_format):
    year_number = f0.time.shape[0] / year_format

    print(f'The total number of year is {year_number}')

    onset_array = np.zeros((int(year_number), int(len(f0.lat.data)), int(len(f0.lon.data))))

    return onset_array

def show_format_of_year(f0):
    '''
        This is because the total number of each year in model is not the same, e.g. 360 days in UKESM
    '''
    print(f0.time[0])

onset_array = generate_onset_array(f0, 360)

year_list   = np.linspace(2015, 2049, 35)
for i in range(len(year_list)):
    print(f'It is dealing with {year_list[i]}')
    f1 = return_1year_data(f0, year_list[i])

    for latt in range(len(f1.lat.data)):
        for lonn in range(len(f1.lon.data)): 
            onset_array[i, latt, lonn] = judge_monsoon_onset(moving_average(f1.pr.data[:, latt, lonn] * 86400, 5))
    #print(f1.pr)
onset_array[onset_array == 90] == np.nan

ncfile  =  xr.Dataset(
    {
        "onset_day":     (["year", "lat", "lon"], onset_array),       
    },
    coords={
        "year":  (["year"],  year_list),
        "lat":  (["lat"],  f0.lat.data),
        "lon":  (["lon"],  f0.lon.data),
    },
    )


ncfile.to_netcdf('/home/sun/' + 'UKESM_onset_day.nc')