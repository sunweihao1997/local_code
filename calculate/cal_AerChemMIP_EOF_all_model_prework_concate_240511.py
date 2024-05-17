'''
2024-5-11
This script serves the second EOF analysis, which concatenate all the model.
Here I use precipitation to do the analysis, masking the ocean data and deal with historical, SSP370 and SSP370lowNTCF respectively

Note: I will standardize the series
'''
import xarray as xr
import numpy as np
import os
import sys
from eofs.standard import Eof

sys.path.append("/home/sun/local_code/calculate/")
from cal_AerChemMIP_band_pass_calculation_240428 import band_pass_calculation

# ======== File Information =============
data_path  = '/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid_linear1.5/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'MPI-ESM-1-2-HAM', 'MIROC6']

mask_file    = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid1.5x1.5.nc').sel(latitude=slice(0, 60), longitude=slice(60, 140)) 

# Get the list for 3 scenarios
all_list   = os.listdir(data_path)
hist_list  = []
ssp3_list  = []
ntcf_list  = []


# add the files into corresponding list
for filename0 in all_list:
    # split the filename0
    filename0_split = filename0.split("_")

    if filename0_split[0] not in models_label:
        continue
    else:
        if filename0_split[1] == 'historical':
            hist_list.append(filename0)
        elif filename0_split[1] == 'SSP370':
            ssp3_list.append(filename0)
        elif filename0_split[1] == 'SSP370NTCF':
            ntcf_list.append(filename0)

def standardize_array(input_array):
    '''
        This function calculate the standardization for the input array
    '''
    std  = np.std(input_array, axis=0)
    mean = np.nanmean(input_array, axis=0)

    standardization_array = (input_array - mean)

    return standardization_array

def concatenate_arrays(list1, expname):
    '''
        The list1 is the list which includes the single experiment
    '''
    # 1. Claim an empty list save the array for every models
    all_models_high = []
    all_models_low  = []

    # 2. Read every file and only extract MJJAS data
    for file1 in list1:
        f1 = xr.open_dataset(data_path + file1).sel(lat=slice(0, 60), lon=slice(60, 140)) # only include Asia region
        
        if expname == 'historical':
            f1 = f1.sel(time=f1.time.dt.year.isin(np.linspace(1980, 2014, 2014-1980+1)))
        else:
            f1 = f1.sel(time=f1.time.dt.year.isin(np.linspace(2031, 2050, 2050-2031+1)))

        f1_MJJAS = f1.sel(time=f1.time.dt.month.isin([5, 6, 7, 8, 9]))

        # 2.1 Mask the value over ocean
        varname = 'pr'
        f1_MJJAS[varname].data[:, mask_file['lsm'].data[0]<0.05] = np.nan

        # 2.2 Send to standardization function
        stand_pr = standardize_array(f1_MJJAS[varname].data)

        stand_pr_high = stand_pr.copy()
        stand_pr_low  = stand_pr.copy()

        # 2.3 Butterworth filter
        for i in range(len(f1.lat.data)):
            for j in range(len(f1.lon.data)):
                stand_pr_high[:, i, j] = band_pass_calculation(stand_pr[:, i, j], fs=1, low_frq=20, high_frq=8,  order=5,)
                stand_pr_low[:, i, j]  = band_pass_calculation(stand_pr[:, i, j], fs=1, low_frq=70, high_frq=20, order=5,)

        # 2.4 Add it to the all_models
        all_models_high.append(stand_pr_high)
        all_models_low.append(stand_pr_low)
    
    print('standardization process now complete!')

    # 3. call concatenate function
    a = np.concatenate(all_models_high, axis=0)
    b = np.concatenate(all_models_low, axis=0)
    
    return a, b

def EOF_analysis(input_data, lat):

    coslat  = np.cos(np.deg2rad(lat))
    wgts    = np.sqrt(coslat)[:, np.newaxis]

    solver1 = Eof(input_data, weights=wgts)

    eof     = solver1.eofsAsCorrelation(neofs=3)
    pc      = solver1.pcs(npcs=3, pcscaling=1)
    var     = solver1.varianceFraction(neigs=3)

    return eof, pc, var

