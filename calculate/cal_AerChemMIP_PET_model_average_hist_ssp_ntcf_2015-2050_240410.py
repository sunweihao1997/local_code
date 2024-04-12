'''
2024-4-10
This script is to calculate the model averaged PET for the historical, SSP370 and SSP370lowNTCF experiments

Note: PET file contains 3 varibles, PET, PET_adv, PET_rad. Here I change the name manually
'''
import xarray as xr
import numpy as np
import os

#
src_path = '/data/AerChemMIP/LLNL_PET/postprocess-samegrid/pet/'
out_path = '/data/AerChemMIP/process/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'MIROC6', 'MPI-ESM-1-2-HAM', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G',]
#models_label = ['EC-Earth3-AerChem', 'GFDL-ESM4', 'GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM',]
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G',  'MIROC6', 'CNRM-ESM']
#models_label = ['EC-Earth3-AerChem', 'GISS-E2-1-G',]
#models_label = ['GISS-E2-1-G',]
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM', ]
#good_group   =  ['EC-Earth3-AerChem', 'GISS-E2-1-G', 'MIROC6', 'MPI-ESM-1-2-HAM',]
#bad_group    =  ['BCC-ESM1', 'CESM2-WACCM', 'NorESM2-LM', 'GFDL-ESM4']
#models_label = ['EC-Earth3-AerChem',]

files_all = os.listdir(src_path)

model_number = len(models_label)

hist_models       = np.zeros((model_number, 65 * 12, 121, 241))
ssp370_models     = np.zeros((model_number, 36 * 12, 121, 241))
ssp370ntcf_models = np.zeros((model_number, 36 * 12, 121, 241))
hist_ssp370_models     = np.zeros((model_number, 36 * 12, 121, 241))
hist_ssp370ntcf_models = np.zeros((model_number, 36 * 12, 121, 241))

varname = 'pet'

for i in range(model_number):
    model_name = models_label[i]

    print('It is {}'.format(model_name))
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


        #print(f0_select[varname].attrs['units']) # All of them are kg m-2 s-1
        #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
        ssp370_pr_avg += (f0_select[varname].data / model_numbers_ssp370)

    for ff in ssp370NTCF_files:
        f0 = xr.open_dataset(src_path + ff)

        f0_select = f0.sel(time=f0.time.dt.year.isin(np.linspace(2015, 2050, 36)))

        #print(f0_select[varname].attrs['units']) # All of them are kg m-2 s-1
        #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
        ssp370ntcf_pr_avg += (f0_select[varname].data / model_numbers_ssp370NTCF)

    for ff in hist_files:
        f0 = xr.open_dataset(src_path + ff)

        f0_select_hist = f0.sel(time=f0.time.dt.year.isin(np.linspace(1950, 2014, 65)))

        #print(f0_select[varname].attrs['units']) # All of them are kg m-2 s-1
        #print(f'for the {ff} the time length is {len(f0_select.time.data)}') # All of them are 360 length
        hist_pr_avg       += (f0_select_hist[varname].data / model_numbers_hist)

    # Save the value to the array
    
#    if model_name in good_group:
#        ssp370_models[i] = (ssp370_pr_avg) * 1.0
#        ssp370ntcf_models[i] = ssp370ntcf_pr_avg * 1.0
#    elif model_name in bad_group:
#        ssp370_models[i] = (ssp370_pr_avg) * 0.0
#        ssp370ntcf_models[i] = ssp370ntcf_pr_avg * 0.0
#    else:
#        ssp370_models[i] = (ssp370_pr_avg) * 1.0
#        ssp370ntcf_models[i] = ssp370ntcf_pr_avg * 1.0

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
        '{}_ssp'.format(varname):  (["time", "lat", "lon"], np.average(ssp370_models, axis=0)),
        '{}_ntcf'.format(varname): (["time", "lat", "lon"], np.average(ssp370ntcf_models, axis=0)),
        '{}_hist'.format(varname): (["time_hist", "lat", "lon"], np.average(hist_models, axis=0)),
        'allmodel_{}_ssp'.format(varname):   (["model", "time", "lat", "lon"], ssp370_models),
        'allmodel_{}_ntcf'.format(varname):  (["model", "time", "lat", "lon"], ssp370ntcf_models),
        'allmodel_{}_hist'.format(varname):  (["model", "time_hist", "lat", "lon"], hist_models),
    },
    coords={
        "time": (["time"], f0_select.time.data),
        "time_hist": (["time_hist"], f0_select_hist.time.data),
        "lat":  (["lat"],  f0_select.lat.data),
        "lon":  (["lon"],  f0_select.lon.data),
        "model":(["model"], models_label)
    },
    )

ncfile1['{}_ssp'.format(varname)].attrs['units'] = 'mm day**-1'
ncfile1['{}_ntcf'.format(varname)].attrs['units'] = 'mm day**-1'
ncfile1['{}_hist'.format(varname)].attrs['units'] = 'mm day**-1'
#ncfile1['diff_pr_ssp'].attrs['units'] = 'mm day-1'
#ncfile1['diff_pr_ntcf'].attrs['units'] = 'mm day-1'

ncfile1.attrs['description'] = 'Created on 2024-4-10. This file save the AerChemMIP PET data.'
ncfile1.attrs['Mother'] = 'local-code: cal_AerChemMIP_PET_model_average_hist_ssp_ntcf_2015-2050_240410.py'
#

#print(ncfile1)
ncfile1.to_netcdf(out_path + 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_PET_2015-2050.nc')