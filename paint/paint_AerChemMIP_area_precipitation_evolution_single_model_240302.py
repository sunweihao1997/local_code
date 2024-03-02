'''
2024-3-2
This script is to show the area-averaged precipitation evolution in May and June from 1980 to 2050 under different scenarios

modified from paint_AerChemMIP_area_precipitation_evolution_240228.py, the difference is that this script is to see the single model's revolution
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import os
import scipy.stats as stats
import pymannkendall as mk

data_path = '/data/AerChemMIP/LLNL_download/postprocess/'
files_all = os.listdir(data_path) ; files_all.sort()

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'CESM2-WACCM', 'BCC-ESM1']

def check_ssp_timescale():
    f1 = xr.open_dataset(data_path + 'UKESM1-0-LL_SSP370NTCFCH4_r2i1p1f2.nc')

    print(f1.time.data)

def calculate_area_average(pr, extent, month_num, year_num=np.linspace(1980, 2014, 35)):
    '''
        This function return the area-averaged precip for the given extent
    '''
    #area_pr = pr.sel(lat=slice(extent[0], extent[1]), lon=slice(extent[2], extent[3]), time=pr.time.dt.month.isin([month_num])).sel(time=pr.time.dt.year.isin([year_num]))
    area_pr_month = pr.sel(lat=slice(extent[0], extent[1]), lon=slice(extent[2], extent[3]), time=pr.time.dt.month.isin([month_num]))
    area_pr_year  = area_pr_month.sel(time=area_pr_month.time.dt.year.isin([year_num]))

#    print(area_pr_year)

    avg_pr  = np.zeros(len(area_pr_year.time.data))

    for tt in range(len(area_pr_year.time.data)):
        avg_pr[tt] = np.average(area_pr_year['pr'].data[tt])

    return avg_pr

def cal_historical_evolution(extent, year_scope, mon_scope, model_name):
    # 1. Get the file list, including the historical
    historical_files = []
    for ff in files_all:
        if 'historical' in ff and ff[0] != '.' and 'CMIP6' not in ff and model_name in ff:
            historical_files.append(ff)

    # 2. Read each file and save them into array

    model_pr_array = np.zeros((len(historical_files), len(year_scope)))

    # --- Test ---
#    ftest      = xr.open_dataset(data_path + historical_files[1])
#    a = calculate_area_average(ftest, extent, 5, )
#    print(a)

    # 3. calculate each historical file and save the result
    for fff in range(len(historical_files)):
        print(f'Now it is deal with historical {historical_files[fff]}')
        f0      = xr.open_dataset(data_path + historical_files[fff])

        model_pr_array[fff] = calculate_area_average(f0, extent, mon_scope, year_scope)

    return model_pr_array

def cal_ssp370_evolution(extent, year_scope, mon_scope, model_name):
    # 1. Get the file list, including the historical
    historical_files = []
    for ff in files_all:
        if 'SSP370' in ff and ff[0] != '.' and 'CMIP6' not in ff and 'NTCF' not in ff and model_name in ff:
            historical_files.append(ff)

#    print(historical_files)
    model_pr_array = np.zeros((len(historical_files), len(year_scope)))

    # --- Test ---
#    ftest      = xr.open_dataset(data_path + historical_files[1])
#    a = calculate_area_average(ftest, extent, 5, )
#    print(a)

    # 3. calculate each historical file and save the result
    for fff in range(len(historical_files)):
        print(f'Now it is deal with SSP370 {historical_files[fff]}')
        f0      = xr.open_dataset(data_path + historical_files[fff])

        model_pr_array[fff] = calculate_area_average(f0, extent, mon_scope, year_scope)

    return model_pr_array

def cal_ssp370NTCF_evolution(extent, year_scope, mon_scope, model_name):
    # 1. Get the file list, including the historical
    historical_files = []
    for ff in files_all:
        if 'SSP370NTCF' in ff and ff[0] != '.' and 'CMIP6' not in ff and model_name in ff:
            historical_files.append(ff)


    model_pr_array = np.zeros((len(historical_files), len(year_scope)))

    # --- Test ---
#    ftest      = xr.open_dataset(data_path + historical_files[1])
#    a = calculate_area_average(ftest, extent, 5, )
#    print(a)

    # 3. calculate each historical file and save the result
    for fff in range(len(historical_files)):
        print(f'Now it is deal with SSP370NTCF {historical_files[fff]}')
        f0      = xr.open_dataset(data_path + historical_files[fff])

        model_pr_array[fff] = calculate_area_average(f0, extent, mon_scope, year_scope)

    return model_pr_array

def paint_evolution_monthly_precip(hist, ssp, sspntcf, left_string, right_string, mon_name, area_name, model_name):


#    slop_ssp370,     intercept_ssp370          =  np.polyfit(np.linspace(2015, 2050, 36), ssp370_avg - np.average(historical_avg), 1)
#    slop_ssp370ntcf, intercept_ssp370ntcf      =  np.polyfit(np.linspace(2015, 2050, 36), ssp370ntcf_avg - np.average(historical_avg), 1)
#
#    # MK trend test
#    result_ssp370     = mk.original_test(ssp370_avg - np.average(historical_avg))
#    result_ssp370ntcf = mk.original_test(ssp370ntcf_avg - np.average(historical_avg))
#
#    results           = [result_ssp370, result_ssp370ntcf]
#

    fig, ax = plt.subplots()

#    ax.plot(np.linspace(1980, 2014, 35), hist, color='grey', linewidth=0.75, alpha=0.75)

#    ax.plot(np.linspace(2015, 2050, 36), ssp,        color='lightsteelblue', linewidth=0.75, alpha=0.65)
    ax.plot(np.linspace(2015, 2050, 36), ssp - np.average(hist), color='royalblue',     linestyle='--', linewidth=0.75, alpha=0.5,)

#    ax.plot(np.linspace(2015, 2050, 36), sspntcf,        color='mistyrose', linewidth=0.75, alpha=0.75)
    ax.plot(np.linspace(2015, 2050, 36), sspntcf - np.average(hist), color='red',       linestyle='--', linewidth=0.75, alpha=0.5,)

    # Paint the member average
    ax.plot(np.linspace(2015, 2050, 36), np.average(ssp, axis=1) - np.average(hist), color='royalblue',      linewidth=1.25, alpha=1, label='SSP370')
    ax.plot(np.linspace(2015, 2050, 36), np.average(sspntcf, axis=1) - np.average(hist), color='red',       linewidth=1.25, alpha=1, label='SSP370NTCF')

    plt.legend(loc='upper left')

    ax.set_title(left_string,  loc='left',  fontsize=15)
    ax.set_title(right_string, loc='right', fontsize=15)


    plt.savefig(f"/data/paint/{mon_name}_{area_name}_{model_name}_single_model_mon_precip_deviation_trend_historical_SSP370.png", dpi=700)

if __name__ == '__main__':
    # May BOB
    extent = [5, 15, 85, 100]
    mon    = 5
    hist_model_may   = cal_historical_evolution(extent, np.linspace(1980, 2014, 35), mon, models_label[0])
    ssp370_model_may = cal_ssp370_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])
    ssp370ntcf_model_may = cal_ssp370NTCF_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])

    paint_evolution_monthly_precip(np.swapaxes(hist_model_may,0,1) * 86400, np.swapaxes(ssp370_model_may,0,1) * 86400, np.swapaxes(ssp370ntcf_model_may,0,1) * 86400, 'May', '(5-20N, 85-100E)', 'May', 'BOB', models_label[0])

    # May SCS
    extent = [5, 15, 110, 120]
    mon    = 5
    hist_model_may   = cal_historical_evolution(extent, np.linspace(1980, 2014, 35), mon, models_label[0])
    ssp370_model_may = cal_ssp370_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])
    ssp370ntcf_model_may = cal_ssp370NTCF_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])

    paint_evolution_monthly_precip(np.swapaxes(hist_model_may,0,1) * 86400, np.swapaxes(ssp370_model_may,0,1) * 86400, np.swapaxes(ssp370ntcf_model_may,0,1) * 86400, 'May', '(5-20N, 110-120E)', 'May', 'SCS', models_label[0])

    # June BOB
    extent = [5, 15, 85, 100]
    mon    = 6
    hist_model_may   = cal_historical_evolution(extent, np.linspace(1980, 2014, 35), mon, models_label[0])
    ssp370_model_may = cal_ssp370_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])
    ssp370ntcf_model_may = cal_ssp370NTCF_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])

    paint_evolution_monthly_precip(np.swapaxes(hist_model_may,0,1) * 86400, np.swapaxes(ssp370_model_may,0,1) * 86400, np.swapaxes(ssp370ntcf_model_may,0,1) * 86400, 'June', '(5-20N, 85-100E)', 'June', 'BOB', models_label[0])

    # June SCS
    extent = [5, 15, 110, 120]
    mon    = 6
    hist_model_may   = cal_historical_evolution(extent, np.linspace(1980, 2014, 35), mon, models_label[0])
    ssp370_model_may = cal_ssp370_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])
    ssp370ntcf_model_may = cal_ssp370NTCF_evolution(extent, np.linspace(2015, 2050, 36), mon, models_label[0])

    paint_evolution_monthly_precip(np.swapaxes(hist_model_may,0,1) * 86400, np.swapaxes(ssp370_model_may,0,1) * 86400, np.swapaxes(ssp370ntcf_model_may,0,1) * 86400, 'June', '(5-20N, 110-120E)', 'June', 'SCS', models_label[0])

#    # statistical test
#    t_stat, p_value = stats.ttest_ind(np.average(ssp370_model_may, axis=0), np.average(ssp370ntcf_model_may, axis=0))
#
#    print("t-statistic:", t_stat)
#    print("p-value:", p_value)
#    #check_ssp_timescale() #SSP start from 2015