'''
2024-4-14
This script is to provide the 15day sample for the Heat-Wave analysis.
The reference link is https://iopscience.iop.org/article/10.1088/1748-9326/ac1edb

According to the article, first I should generate sample for each day to decide the range of the threshold. This is the 
15 days period whose center locates on the day for research.

Eventually, it should give the 15 * years sample.
Only deal with the historical simulation, only focus on the 1980-2014 climatology
'''
import xarray as xr
import numpy as np
import os
import pandas as pd

period_num = 15

# Analysis months
months     = [6, 7, 8, 9]
months_ex  = [5, 6, 7, 8, 9, 10] # Provide data for the head and end of the target month

def get_one_year_sample(f0, varname,):
    '''
        The input should be 1 year's data
        The return data should be (day, 15, lat, lon)
    '''
    # 1. Filter out the target month
    f0_mon1 = f0.sel(time=f0.time.dt.month.isin(months))
    f0_mon2 = f0.sel(time=f0.time.dt.month.isin(months_ex))

    # 2. Claim the array to save the result
    sample_1yr = np.zeros((len(f0_mon1.time.data), 15, len(f0_mon1.lat.data), len(f0_mon1.lon.data)))
#    print(sample_1yr.shape)

    # 3. Start process
    time_loc1  = 31 ; time_loc2   =  122 # Corresponding to the 1 Jun and 31 Aug

#    print(f0_mon2.time[time_loc2])
    j = 0 # the day
    for dd in range(len(f0_mon1.time.data)):
#        print(f0_mon1.time.data[dd])
        sample_1yr[dd, :, :, :] = f0_mon2[varname].data[(time_loc1 + dd - 7):(time_loc1 + dd + 8)]

    return sample_1yr

def get_multiple_year_sample(path0, filename, endpath):
    print(f'Now it is dealing with the file {filename}')
    file0 = xr.open_dataset(path0 + filename)

#    print(year_list)
    # Claim the array to save the result
    file0         = file0.sel(time=file0.time.dt.year.isin(np.linspace(1980, 2014, 2014 - 1980 + 1))) # only for the year 1980-2014
    # 1. Get the number of the year
    year_list = np.unique(file0.time.dt.year.data)

    file0_mon     = file0.sel(time=file0.time.dt.month.isin([6, 7, 8, 9]))
    file0_mon_1yr = file0_mon.sel(time=file0_mon.time.dt.year.isin([file0_mon.time.dt.year.data[0]]))

    sample_multiple_year = np.zeros((len(year_list), len(file0_mon_1yr.time.data), 15, len(file0.lat.data), len(file0.lon.data)))
#    print(sample_multiple_year.shape)

    # 2. calculate for each year
    for yy in range(len(year_list)):
        #print(f'First stage, one year dealing with, now it is {yy}')
        file0_1yr = file0.sel(time=file0.time.dt.year.isin([year_list[yy]]))

        sample_multiple_year[yy] = get_one_year_sample(file0_1yr, 'tasmax')


    # 2. 1 exchange the axis
    sample_multiple_year = sample_multiple_year.swapaxes(0, 1) # day, year , 15, lat, lon
    sample_multiple_year = sample_multiple_year.astype(np.float32)


    # 3. reshape the array
#    sample_multiple_year_reshape = np.zeros((len(file0_mon_1yr.time.data), 15 * len(year_list), len(file0.lat.data), len(file0.lon.data)))

    #sample_multiple_year_reshape = sample_multiple_year.reshape(new_shape)
    # 4. Find the 90th, 95th, 99th percentile
    percentile1 = np.zeros((len(file0_mon_1yr.time.data), len(file0.lat.data), len(file0.lon.data))) # 90th
    percentile2 = np.zeros((len(file0_mon_1yr.time.data), len(file0.lat.data), len(file0.lon.data))) # 95th
    percentile3 = np.zeros((len(file0_mon_1yr.time.data), len(file0.lat.data), len(file0.lon.data))) # 99th

#     The following array is too slow here I need to change the code
#    for yy in range(len(file0_mon_1yr.time.data)):
#        print(f'Second stage, each day dealing, now it is {yy}')
#        for latt in range(len(file0.lat.data)):
#            for lonn in range(len(file0.lon.data)):
#                sample_multiple_year_reshape[yy, :, latt, lonn] = sample_multiple_year[:, yy, :, latt, lonn].reshape((15 * len(year_list)))
#
#                percentile1[yy, latt, lonn] = np.percentile(sample_multiple_year_reshape, 90)
#                percentile2[yy, latt, lonn] = np.percentile(sample_multiple_year_reshape, 95)
#                percentile3[yy, latt, lonn] = np.percentile(sample_multiple_year_reshape, 99)
    # ----------------------- New code for calculation ---------------------------
    sample_multiple_year_reshape = sample_multiple_year.reshape((len(file0_mon_1yr.time.data), 15*len(year_list), len(file0.lat.data), len(file0.lon.data)))

    percentile1                  = np.percentile(sample_multiple_year_reshape, 90, axis=1)
    percentile2                  = np.percentile(sample_multiple_year_reshape, 95, axis=1)
    percentile3                  = np.percentile(sample_multiple_year_reshape, 99, axis=1)

    del sample_multiple_year_reshape


    # 5. Calculation finish, write to ncfile
    # ------------ Write to a ncfile  ------------------
    dates = pd.date_range(start='2000-06-01', end='2000-09-30', freq='D') #The problem is that in some model (UKESM) it is 120 day in JJAS
    date_numpy = dates.to_numpy()
    ncfile  =  xr.Dataset(
            {
                "threshold90":     (["time", "lat", "lon"], percentile1),     
                "threshold95":     (["time", "lat", "lon"], percentile2),     
                "threshold99":     (["time", "lat", "lon"], percentile3),          
            },
            coords={
                "time": (["time"], date_numpy[:len(file0_mon_1yr.time.data)]),
                "lat":  (["lat"],  file0.lat.data),
                "lon":  (["lon"],  file0.lon.data),
            },
            )
    ncfile.attrs['description'] = 'Created on 15-Apr-2024 by cal_AerChemMIP_heatwave_analysis_15day_sample_240414.py. The data in this file is the pencentile of the tasmax/tasmin based on 1980-2014 historical simulation'

    ncfile.to_netcdf(endpath + filename)

    del ncfile

if __name__ == '__main__':
    path0 = '/home/sun/data/process/model/aerchemmip-postprocess/tasmax/'
    path_out = '/home/sun/data/process/analysis/AerChem/heat_wave/sample_JJAS/tasmax/'

    file_lists = os.listdir(path0)

    for ff in file_lists:
        if 'histor' in ff:
            get_multiple_year_sample(path0, ff, path_out)


    # test
#    ftest  = xr.open_dataset('/home/sun/data/process/model/aerchemmip-postprocess/tasmax/EC-Earth3-AerChem_historical_r1i1p1f1.nc')
#
#    ftest2 = ftest.sel(time=ftest.time.dt.year.isin([2000]))
#
#    get_one_year_sample(ftest2, 'tasmax')
#    print(file_lists[1])
#    get_multiple_year_sample(path0, file_lists[1])