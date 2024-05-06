'''
2024-4-29
This script is to calculate the regional averaged series for power spectra analysis

Here I select three regions:
1. SA: (70-85E, 15-25N)
2. Indochina: (95-110E, 10-20N)
3. EA: (105-120E, 22.5-32.5N)
'''
import xarray as xr
import numpy as np
import os
import sys

# ================= File Information =====================

data_path = '/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid_linear/'
out_path  = '/home/sun/data/process/analysis/AerChem/regional_pr_MJJAS_v2/'

mask_file    = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid2x2.nc')

# Region division
region_SA = [15, 25, 70, 85]
region_ID = [10, 20, 95, 110]
region_EA = [22.5, 32.5, 105, 120]

file_list = os.listdir(data_path) ; file_list.sort()

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ]

# ========================================================

def cal_daily_anomaly(f0):
    # 1. Define how many days per year, e.g. in UKESM it is 360 days
    years = np.unique(f0.time.dt.year.data)
    
    # 2. Initialize the array
    anomaly_array = np.zeros((len(f0.time.data)))

    # 3. Get how many days in one year
    f0_1yr = f0.sel(time=f0.time.dt.year.isin([years[1]]))

    days   = f0_1yr.time.data # about 148 days

    if (len(f0.time.data) / len(years)) != len(days):
        sys.exit('Wrong')

#    else:
#        print('Pass the test')

    
    for i in range(len(days)):
        # 1. Generate index
        index_day = np.arange(i, len(f0.time.data), len(days))

        #print(index_day)
        anomaly_array[index_day] = (np.nanmean(np.nanmean(f0['pr'].data[index_day], axis=1), axis=1) - np.nanmean(f0['pr'].data[index_day])) * 86400

    # 4. Normalization
    anomaly_array = np.convolve(anomaly_array, np.ones(3), "valid") / 3
    anomaly_array = (anomaly_array - anomaly_array.min()) / (anomaly_array.max() - anomaly_array.min())

    return anomaly_array
        
# ======================= calculate the model mean ===============================
# Initialize the model-mean array, the second axis corresponds to the regions (SA, Indo, EA)
hist_model = np.zeros((len(models_label), 3, 148*35))
ssp3_model = np.zeros((len(models_label), 3, 148*26))
ntcf_model = np.zeros((len(models_label), 3, 148*26))

