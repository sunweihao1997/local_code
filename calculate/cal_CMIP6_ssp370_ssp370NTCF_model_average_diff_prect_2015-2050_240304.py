'''
2024-3-4
This script is to calculate the SSP370 and SSP370NTCF period difference between 2015-2050, representing the future scenarios

This script is modified from cal_CMIP6_ssp370_ssp370NTCF_model_average_prect_2015-2050_240229.py. In the old script I noticed that when the members number is different, the result will be influenced.
Thus I decide to use another way to calculate the difference between SSP370 and SSP370lowNTCF experiment, I calculate each models response and calculate average of these differences
'''
import xarray as xr
import numpy as np
import os

#
src_path = '/data/AerChemMIP/LLNL_download/postprocess_samegrids/'
out_path = '/data/AerChemMIP/LLNL_download/model_average/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL','GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM', 'NorESM2-LM', 'GFDL-ESM4', 'MRI-ESM2']
#models_label = ['EC-Earth3-AerChem', 'GFDL-ESM4', 'GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM',]
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G',  'MIROC6', 'CNRM-ESM']
#models_label = ['EC-Earth3-AerChem', 'GISS-E2-1-G',]
#models_label = ['GISS-E2-1-G',]
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM', ]
good_group   =  ['EC-Earth3-AerChem', 'GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM',]
bad_group    =  ['BCC-ESM1', 'CESM2-WACCM', 'NorESM2-LM', 'GFDL-ESM4']

files_all = os.listdir(src_path)

model_number = len(models_label)

hist_models       = np.zeros((model_number, 65 * 12, 121, 241))
ssp370_models     = np.zeros((model_number, 36 * 12, 121, 241))
ssp370ntcf_models = np.zeros((model_number, 36 * 12, 121, 241))
hist_ssp370_models     = np.zeros((model_number, 36 * 12, 121, 241))
hist_ssp370ntcf_models = np.zeros((model_number, 36 * 12, 121, 241))

for i in range(model_number):
    model_name = models_label[i]
    #print(model_name)

    # screen out the target models and historical experiments
    hist_files        = []
    ssp370_files      = []
    ssp370NTCF_files  = []

    for ffff in files_all:
        name_list = ffff.split("_")
        modelname = name_list[0]
        #print(modelname)
        if 'SSP370' in ffff and 'NTCF' not in ffff and 'CMIP6' not in ffff and modelname == model_name:
            ssp370_files.append(ffff)
        elif 'SSP370NTCF' in ffff and 'CMIP6' not in ffff and modelname == model_name:
            ssp370NTCF_files.append(ffff)
        elif 'historical' in ffff and 'NTCF' not in ffff and 'CMIP6' not in ffff and modelname == model_name:
            hist_files.append(ffff)

    #!!! Notice that the IPSL starts from 1950 !!!

    # Calculate the muti-models average
    hist_pr_avg        =  np.zeros((65 * 12, 121, 241)) # 2015-2050, 36year
    ssp370_pr_avg      =  np.zeros((36 * 12, 121, 241)) # 2015-2050, 36year
    ssp370ntcf_pr_avg  =  np.zeros((36 * 12, 121, 241)) # 2015-2050, 36year

    model_numbers_hist        =  len(hist_files)  ; print(model_numbers_hist)
    model_numbers_ssp370      =  len(ssp370_files) ; print(model_numbers_ssp370)
    model_numbers_ssp370NTCF  =  len(ssp370NTCF_files)  ; print(model_numbers_ssp370NTCF)

    for ff in ssp370_files:
        f0 = xr.open_dataset(src_path + ff)

        f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2015, 2050, 36)))
        #print(f0_select)


        #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
        #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
        ssp370_pr_avg += (f0_select['pr'].data * 86400 / model_numbers_ssp370)

    for ff in ssp370NTCF_files:
        f0 = xr.open_dataset(src_path + ff)

        f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2015, 2050, 36)))

        #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
        #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
        ssp370ntcf_pr_avg += (f0_select['pr'].data * 86400 / model_numbers_ssp370NTCF)

    for ff in hist_files:
        f0 = xr.open_dataset(src_path + ff)

        f0_select_hist = f0.sel(time=f0.time.dt.year.isin(np.linspace(1950, 2014, 65)))

        #print(f0_select['pr'].attrs['units']) # All of them are kg m-2 s-1
        #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
        hist_pr_avg       += (f0_select_hist['pr'].data * 86400 / model_numbers_hist)

    # Save the value to the array
    
    if model_name in good_group:
        ssp370_models[i] = (ssp370_pr_avg) * 1.0
        ssp370ntcf_models[i] = ssp370ntcf_pr_avg * 1.0
    elif model_name in bad_group:
        ssp370_models[i] = (ssp370_pr_avg) * 0.0
        ssp370ntcf_models[i] = ssp370ntcf_pr_avg * 0.0
    else:
        ssp370_models[i] = (ssp370_pr_avg) * 1.0
        ssp370ntcf_models[i] = ssp370ntcf_pr_avg * 1.0

    ssp370_models[i]     = ssp370_pr_avg
    ssp370ntcf_models[i] = ssp370ntcf_pr_avg
    hist_models[i]       = hist_pr_avg

    # ============== Here I want to calculate the single models response ================
