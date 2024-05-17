'''
2024-5-7
This script is to calculate the model mean for the 4 variables denoted in the title
'''
import xarray as xr
import numpy as np
import os

var_list = ['uas', 'vas', 'rlut', 'psl']

# ============== File Information ==================
models_label_all = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ] # GISS provide no daily data

data_path    = '/home/sun/data/process/model/aerchemmip-postprocess/vvvv_regrid/'

# =================================================

def cal_modelmean_singlevar(data_path0, var0, models_label):
    # 1. Modify the path
    data_path1 = data_path0.replace('vvvv', var0)
    data_file  = os.listdir(data_path1)

    # 2. Claim the averaged array for 3 scenarios
    # Note that for each variable the covered model may vary
    hist_model = np.zeros((len(models_label), 150*35, 119, 240))
    ssp3_model = np.zeros((len(models_label), 150*26, 119, 240))
    ntcf_model = np.zeros((len(models_label), 150*26, 119, 240))

    m = 0 # number for model account
    for model0 in models_label:
        print(f'Now it is dealing with model {model0}')
        # Get the file list for each experiment about single model result
        hist_single_model = []
        ssp3_single_model = []
        ntcf_single_model = []

        for file0 in data_file: # modify this parameter to change which frequency for calculating
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

        if len(ssp3_single_model) != len(ntcf_single_model):
            sys.exit(f'Now it is dealing with model {model0} the hist, ssp and ntcf file numbers are {len(hist_single_model)} {len(ssp3_single_model)} and {len(ntcf_single_model)}')

        # Here I process data for historical, SSP370 and SSP370lowNTCF respectively
        # ----------------- Historical --------------------
        # Claim the array for average result
        var_hist = np.zeros((35*150, 119, 240))
    

        for ff0 in hist_single_model:
            f0    = xr.open_dataset(data_path1 + ff0)

            # 1. Select out the MJJAS data
            f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))
            #print(f0_MJJAS[var0][:int(150 * 35)].shape)

            var_hist += (f0_MJJAS[var0][:int(150 * 35)] / len(hist_single_model))

        # ----------------- SSP370 --------------------
        # Claim the array for average result
        var_ssp3 = np.zeros((26*150, 119, 240))
    

        for ff0 in ssp3_single_model:
            f0    = xr.open_dataset(data_path1 + ff0)

            # 1. Select out the MJJAS data
            f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))

            var_ssp3 += (f0_MJJAS[var0][:int(150 * 26)] / len(hist_single_model))

        # ----------------- SSP370NTCF --------------------
        # Claim the array for average result
        var_ntcf = np.zeros((26*150, 119, 240))
    

        for ff0 in ntcf_single_model:
            f0    = xr.open_dataset(data_path1 + ff0)

            # 1. Select out the MJJAS data
            f0_MJJAS = f0.sel(time=f0.time.dt.month.isin([5, 6, 7, 8, 9]))

            var_ntcf += (f0_MJJAS[var0][:int(150 * 26)] / len(hist_single_model))

        hist_model[m,] = var_hist
        ssp3_model[m,] = var_ssp3
        ntcf_model[m,] = var_ntcf

        m += 1

    return hist_model, ssp3_model, ntcf_model