m = 0 # number for model account
for model0 in models_label:
    print(f'Now it is dealing with model {model0}')
    # Get the file list for each experiment about single model result
    hist_single_model = []
    ssp3_single_model = []
    ntcf_single_model = []

    for file0 in file_list:
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
    prect_SA_hist = np.zeros((35*148)) ; prect_ID_hist = np.zeros((35*148)) ; prect_EA_hist = np.zeros((35*148))

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

        # 2. Regional selection
        f0_MJJAS_SA = f0_MJJAS.sel(lat=slice(region_SA[0], region_SA[1]), lon=slice(region_SA[2], region_SA[3])) ; mask_file_SA = mask_file.sel(latitude=slice(region_SA[0], region_SA[1]), longitude=slice(region_SA[2], region_SA[3]))
        f0_MJJAS_ID = f0_MJJAS.sel(lat=slice(region_ID[0], region_ID[1]), lon=slice(region_ID[2], region_ID[3])) ; mask_file_ID = mask_file.sel(latitude=slice(region_ID[0], region_ID[1]), longitude=slice(region_ID[2], region_ID[3]))
        f0_MJJAS_EA = f0_MJJAS.sel(lat=slice(region_EA[0], region_EA[1]), lon=slice(region_EA[2], region_EA[3])) ; mask_file_EA = mask_file.sel(latitude=slice(region_EA[0], region_EA[1]), longitude=slice(region_EA[2], region_EA[3]))

        # 3. calculate the series for the regional precipitation
        #print(f0_MJJAS_SA)
        f0_MJJAS_SA['pr'].data[:, mask_file_SA['lsm'].data[0] < 0.05] = np.nan
        f0_MJJAS_ID['pr'].data[:, mask_file_ID['lsm'].data[0] < 0.05] = np.nan
        f0_MJJAS_EA['pr'].data[:, mask_file_EA['lsm'].data[0] < 0.05] = np.nan

        #print(len(f0_MJJAS_SA.time))
        intermediate_result1 = cal_daily_anomaly(f0_MJJAS_SA)
        intermediate_result2 = cal_daily_anomaly(f0_MJJAS_ID)
        intermediate_result3 = cal_daily_anomaly(f0_MJJAS_EA)
        #print(intermediate_result1.shape)
        prect_SA_hist += (intermediate_result1[:int(148 * len(year_sel))] / len(hist_single_model))
        prect_ID_hist += (intermediate_result2[:int(148 * len(year_sel))] / len(hist_single_model))
        prect_EA_hist += (intermediate_result3[:int(148 * len(year_sel))] / len(hist_single_model))

    # ----------------- SSP370 --------------------
    prect_SA_ssp3 = np.zeros((26*148)) ; prect_ID_ssp3 = np.zeros((26*148)) ; prect_EA_ssp3 = np.zeros((26*148))

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

        # 2. Regional selection
        f0_MJJAS_SA = f0_MJJAS.sel(lat=slice(region_SA[0], region_SA[1]), lon=slice(region_SA[2], region_SA[3])) ; mask_file_SA = mask_file.sel(latitude=slice(region_SA[0], region_SA[1]), longitude=slice(region_SA[2], region_SA[3]))
        f0_MJJAS_ID = f0_MJJAS.sel(lat=slice(region_ID[0], region_ID[1]), lon=slice(region_ID[2], region_ID[3])) ; mask_file_ID = mask_file.sel(latitude=slice(region_ID[0], region_ID[1]), longitude=slice(region_ID[2], region_ID[3]))
        f0_MJJAS_EA = f0_MJJAS.sel(lat=slice(region_EA[0], region_EA[1]), lon=slice(region_EA[2], region_EA[3])) ; mask_file_EA = mask_file.sel(latitude=slice(region_EA[0], region_EA[1]), longitude=slice(region_EA[2], region_EA[3]))

        # 3. calculate the series for the regional precipitation
        #print(f0_MJJAS_SA)
        f0_MJJAS_SA['pr'].data[:, mask_file_SA['lsm'].data[0] < 0.05] = np.nan
        f0_MJJAS_ID['pr'].data[:, mask_file_ID['lsm'].data[0] < 0.05] = np.nan
        f0_MJJAS_EA['pr'].data[:, mask_file_EA['lsm'].data[0] < 0.05] = np.nan

        intermediate_result1 = cal_daily_anomaly(f0_MJJAS_SA)
        intermediate_result2 = cal_daily_anomaly(f0_MJJAS_ID)
        intermediate_result3 = cal_daily_anomaly(f0_MJJAS_EA)
        prect_SA_ssp3 += (intermediate_result1[:int(148 * len(year_sel))] / len(ssp3_single_model))
        prect_ID_ssp3 += (intermediate_result2[:int(148 * len(year_sel))] / len(ssp3_single_model))
        prect_EA_ssp3 += (intermediate_result3[:int(148 * len(year_sel))] / len(ssp3_single_model))

    # ----------------- SSP370NTCF --------------------
    prect_SA_ntcf = np.zeros((26*148)) ; prect_ID_ntcf = np.zeros((26*148)) ; prect_EA_ntcf = np.zeros((26*148))

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

        # 2. Regional selection
        f0_MJJAS_SA = f0_MJJAS.sel(lat=slice(region_SA[0], region_SA[1]), lon=slice(region_SA[2], region_SA[3])) ; mask_file_SA = mask_file.sel(latitude=slice(region_SA[0], region_SA[1]), longitude=slice(region_SA[2], region_SA[3]))
        f0_MJJAS_ID = f0_MJJAS.sel(lat=slice(region_ID[0], region_ID[1]), lon=slice(region_ID[2], region_ID[3])) ; mask_file_ID = mask_file.sel(latitude=slice(region_ID[0], region_ID[1]), longitude=slice(region_ID[2], region_ID[3]))
        f0_MJJAS_EA = f0_MJJAS.sel(lat=slice(region_EA[0], region_EA[1]), lon=slice(region_EA[2], region_EA[3])) ; mask_file_EA = mask_file.sel(latitude=slice(region_EA[0], region_EA[1]), longitude=slice(region_EA[2], region_EA[3]))

        # 3. calculate the series for the regional precipitation
        #print(f0_MJJAS_SA)
        f0_MJJAS_SA['pr'].data[:, mask_file_SA['lsm'].data[0] < 0.05] = np.nan
        f0_MJJAS_ID['pr'].data[:, mask_file_ID['lsm'].data[0] < 0.05] = np.nan
        f0_MJJAS_EA['pr'].data[:, mask_file_EA['lsm'].data[0] < 0.05] = np.nan

        intermediate_result1 = cal_daily_anomaly(f0_MJJAS_SA)
        intermediate_result2 = cal_daily_anomaly(f0_MJJAS_ID)
        intermediate_result3 = cal_daily_anomaly(f0_MJJAS_EA)
        prect_SA_ntcf += (intermediate_result1[:int(148 * len(year_sel))] / len(ntcf_single_model))
        prect_ID_ntcf += (intermediate_result2[:int(148 * len(year_sel))] / len(ntcf_single_model))
        prect_EA_ntcf += (intermediate_result3[:int(148 * len(year_sel))] / len(ntcf_single_model))

    hist_model[m, 0] = prect_SA_hist ; hist_model[m, 1] = prect_ID_hist ; hist_model[m, 2] = prect_EA_hist
    ssp3_model[m, 0] = prect_SA_ssp3 ; ssp3_model[m, 1] = prect_ID_ssp3 ; ssp3_model[m, 2] = prect_EA_ssp3
    ntcf_model[m, 0] = prect_SA_ntcf ; ntcf_model[m, 1] = prect_ID_ntcf ; ntcf_model[m, 2] = prect_EA_ntcf

    m += 1



ncfile  =  xr.Dataset(
    {
        "hist_model":     (["model", "region", "time0"], hist_model),
        "ssp3_model":     (["model", "region", "time1"], ssp3_model),
        "ntcf_model":     (["model", "region", "time1"], ntcf_model), 
    },
    coords={
#        "time":         (["time"], np.linspace(1, )),
        "model":        (["model"],models_label),
        "region":       (["region"],["SA", "ID", "EA"]),
    },
    )

ncfile.attrs['description'] = 'Created on 2024-4-30. This file save the multiple models regional summer precipitation anomalies, which have been normalized'

ncfile.to_netcdf(out_path + 'multiple_model_result.nc')            