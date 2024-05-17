'''
2024-5-9
This script is to calculate the correlation between pc1 and other variables (uas, vas, psl, rlut)
'''
import xarray as xr
import numpy as np
from statsmodels.tsa.stattools import acf, ccf
from scipy import stats

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

def auto_correlations_effective_n_bhfunc(data0, pc, k):
    auto_corr_data = acf(data0, nlags=np.abs(k), fft=True)[np.abs(k)]
    auto_corr_pc   = acf(pc, nlags=np.abs(k), fft=True)[np.abs(k)]

    
    n = len(data0)
    #print(auto_corr_data[1:]*auto_corr_pc[1:])

    effective_n = n * (1- auto_corr_data*auto_corr_pc) / (1 + auto_corr_data*auto_corr_pc)

    #print(effective_n)

    return effective_n

def auto_correlations_effective_n_fisherfunc(data0, pc, k):
    
    n = len(data0)

    effective_n = n - 3

    #print(effective_n)
    return effective_n

# ================ Calculation Function ====================
def cal_corre_pc_var(data0, pc, k):
    '''
        This function calculate the correlation usnig Pearson correlation between data0 and pc, in which the data0 is numpy array
    '''
    import scipy

    # Claim the array to save the correlation
    corre_array = np.zeros((len(lat), len(lon)))
    p_array     = np.zeros((len(lat), len(lon)))
    p_array_bh  = np.zeros((len(lat), len(lon))) # remove the autocorrelation
    p_array_fi  = np.zeros((len(lat), len(lon))) # remove the autocorrelation

    length = len(data0[:, 50, 50])
    for i in range(len(lat)):
        for j in range(len(lon)):
            if np.isnan(data0[0, i, j]):
                continue
            else:
                # rearray the variable
                
                data1  = data0[:, i, j]
                pc1    = pc[:]

                # Calculate the 11 times lead-lag autocorrelation
                #print(data1.shape)
                #print(pc1.shape)
                
                #print(pc.shape)
                #print(data0[:, i, j].shape)
                #print(pc.shape)
                #print(data1.shape)
                pearson_r     = scipy.stats.pearsonr(pc, data0[:, i, j])    

                # Calculate the new-p
                if k != 6:
                    if k<6:
                        lag = 12 + 2 * k
                    elif k>6:
                        lag = 2 * k - 12


                    # Calculate the t-statistics
                    auto_correlations_effective_n_bh      = auto_correlations_effective_n_bhfunc(data1, pc1, lag)
                    auto_correlations_effective_n_fisher  = auto_correlations_effective_n_fisherfunc(data1, pc1, lag)

                    t_bh          = pearson_r[0] * np.sqrt((auto_correlations_effective_n_bh - 2) / (1 - pearson_r[0]**2))
                    t_fi          = pearson_r[0] * np.sqrt((auto_correlations_effective_n_fisher - 2) / (1 - pearson_r[0]**2))

                    p_array_bh[i, j] = 2 * stats.t.sf(np.abs(t_bh), auto_correlations_effective_n_bh - 2)
                    p_array_fi[i, j] = 2 * stats.t.sf(np.abs(t_fi), auto_correlations_effective_n_fisher - 2)

                else:
                    p_array_bh[i, j] = pearson_r[1]
                    p_array_fi[i, j] = pearson_r[1]


                corre_array[i, j]   = pearson_r[0]
                p_array[i, j] = pearson_r[1]

                #print(pearson_r[1])

    return corre_array, p_array, p_array_bh, p_array_fi