if __name__ == '__main__':
    uas_hist, uas_ssp370, uas_ntcf = cal_modelmean_singlevar(data_path, var_list[0], models_label_all)
    vas_hist, vas_ssp370, vas_ntcf = cal_modelmean_singlevar(data_path, var_list[1], models_label_all)
    rlut_hist,rlut_ssp370,rlut_ntcf= cal_modelmean_singlevar(data_path, var_list[2], ['UKESM1-0-LL', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6'])
    psl_hist, psl_ssp370, psl_ntcf = cal_modelmean_singlevar(data_path, var_list[3], ['GFDL-ESM4', 'UKESM1-0-LL', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6'])
    
    # save to the ncfile
    f0 = xr.open_dataset('/home/sun/data/process/model/aerchemmip-postprocess/vas_regrid/EC-Earth3-AerChem_SSP370NTCF_r4i1p1f1.nc')
    # 1. Uas
    ncfile_uas  =  xr.Dataset(
    {
        "hist_model":     (["model", "time0", "lat", "lon"], uas_hist),
        "ssp3_model":     (["model", "time1", "lat", "lon"], uas_ssp370),
        "ntcf_model":     (["model", "time1", "lat", "lon"], uas_ntcf), 
    },
    coords={
        "model":        (["model"],models_label_all),
        "lat":          (["lat"],  f0.lat.data),
        "lon":          (["lon"],  f0.lon.data),
    },
    )

    ncfile_uas.attrs['description'] = 'Created on 2024-5-7. This file save the multiple models summertime uas. Generated by cal_AerChemMIP_model_mean_uas_vas_psl_olr_240507.py.'

    out_path  = '/home/sun/data/process/analysis/AerChem/'
    ncfile_uas.to_netcdf(out_path + 'uas_MJJAS_multiple_model_result2.nc')  

    # 2. Vas
    ncfile_vas  =  xr.Dataset(
    {
        "hist_model":     (["model", "time0", "lat", "lon"], vas_hist),
        "ssp3_model":     (["model", "time1", "lat", "lon"], vas_ssp370),
        "ntcf_model":     (["model", "time1", "lat", "lon"], vas_ntcf), 
    },
    coords={
        "model":        (["model"],models_label_all),
        "lat":          (["lat"],  f0.lat.data),
        "lon":          (["lon"],  f0.lon.data),
    },
    )

    ncfile_vas.attrs['description'] = 'Created on 2024-5-7. This file save the multiple models summertime vas. Generated by cal_AerChemMIP_model_mean_uas_vas_psl_olr_240507.py.'

    out_path  = '/home/sun/data/process/analysis/AerChem/'
    ncfile_vas.to_netcdf(out_path + 'vas_MJJAS_multiple_model_result2.nc') 

    # 3. Rlut
    ncfile_rlut  =  xr.Dataset(
    {
        "hist_model":     (["model", "time0", "lat", "lon"], rlut_hist),
        "ssp3_model":     (["model", "time1", "lat", "lon"], rlut_ssp370),
        "ntcf_model":     (["model", "time1", "lat", "lon"], rlut_ntcf), 
    },
    coords={
        "model":        (["model"],['UKESM1-0-LL', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6']),
        "lat":          (["lat"],  f0.lat.data),
        "lon":          (["lon"],  f0.lon.data),
    },
    )

    ncfile_rlut.attrs['description'] = 'Created on 2024-5-7. This file save the multiple models summertime rlut. Generated by cal_AerChemMIP_model_mean_uas_vas_psl_olr_240507.py.'

    out_path  = '/home/sun/data/process/analysis/AerChem/'
    ncfile_rlut.to_netcdf(out_path + 'rlut_MJJAS_multiple_model_result2.nc') 

    # 4. Psl
    ncfile_psl  =  xr.Dataset(
    {
        "hist_model":     (["model", "time0", "lat", "lon"], psl_hist),
        "ssp3_model":     (["model", "time1", "lat", "lon"], psl_ssp370),
        "ntcf_model":     (["model", "time1", "lat", "lon"], psl_ntcf), 
    },
    coords={
        "model":        (["model"],['GFDL-ESM4', 'UKESM1-0-LL', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6']),
        "lat":          (["lat"],  f0.lat.data),
        "lon":          (["lon"],  f0.lon.data),
    },
    )

    ncfile_psl.attrs['description'] = 'Created on 2024-5-7. This file save the multiple models summertime psl. Generated by cal_AerChemMIP_model_mean_uas_vas_psl_olr_240507.py.'

    out_path  = '/home/sun/data/process/analysis/AerChem/'
    ncfile_psl.to_netcdf(out_path + 'psl_MJJAS_multiple_model_result2.nc') 