#    ssp370_pr_diff_hist     = ssp370_pr_avg.copy()
#    ssp370ntcf_pr_diff_hist = ssp370ntcf_pr_avg.copy()
#    #print(ssp370_pr_avg.shape)
#    for j in range(12): 
#        #print(ssp370_pr_diff_hist[np.arange(i, 36*12, 12)].shape)
#        ssp370_pr_diff_hist[np.arange(j, 36*12, 12)] = ssp370_pr_avg[np.arange(j, 36*12, 12)] - np.average(hist_pr_avg[np.arange(j, 65*12, 12)], axis=0)
#        ssp370ntcf_pr_diff_hist[np.arange(j, 36*12, 12)] = ssp370ntcf_pr_diff_hist[np.arange(j, 36*12, 12)] - np.average(hist_pr_avg[np.arange(j, 65*12, 12)], axis=0)
#
##    print(ssp370_pr_diff_hist.shape)
#    hist_ssp370_models[i] = ssp370_pr_diff_hist
#    hist_ssp370ntcf_models[i] = ssp370ntcf_pr_diff_hist

# =================== Calculate the models deviation =========================

# Write to ncfile
ncfile1  =  xr.Dataset(
    {
        'pr_ssp':  (["time", "lat", "lon"], np.average(ssp370_models, axis=0)),
        'pr_ntcf': (["time", "lat", "lon"], np.average(ssp370ntcf_models, axis=0)),
#        'diff_pr_ssp':  (["time", "lat", "lon"], np.average(hist_ssp370_models, axis=0)),
#        'diff_pr_ntcf': (["time", "lat", "lon"], np.average(hist_ssp370ntcf_models, axis=0)),
        'pr_hist': (["time_hist", "lat", "lon"], np.average(hist_models, axis=0)),
        'allmodel_pr_ssp':   (["model", "time", "lat", "lon"], ssp370_models),
        'allmodel_pr_ntcf':  (["model", "time", "lat", "lon"], ssp370ntcf_models),
    },
    coords={
        "time": (["time"], f0_select.time.data),
        "time_hist": (["time_hist"], f0_select_hist.time.data),
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
        "model":(["model"], models_label)
    },
    )

ncfile1['pr_ssp'].attrs['units'] = 'mm day-1'
ncfile1['pr_ntcf'].attrs['units'] = 'mm day-1'
ncfile1['pr_hist'].attrs['units'] = 'mm day-1'
#ncfile1['diff_pr_ssp'].attrs['units'] = 'mm day-1'
#ncfile1['diff_pr_ntcf'].attrs['units'] = 'mm day-1'

ncfile1.attrs['description'] = 'Created on 2024-3-4. This file save the CMIP6 SSP370 monthly precipitation data. The result is the multi-model average of the difference between SSP370 and SSP370NTCF'
ncfile1.attrs['Mother'] = 'local-code: cal_CMIP6_ssp370_ssp370NTCF_model_average_diff_prect_2015-2050_240304.py'
#

ncfile1.to_netcdf(out_path + 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_precipitation_2015-2050.nc')