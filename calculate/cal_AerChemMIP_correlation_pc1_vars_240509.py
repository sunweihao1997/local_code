'''
2024-5-9
This script is to calculate the correlation between pc1 and other variables (uas, vas, psl, rlut)
'''
import xarray as xr
import numpy as np

# ================= File Information ====================
# 1. Read the PC1 file 
data_path   =  '/home/sun/data/process/analysis/AerChem/'
high_EOF    =  xr.open_dataset(data_path + 'AerchemMIP_Asia_EOF_land_summertime_8-20_precipitation_hist_SSP370_NTCF.nc')
low_EOF     =  xr.open_dataset(data_path + 'AerchemMIP_Asia_EOF_land_summertime_20-70_precipitation_hist_SSP370_NTCF.nc')

high_pc_hist     =  high_EOF['pc_hist'].data[:, 0]
low_pc_hist      =  low_EOF['pc_hist'].data[:, 0]

high_pc_ssp      =  high_EOF['pc_ssp3'].data[:, 0]
low_pc_ssp       =  low_EOF['pc_ssp3'].data[:, 0]

high_pc_ntcf     =  high_EOF['pc_ntcf'].data[:, 0]
low_pc_ntcf      =  low_EOF['pc_ntcf'].data[:, 0]

# 2. Read the variable files
var_list         =  ['uas', 'vas', 'psl', 'rlut']
filename_raw     =  '_MJJAS_multiple_model_result.nc' # variable name + suffix = filename

# 3. lat/lon information
ref_file         =  xr.open_dataset(data_path + var_list[1] + filename_raw)
lat  =  ref_file.lat.data ; lon  =  ref_file.lon.data

# ========================================================

# ================ Calculation Function ====================
def cal_corre_pc_var(data0, pc):
    '''
        This function calculate the correlation usnig Pearson correlation between data0 and pc, in which the data0 is numpy array
    '''
    import scipy

    # Claim the array to save the correlation
    corre_array = np.zeros((len(lat), len(lon)))
    p_array     = np.zeros((len(lat), len(lon)))

    for i in range(len(lat)):
        for j in range(len(lon)):
            if np.isnan(data0[0, i, j]):
                continue
            else:
                pearson_r     = scipy.stats.pearsonr(pc, (data0[:, i, j] - np.average(data0[:, i, j])))    

                corre_array[i, j]   = pearson_r[0]
                p_array[i, j] = pearson_r[1]

    return corre_array, p_array

if __name__ == '__main__':
    ncfile = xr.Dataset()
    for vv in var_list:

        f_var = xr.open_dataset(data_path + vv + filename_raw)

        
        correlation_scenario = np.zeros((3, 2, 7, len(lat), len(lon))) # 3 means scenarios, 2 means (high, low) freq
        p_scenario           = np.zeros((3, 2, 7, len(lat), len(lon))) # 3 means scenarios, 2 means (high, low) freq

        for dd in np.linspace(0, 6, 7, dtype=int): # lead-lag correlation
            # --- high freq ---
            len_hist = 5250
            len_furt = 3900
            correlation_scenario[0, 0, dd], p_scenario[0, 0, dd] = cal_corre_pc_var(np.nanmean(f_var['hist_model'].data, axis=0)[:len_hist-1*dd*2], high_pc_hist[dd*2:])
            correlation_scenario[1, 0, dd], p_scenario[1, 0, dd] = cal_corre_pc_var(np.nanmean(f_var['ssp3_model'].data, axis=0)[:len_furt-1*dd*2], high_pc_ssp[dd*2:])
            correlation_scenario[2, 0, dd], p_scenario[2, 0, dd] = cal_corre_pc_var(np.nanmean(f_var['ntcf_model'].data, axis=0)[:len_furt-1*dd*2], high_pc_ntcf[dd*2:])

            # --- low freq ---
            correlation_scenario[0, 1, dd], p_scenario[0, 1, dd] = cal_corre_pc_var(np.nanmean(f_var['hist_model'].data, axis=0)[:len_hist-1*dd*2], low_pc_hist[dd*2:])
            correlation_scenario[1, 1, dd], p_scenario[1, 1, dd] = cal_corre_pc_var(np.nanmean(f_var['ssp3_model'].data, axis=0)[:len_furt-1*dd*2], low_pc_ssp[dd*2:])
            correlation_scenario[2, 1, dd], p_scenario[2, 1, dd] = cal_corre_pc_var(np.nanmean(f_var['ntcf_model'].data, axis=0)[:len_furt-1*dd*2], low_pc_ntcf[dd*2:])

        ncfile[vv+'_correlation'] = xr.DataArray(data=correlation_scenario, dims=["scenario", "freq", "lead_day", "lat", "lon"],
                                        coords=dict(
                                            lon=(["lon"], lon),
                                            lat=(["lat"], lat),
                                            scenario=(["scenario"], ['historical', 'ssp370', 'ssp370ntcf']),
                                            freq=(["freq"], ['high', 'low']),         
                                            lead_day=(["lead_day"], np.linspace(0, 12, 7)),
                                        ),
                                        )
        ncfile[vv+'p'] = xr.DataArray(data=p_scenario, dims=["scenario", "freq", "lead_day", "lat", "lon"],
                                        coords=dict(
                                            lon=(["lon"], lon),
                                            lat=(["lat"], lat),
                                            scenario=(["scenario"], ['historical', 'ssp370', 'ssp370ntcf']),
                                            freq=(["freq"], ['high', 'low']),
                                            lead_day=(["lead_day"], np.linspace(0, 12, 7)),
                                        ),
                                        )

        print(f'Finish {vv}')

    ncfile.to_netcdf(data_path + 'AerChemMIP_correlation_pvalue_PC_variable_uas_vas_psl_rlut.nc')

    

