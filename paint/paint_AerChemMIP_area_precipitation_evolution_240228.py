'''
2024-2-28
This script is to show the area-averaged precipitation evolution in May and June from 1980 to 2050 under different scenarios
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

data_path = '/data/AerChemMIP/LLNL_download/postprocess_samegrids/'
files_all = os.listdir(data_path) ; files_all.sort()

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

def cal_historical_evolution(extent, year_scope, mon_scope):
    # 1. Get the file list, including the historical
    historical_files = []
    for ff in files_all:
        if 'historical' in ff and ff[0] != '.' and 'CMIP6' not in ff:
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

def cal_ssp370_evolution(extent, year_scope, mon_scope):
    # 1. Get the file list, including the historical
    historical_files = []
    for ff in files_all:
        if 'SSP370' in ff and ff[0] != '.' and 'CMIP6' not in ff and 'NTCF' not in ff:
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

def cal_ssp370NTCF_evolution(extent, year_scope, mon_scope):
    # 1. Get the file list, including the historical
    historical_files = []
    for ff in files_all:
        if 'SSP370NTCF' in ff and ff[0] != '.' and 'CMIP6' not in ff:
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

def paint_evolution_monthly_precip(hist, ssp, sspntcf, left_string, right_string):

    historical_avg       = np.average(hist, axis=1)
    ssp370_avg           = np.average(ssp, axis=1)
    ssp370ntcf_avg      = np.average(sspntcf, axis=1)


    slop_ssp370,     intercept_ssp370          =  np.polyfit(np.linspace(2015, 2050, 36), ssp370_avg - np.average(historical_avg), 1)
    slop_ssp370ntcf, intercept_ssp370ntcf      =  np.polyfit(np.linspace(2015, 2050, 36), ssp370ntcf_avg - np.average(historical_avg), 1)

    ssp370_avg          = np.insert(ssp370_avg, 0, historical_avg[-1])
    ssp370ntcf_avg      = np.insert(ssp370ntcf_avg, 0, historical_avg[-1])

    # MK trend test
    result_ssp370     = mk.original_test(ssp370_avg - np.average(historical_avg))
    result_ssp370ntcf = mk.original_test(ssp370ntcf_avg - np.average(historical_avg))

    results           = [result_ssp370, result_ssp370ntcf]


    fig, ax = plt.subplots()

#    ax.plot(np.linspace(1980, 2014, 35), hist, color='grey', linewidth=0.75, alpha=0.75)
    ax.plot(np.linspace(1980, 2014, 35), historical_avg - np.average(historical_avg), color='black', linewidth=1.75, alpha=1, label='historical')

#    ax.plot(np.linspace(2015, 2050, 36), ssp,        color='lightsteelblue', linewidth=0.75, alpha=0.65)
    ax.plot(np.linspace(2014, 2050, 37), ssp370_avg - np.average(historical_avg), color='royalblue',      linewidth=1.75, alpha=1, label='SSP370')

#    ax.plot(np.linspace(2015, 2050, 36), sspntcf,        color='mistyrose', linewidth=0.75, alpha=0.75)
    ax.plot(np.linspace(2014, 2050, 37), ssp370ntcf_avg - np.average(historical_avg), color='red',       linewidth=1.75, alpha=1, label='SSP370NTCF')

    # Plot the linear trend
    ax.plot(np.linspace(2014, 2050, 37), slop_ssp370*np.linspace(2014, 2050, 37) + intercept_ssp370, color='royalblue', linestyle='--', linewidth=1.75, alpha=1,)
    ax.plot(np.linspace(2014, 2050, 37), slop_ssp370ntcf*np.linspace(2014, 2050, 37) + intercept_ssp370ntcf, color='red', linestyle='--', linewidth=1.75, alpha=1,)

    plt.legend(loc='lower left')

    ax.set_title(left_string,  loc='left',  fontsize=15)
    ax.set_title(right_string, loc='right', fontsize=15)

    # Add text
    font = {'family': 'serif',
        'color':  'royalblue',
        'weight': 'normal',
        'size': 11,
        }

#    print(result_ssp370.p)
#    print(round(result_ssp370.p, 3))
    ax.text(1980, 0.85, "MK-trend p-value: "+str(round(result_ssp370.p, 3)), fontdict=font, zorder=10)

    font = {'family': 'serif',
        'color':  'red',
        'weight': 'normal',
        'size': 11,
        }
    ax.text(1980, 0.65, "MK-trend p-value: "+str(round(result_ssp370ntcf.p, 3)), fontdict=font, zorder=10)
    #plt.text(2, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict=font)

    plt.savefig("/data/paint/June_SCS_mon_precip_deviation_trend_historical_SSP370.png", dpi=700)

if __name__ == '__main__':
    extent = [5, 20, 110, 120]
    mon    = 6
    hist_model_may   = cal_historical_evolution(extent, np.linspace(1980, 2014, 35), mon)
    ssp370_model_may = cal_ssp370_evolution(extent, np.linspace(2015, 2050, 36), mon)
    ssp370ntcf_model_may = cal_ssp370NTCF_evolution(extent, np.linspace(2015, 2050, 36), mon)

    paint_evolution_monthly_precip(np.swapaxes(hist_model_may,0,1) * 86400, np.swapaxes(ssp370_model_may,0,1) * 86400, np.swapaxes(ssp370ntcf_model_may,0,1) * 86400, 'June', '(5-20N, 110-120E)')

    # statistical test
    t_stat, p_value = stats.ttest_ind(np.average(ssp370_model_may, axis=0), np.average(ssp370ntcf_model_may, axis=0))

    print("t-statistic:", t_stat)
    print("p-value:", p_value)
    #check_ssp_timescale() #SSP start from 2015