if __name__ == '__main__':
    ncfile = xr.Dataset()
    for vv in var_list:

        f_var = xr.open_dataset(data_path + vv + filename_raw)

        
        correlation_scenario = np.zeros((3, 2, 13, len(lat), len(lon))) # 3 means scenarios, 2 means (high, low) freq, 11 is 12days (6 times) before, 0 day (1 time) and 12 days after (6 times)
        p_scenario           = np.zeros((3, 2, 13, len(lat), len(lon))) # 3 means scenarios, 2 means (high, low) freq, 11 is 12days (6 times) before, 0 day (1 time) and 12 days after (6 times)
        p_scenario_cali1     = np.zeros((3, 2, 13, len(lat), len(lon)))
        p_scenario_cali2     = np.zeros((3, 2, 13, len(lat), len(lon)))

        dd=13
        len_hist = 5250
        len_furt = 3900
        #print(auto_correlations_effective_n(np.nanmean(f_var['hist_model'].data, axis=0)[:len_hist-1*dd*2, 50, 50], high_pc_hist[dd*2:], 20))

        # Note here also involves the days after 0 day, thus the autocorrelation should be set on the 8 days after the zeros day
        # So, before the calculation I move the array to initialize the two series with 8 days lag
        for dd in np.linspace(0, 12, 13, dtype=int): # lead-lag correlation
            # --- high freq ---
            len_hist = 5250
            len_furt = 3900

            #print()
            correlation_scenario[0, 0, dd], p_scenario[0, 0, dd], p_scenario_cali1[0, 0, dd], p_scenario_cali2[0, 0, dd] = cal_corre_pc_var(np.nanmean(f_var['hist_model'].data[:, 12:len_hist-12], axis=0), high_pc_hist[2 * dd:len_hist - 24 + 2*dd],  dd*2)
            correlation_scenario[1, 0, dd], p_scenario[1, 0, dd], p_scenario_cali1[1, 0, dd], p_scenario_cali2[1, 0, dd] = cal_corre_pc_var(np.nanmean(f_var['ssp3_model'].data[:, 12:len_furt-12], axis=0), high_pc_ssp[ 2 *  dd:len_furt - 24 + 2*dd],  dd*2)
            correlation_scenario[2, 0, dd], p_scenario[2, 0, dd], p_scenario_cali1[2, 0, dd], p_scenario_cali2[2, 0, dd] = cal_corre_pc_var(np.nanmean(f_var['ntcf_model'].data[:, 12:len_furt-12], axis=0), high_pc_ntcf[2 * dd:len_furt - 24 + 2*dd],  dd*2)

            # --- low freq ---
            correlation_scenario[0, 1, dd], p_scenario[0, 1, dd], p_scenario_cali1[0, 1, dd], p_scenario_cali2[0, 1, dd]  = cal_corre_pc_var(np.nanmean(f_var['hist_model'].data[:, 12:len_hist-12], axis=0), low_pc_hist[2 * dd:len_hist - 24 + 2*dd],  dd*2)
            correlation_scenario[1, 1, dd], p_scenario[1, 1, dd], p_scenario_cali1[1, 1, dd], p_scenario_cali2[1, 1, dd]  = cal_corre_pc_var(np.nanmean(f_var['ssp3_model'].data[:, 12:len_furt-12], axis=0), low_pc_ssp[2 *  dd:len_furt - 24 + 2*dd],  dd*2)
            correlation_scenario[2, 1, dd], p_scenario[2, 1, dd], p_scenario_cali1[2, 1, dd], p_scenario_cali2[2, 1, dd]  = cal_corre_pc_var(np.nanmean(f_var['ntcf_model'].data[:, 12:len_furt-12], axis=0), low_pc_ntcf[2 * dd:len_furt - 24 + 2*dd],  dd*2)

        ncfile[vv+'_correlation'] = xr.DataArray(data=correlation_scenario, dims=["scenario", "freq", "lead_day", "lat", "lon"],
                                        coords=dict(
                                            lon=(["lon"], lon),
                                            lat=(["lat"], lat),
                                            scenario=(["scenario"], ['historical', 'ssp370', 'ssp370ntcf']),
                                            freq=(["freq"], ['high', 'low']),         
                                            lead_day=(["lead_day"], np.linspace(0, 24, 13)),
                                        ),
                                        )
        ncfile[vv+'p'] = xr.DataArray(data=p_scenario, dims=["scenario", "freq", "lead_day", "lat", "lon"],
                                        coords=dict(
                                            lon=(["lon"], lon),
                                            lat=(["lat"], lat),
                                            scenario=(["scenario"], ['historical', 'ssp370', 'ssp370ntcf']),
                                            freq=(["freq"], ['high', 'low']),
                                            lead_day=(["lead_day"], np.linspace(0, 24, 13)),
                                        ),
                                        )
        ncfile[vv+'p_bh'] = xr.DataArray(data=p_scenario_cali1, dims=["scenario", "freq", "lead_day", "lat", "lon"],
                                        coords=dict(
                                            lon=(["lon"], lon),
                                            lat=(["lat"], lat),
                                            scenario=(["scenario"], ['historical', 'ssp370', 'ssp370ntcf']),
                                            freq=(["freq"], ['high', 'low']),
                                            lead_day=(["lead_day"], np.linspace(0, 24, 13)),
                                        ),
                                        )
        ncfile[vv+'p_fi'] = xr.DataArray(data=p_scenario_cali2, dims=["scenario", "freq", "lead_day", "lat", "lon"],
                                        coords=dict(
                                            lon=(["lon"], lon),
                                            lat=(["lat"], lat),
                                            scenario=(["scenario"], ['historical', 'ssp370', 'ssp370ntcf']),
                                            freq=(["freq"], ['high', 'low']),
                                            lead_day=(["lead_day"], np.linspace(0, 24, 13)),
                                        ),
                                        )

        print(f'Finish {vv}')

    ncfile.to_netcdf(data_path + 'AerChemMIP_correlation_pvalue_PC_variable_uas_vas_psl_rlut_autocaliberate.nc')

    

