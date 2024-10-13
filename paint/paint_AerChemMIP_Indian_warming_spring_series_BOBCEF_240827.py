'''
mac laptop
240826
This script is to compare the warming trend over the Indian continent in Mar-Apr
'''
import xarray as xr
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys

#import sys
#sys.path.append("/home/sun/local_code/module/")
#from module_sun import set_cartopy_tick

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data

def cal_multiple_model_avg(f0, exp_tag, timeaxis,):
    '''
    Because the input data is single model, so this function is to calculate the model-averaged data

    timeaxis is 65 for historical and 36 for furture simulation
    '''
    # 1. Generate the averaged array
    lat = f0.lat.data ; lon = f0.lon.data ; time = f0[timeaxis].data

    multiple_model_avg = np.zeros((len(time), len(lat), len(lon)))
    multiple_model_std = np.zeros((len(models_label), len(time), len(lat), len(lon)))

    # 2. Calculation
    models_num = len(models_label)

    j = 0
    for mm in models_label:
        varname1 = mm + '_' + exp_tag

        multiple_model_avg += (f0[varname1].data / models_num)
        multiple_model_std[j] = f0[varname1].data

        j += 1
    #
    return multiple_model_avg, multiple_model_std

def cal_student_ttest(array1, array2):
    '''
        This function is to calculate the student ttest among the array1 and array2
    '''
    from scipy import stats
    p_value = np.zeros((array1.shape[1], array2.shape[2]))

    for i in range(array1.shape[1]):
        for j in range(array2.shape[2]):
            #print(i)
            p_value[i, j] = stats.ttest_rel(array1[:, i, j], array2[:, i, j])[1]

    return p_value
# ================= File Information ====================

import pymannkendall as mk
data_path = "/home/sun/data/AerChemMIP/process/"
data_name = "multiple_model_climate_va_month_AM.nc"

f0        = xr.open_dataset(data_path + data_name).sel(lat=slice(-10, 10), lon=slice(76,85), plev=92500)
#print(f0)

ssp0_indian, ssp0_indian_std      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
#sys.exit(ssp0_indian_std.shape)
ntcf0_indian,ntcf0_indian_std     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

#f1        = xr.open_dataset(data_path + data_name).sel(lat=slice(10, 25))
##print(f0)
#
#ssp0_zonal, ssp0_zonal_std      =  cal_multiple_model_avg(f1, 'ssp',  'time_ssp')
#ntcf0_zonal, ntcf0_zonal_std    =  cal_multiple_model_avg(f1, 'sspntcf', 'time_ssp')

#ttest     =  cal_student_ttest(ssp0, ntcf0)

# =======================================================

# =============== calculation ===============
series1_indian = np.nanmean(np.nanmean(ssp0_indian, axis=1),  axis=1)
series2_indian = np.nanmean(np.nanmean(ntcf0_indian, axis=1), axis=1)
#series1_zonal  = np.nanmean(np.nanmean(ssp0_zonal, axis=1),  axis=1)
#series2_zonal  = np.nanmean(np.nanmean(ntcf0_zonal, axis=1), axis=1)

series1_indian_std = np.std(np.nanmean(np.nanmean(ssp0_indian_std, axis=2),  axis=2), axis=0)
series2_indian_std = np.std(np.nanmean(np.nanmean(ntcf0_indian_std, axis=2), axis=2) - np.nanmean(np.nanmean(ssp0_indian_std, axis=2),  axis=2), axis=0)
#print(series2_indian_std.shape)
#print(series1_indian - series1_zonal)
#print(series2_indian)


def paint_evolution_landsea_contrast(ssp, sspntcf, ssp_std, ntcf_std, left_string, right_string,):
    fig, ax = plt.subplots(figsize=(12, 10))

    # Paint the member average
#    ax.plot(np.linspace(2015, 2050, 36), ssp,     color='royalblue',      linewidth=3.25, alpha=1, label='SSP370')
    ax.plot(np.linspace(2015, 2050, 36), sspntcf - ssp, color='red',            linewidth=3.25, alpha=1, label='SSP370lowNTCF')

    # Paint the model deviation
#    ax.fill_between(np.linspace(2015, 2050, 36), ssp   + ssp_std,     ssp  - ssp_std, facecolor='royalblue', alpha=0.2)
    ax.fill_between(np.linspace(2015, 2050, 36), sspntcf  - ssp + ntcf_std, sspntcf - ssp - ntcf_std, facecolor='k', alpha=0.2)

    plt.legend(loc='lower right', fontsize=25)
    print(sspntcf - ssp)

    ax.set_title(left_string,  loc='left',  fontsize=25)
    ax.set_title(right_string, loc='right', fontsize=25)

    ax.set_ylim((-1, 1))

    plt.savefig("/Volumes/Untitled/paint/SSP370_SSP370lowNTCF_indian_tas.png", dpi=500)

    plt.close()


paint_evolution_landsea_contrast(series1_indian - series1_indian[0], series2_indian - series2_indian[0], series1_indian_std, series2_indian_std, ' ', ' ')