if __name__ == '__main__':
    ntcf_concatenate_high, ntcf_concatenate_low = concatenate_arrays(ntcf_list, 'furt')
    hist_concatenate_high, hist_concatenate_low = concatenate_arrays(hist_list, 'historical')
    ssp3_concatenate_high, ssp3_concatenate_low = concatenate_arrays(ssp3_list, 'furt')

    # Send it to calculate EOFs
    ref_file = xr.open_dataset('/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid_linear1.5/MPI-ESM-1-2-HAM_SSP370_r1i1p1f1.nc').sel(lat=slice(0, 60), lon=slice(60, 140))
    lat      = ref_file.lat.data
    lon      = ref_file.lon.data

    ncfile = xr.Dataset()


    # =========== The following is writing process ===============
    # ------------------- NTCF ------------------------
    eof, pc, var = EOF_analysis(ntcf_concatenate_high, lat)
    ncfile['ntcf_high_eof'] = xr.DataArray(data=eof, dims=["num", "lat", "lon"],
                                    coords=dict(num=(["num"], [1, 2, 3]), lon=(["lon"], lon), lat=(["lat"], lat)))
    ncfile['ntcf_high_pc']  = xr.DataArray(data=pc, dims=["time0", "num"],
                                    coords=dict(num=(["num"], [1, 2, 3])))
    ncfile['ntcf_high_var'] = xr.DataArray(data=var, dims=["num"],
                                    coords=dict(num=(["num"], [1, 2, 3])))

    eof, pc, var = EOF_analysis(ntcf_concatenate_low, lat)
    ncfile['ntcf_low_eof'] = xr.DataArray(data=eof, dims=["num", "lat", "lon"],
                                    coords=dict(num=(["num"], [1, 2, 3]), lon=(["lon"], lon), lat=(["lat"], lat)))
    ncfile['ntcf_low_pc']  = xr.DataArray(data=pc, dims=["time0", "num"],
                                    coords=dict(num=(["num"], [1, 2, 3])))
    ncfile['ntcf_low_var'] = xr.DataArray(data=var, dims=["num"],
                                    coords=dict(num=(["num"], [1, 2, 3])))
    # -------------------- historical ------------------------
    eof, pc, var = EOF_analysis(hist_concatenate_high, lat)
    ncfile['hist_high_eof'] = xr.DataArray(data=eof, dims=["num", "lat", "lon"],coords=dict(num=(["num"], [1, 2, 3]), lon=(["lon"], lon), lat=(["lat"], lat)))
    ncfile['hist_high_pc']  = xr.DataArray(data=pc, dims=["time1", "num"],coords=dict(num=(["num"], [1, 2, 3])))
    ncfile['hist_high_var'] = xr.DataArray(data=var, dims=["num"], coords=dict(num=(["num"], [1, 2, 3])))

    eof, pc, var = EOF_analysis(hist_concatenate_low, lat)
    ncfile['hist_low_eof'] = xr.DataArray(data=eof, dims=["num", "lat", "lon"],coords=dict(num=(["num"], [1, 2, 3]), lon=(["lon"], lon), lat=(["lat"], lat)))
    ncfile['hist_low_pc']  = xr.DataArray(data=pc, dims=["time1", "num"],coords=dict(num=(["num"], [1, 2, 3])))
    ncfile['hist_low_var'] = xr.DataArray(data=var, dims=["num"],coords=dict(num=(["num"], [1, 2, 3])))

    # -------------------- SSP370lowNTCF ------------------------
    eof, pc, var = EOF_analysis(ssp3_concatenate_high, lat)
    ncfile['ssp3_high_eof'] = xr.DataArray(data=eof, dims=["num", "lat", "lon"],coords=dict(num=(["num"], [1, 2, 3]), lon=(["lon"], lon), lat=(["lat"], lat)))
    ncfile['ssp3_high_pc']  = xr.DataArray(data=pc, dims=["time2", "num"],coords=dict(num=(["num"], [1, 2, 3])))
    ncfile['ssp3_high_var'] = xr.DataArray(data=var, dims=["num"], coords=dict(num=(["num"], [1, 2, 3])))

    eof, pc, var = EOF_analysis(ssp3_concatenate_low, lat)
    ncfile['ssp3_low_eof'] = xr.DataArray(data=eof, dims=["num", "lat", "lon"],coords=dict(num=(["num"], [1, 2, 3]), lon=(["lon"], lon), lat=(["lat"], lat)))
    ncfile['ssp3_low_pc']  = xr.DataArray(data=pc, dims=["time2", "num"],coords=dict(num=(["num"], [1, 2, 3])))
    ncfile['ssp3_low_var'] = xr.DataArray(data=var, dims=["num"],coords=dict(num=(["num"], [1, 2, 3])))

    ncfile.to_netcdf('/home/sun/data/process/analysis/AerChem/EoFs.nc')
    #print(eof_test.shape)
    #print(pc_test.shape)
    #print(var_test.shape)