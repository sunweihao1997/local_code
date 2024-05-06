'''
2024-5-1
This script is about the prework for the EOF analysis: calculating the model mean value
'''
import xarray as xr
import numpy as np
import os

# ================ Files location ======================
models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ] # GISS provide no daily data

data_path_8_20  = '/home/sun/data/process/model/aerchemmip-postprocess/day_prect_8_20/'
data_path_20_70 = '/home/sun/data/process/model/aerchemmip-postprocess/day_prect_20_70/'

mask_file    = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid2x2.nc')

data_file_high = os.listdir(data_path_8_20) ; data_file_high.sort()
data_file_low  = os.listdir(data_path_20_70); data_file_low.sort()

region_Asia    = [0, 60, 60, 140]

#========================================================

# ---------------- First. Deal with the low-frequency data ------------------------
# Claim the array for multi-models value
hist_model = np.zeros((len(models_label), 150*35, 91, 181))
ssp3_model = np.zeros((len(models_label), 150*26, 91, 181))
ntcf_model = np.zeros((len(models_label), 150*26, 91, 181))



m = 0 # number for model account
for model0 in models_label:
    print(f'Now it is dealing with model {model0}')
    # Get the file list for each experiment about single model result
    hist_single_model = []
    ssp3_single_model = []
    ntcf_single_model = []

    data_path = data_path_20_70
    for file0 in data_file_low: # modify this parameter to change which frequency for calculating
        file0_split = file0.split("_")

        if file0_split[0] != model0:
            continue
        
        else:
            if 'historical' in file0:
                hist_single_model.append(file0)
            
            elif file0_split[1] == 'SSP370':
                ssp3_single_model.append(file0)

            elif file0_split[1] == 'SSP370NTCF':
                ntcf_single_model.append(file0)
    
    if len(hist_single_model) != len(ssp3_single_model) or len(ssp3_single_model) != len(ntcf_single_model):
        sys.exit(f'Now it is dealing with model {model0} the hist, ssp and ntcf file numbers are {len(hist_single_model)} {len(ssp3_single_model)} and {len(ntcf_single_model)}')

    # Here I process data for historical, SSP370 and SSP370lowNTCF respectively
    # ----------------- Historical --------------------
    # Claim the array for average result
    prect_hist = np.zeros((35*150, 91, 181))
    

    for ff0 in hist_single_model:
        f0    = xr.open_dataset(data_path + ff0)

        # 1. Select out the MJJAS data
        f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))

        # 1.1 Select historical years and furture years: 1980-2014 for historical and 2025-2050 for furture simulation
        if 'historical' in ff0:
            year_sel = np.linspace(1980, 2014, 2014-1980+1)
        else:
            year_sel = np.linspace(2025, 2050, 2050-2025+1)

        f0_MJJAS = f0_MJJAS.sel(time=f0_MJJAS.time.dt.year.isin(year_sel))



        # 3. calculate the series for the regional precipitation
        #print(f0_MJJAS_SA)
        f0_MJJAS['filter_pr'].data[:, mask_file['lsm'].data[0] < 0.05] = np.nan

        #print(len(f0_MJJAS_SA.time))
        intermediate_result = f0_MJJAS['filter_pr'].data - np.average(f0_MJJAS['filter_pr'].data, axis=0)

        prect_hist += (intermediate_result[:int(150 * len(year_sel))] / len(hist_single_model))

    # ----------------- SSP370 --------------------
    # Claim the array for average result
    prect_ssp3 = np.zeros((26*150, 91, 181))
    

    for ff0 in ssp3_single_model:
        f0    = xr.open_dataset(data_path + ff0)

        # 1. Select out the MJJAS data
        f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))

        # 1.1 Select historical years and furture years: 1980-2014 for historical and 2025-2050 for furture simulation
        if 'historical' in ff0:
            year_sel = np.linspace(1980, 2014, 2014-1980+1)
        else:
            year_sel = np.linspace(2025, 2050, 2050-2025+1)

        f0_MJJAS = f0_MJJAS.sel(time=f0_MJJAS.time.dt.year.isin(year_sel))

        # 3. calculate the series for the regional precipitation
        #print(f0_MJJAS_SA)
        f0_MJJAS['filter_pr'].data[:, mask_file['lsm'].data[0] < 0.05] = np.nan

        #print(len(f0_MJJAS_SA.time))
        intermediate_result = f0_MJJAS['filter_pr'].data - np.average(f0_MJJAS['filter_pr'].data, axis=0)

        prect_ssp3 += (intermediate_result[:int(150 * len(year_sel))] / len(ssp3_single_model))

    # ----------------- SSP370NTCF --------------------
    # Claim the array for average result
    prect_ntcf = np.zeros((26*150, 91, 181))
    
    for ff0 in ntcf_single_model:
        f0    = xr.open_dataset(data_path + ff0)

        # 1. Select out the MJJAS data
        f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))

        # 1.1 Select historical years and furture years: 1980-2014 for historical and 2025-2050 for furture simulation
        if 'historical' in ff0:
            year_sel = np.linspace(1980, 2014, 2014-1980+1)
        else:
            year_sel = np.linspace(2025, 2050, 2050-2025+1)

        f0_MJJAS = f0_MJJAS.sel(time=f0_MJJAS.time.dt.year.isin(year_sel))

        # 3. calculate the series for the regional precipitation
        #print(f0_MJJAS_SA)
        f0_MJJAS['filter_pr'].data[:, mask_file['lsm'].data[0] < 0.05] = np.nan

        #print(len(f0_MJJAS_SA.time))
        intermediate_result = f0_MJJAS['filter_pr'].data - np.average(f0_MJJAS['filter_pr'].data, axis=0)

        prect_ntcf += (intermediate_result[:int(150 * len(year_sel))] / len(ntcf_single_model))

    hist_model[m,] = prect_hist
    ssp3_model[m,] = prect_ssp3
    ntcf_model[m,] = prect_ntcf

    m += 1

ncfile  =  xr.Dataset(
    {
        "hist_model":     (["model", "time0", "lat", "lon"], hist_model),
        "ssp3_model":     (["model", "time1", "lat", "lon"], ssp3_model),
        "ntcf_model":     (["model", "time1", "lat", "lon"], ntcf_model), 
    },
    coords={
        "model":        (["model"],models_label),
        "lat":          (["lat"],  f0.lat.data),
        "lon":          (["lon"],  f0.lon.data),
    },
    )

ncfile.attrs['description'] = 'Created on 2024-5-2. This file save the multiple models summertime 8-20 values over Asia'

out_path  = '/home/sun/data/process/analysis/AerChem/'
ncfile.to_netcdf(out_path + '20-70_pr_MJJAS_multiple_model_result.nc')  