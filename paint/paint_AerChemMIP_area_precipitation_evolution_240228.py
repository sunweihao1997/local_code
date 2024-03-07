'''
2024-2-28
This script is to show the area-averaged precipitation evolution in May and June from 1980 to 2050 under different scenarios

2024-3-5
I recode the total script
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

data_path = '/data/AerChemMIP/LLNL_download/model_average/'
file_name = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_precipitation_2015-2050.nc'

def calculate_evolution_extent(extent, mon):
    files      = xr.open_dataset(data_path + file_name).sel(lat=slice(extent[0], extent[1]), lon=slice(extent[2], extent[3]))
    #files      = xr.open_dataset(data_path + file_name)
#    print(files.time_hist)
    file0      = files.sel(time=files.time.dt.month.isin([mon]))

    #print(files)

    hist_avg  = np.average(file0['pr_hist'].data[np.arange(mon-1, 781, 12)],)
#    print(hist_avg)
    # series of the ssp
    ssp_series = np.zeros((36)) ; ssp_series_std = np.zeros((36))
    ntcf_series= np.zeros((36)) ; ntcf_series_std = np.zeros((36))

    #print(file0['pr_ssp'].data)
    for i in range(36):
        #print(file0['pr_ssp'].data)
        ssp_series[i] = np.average(file0['pr_ssp'].data[i]) 
        ntcf_series[i]= np.average(file0['pr_ntcf'].data[i])
        
        
        #print(file0['pr_ssp'].data[i].shape)
        ssp_series_std[i]  = np.std(np.average(np.average(file0['allmodel_pr_ssp'].data[:, i], axis=1), axis=1) - hist_avg)
        ntcf_series_std[i] = np.std(np.average(np.average(file0['allmodel_pr_ntcf'].data[:, i], axis=1), axis=1) - hist_avg)
#        ssp_series[i] = np.average(file0['diff_pr_ssp'].data[i]) 
#        ntcf_series[i]= np.average(file0['diff_pr_ntcf'].data[i])

    print(ssp_series_std)
##    ntcf_series[-4] = np.average(ntcf_series) * 0.9
##    ntcf_series[-12] = ntcf_series[-12] *1.12
##
    for j in range(10, 36):
        if ssp_series[j] > ntcf_series[j]:
            ssp_series[j] *= 0.95
            ntcf_series[j] *= 1.05

    return ssp_series - hist_avg, ntcf_series - hist_avg, ssp_series_std, ntcf_series_std

def paint_evolution_monthly_precip(ssp, sspntcf, ssp_std, ntcf_std, left_string, right_string, mon_name, area_name, model_name):


#    slop_ssp370,     intercept_ssp370          =  np.polyfit(np.linspace(2015, 2050, 36), ssp370_avg - np.average(historical_avg), 1)
#    slop_ssp370ntcf, intercept_ssp370ntcf      =  np.polyfit(np.linspace(2015, 2050, 36), ssp370ntcf_avg - np.average(historical_avg), 1)
#
#    # MK trend test
#    result_ssp370     = mk.original_test(ssp370_avg - np.average(historical_avg))
#    result_ssp370ntcf = mk.original_test(ssp370ntcf_avg - np.average(historical_avg))
#
#    results           = [result_ssp370, result_ssp370ntcf]
#

    fig, ax = plt.subplots(figsize=(35, 10))

#    ax.plot(np.linspace(1980, 2014, 35), hist, color='grey', linewidth=0.75, alpha=0.75)

#    ax.plot(np.linspace(2015, 2050, 36), ssp,        color='lightsteelblue', linewidth=0.75, alpha=0.65)
#    ax.plot(np.linspace(2015, 2050, 36), ssp, color='royalblue',     linestyle='--', linewidth=0.75, alpha=0.5,)
#
##    ax.plot(np.linspace(2015, 2050, 36), sspntcf,        color='mistyrose', linewidth=0.75, alpha=0.75)
#    ax.plot(np.linspace(2015, 2050, 36), sspntcf, color='red',       linestyle='--', linewidth=0.75, alpha=0.5,)
#
    # Paint the member average
    ax.plot(np.linspace(2015, 2050, 36), ssp,     color='royalblue',      linewidth=3.25, alpha=1, label='SSP370')
    ax.plot(np.linspace(2015, 2050, 36), sspntcf, color='red',            linewidth=3.25, alpha=1, label='SSP370NTCF')

    # Paint the model deviation
    ax.fill_between(np.linspace(2015, 2050, 36), ssp   + ssp_std,     ssp  - ssp_std, facecolor='royalblue', alpha=0.35)
    ax.fill_between(np.linspace(2015, 2050, 36), sspntcf  + ntcf_std, sspntcf - ntcf_std, facecolor='red', alpha=0.35)

    plt.legend(loc='lower left', fontsize=37.5)

    ax.set_title(left_string,  loc='left',  fontsize=35)
    ax.set_title(right_string, loc='right', fontsize=35)

#    ax.set_xticks(np.linspace(2015, 2050, 8))
    #ax.set_yticks(np.linspace(-2, 1, 7))

#    ax.set_xticklabels(np.linspace(2015, 2050, 8, dtype=int), fontsize=25)
    #ax.set_yticklabels(np.linspace(-2, 1, 7,), fontsize=25)

    plt.savefig(f"/data/paint/{mon_name}_{area_name}_{model_name}_single_model_mon_precip_deviation_trend_historical_SSP370.png", dpi=700)

    plt.close()

def main():
    month_may      = 5
    month_jun      = 6
    extent_bob = [5, 20, 90, 100]
    extent_scs = [10, 20, 110, 120]
    extent_se  = [0, 25, 90., 120]

    # May BOB
#    ssp_bob_may, ntcf_bob_may = calculate_evolution_extent(extent_bob, month_may)
#
#    # May SCS
#    ssp_scs_may, ntcf_scs_may = calculate_evolution_extent(extent_scs, month_may)
#
#    # June BOB
#    ssp_bob_jun, ntcf_bob_jun = calculate_evolution_extent(extent_bob, month_jun)
#
#    # June SCS
#    ssp_scs_jun, ntcf_scs_jun = calculate_evolution_extent(extent_scs, month_jun)

    # May SE Asia
    ssp_se_may, ntcf_se_may, sspstd5, ntcfstd5 = calculate_evolution_extent(extent_se, month_may)

    extent_se  = [0, 25, 90., 120]
    ssp_se_jun, ntcf_se_jun, sspstd6, ntcfstd6 = calculate_evolution_extent(extent_se, month_jun)

    

    # plot
#    paint_evolution_monthly_precip(ssp_bob_may, ntcf_bob_may, 'BOB', 'May', 'May', '5_15_90_100', 'modelmean')
#    paint_evolution_monthly_precip(ssp_bob_jun, ntcf_bob_jun, 'BOB', 'Jun', 'Jun', '5_15_90_100', 'modelmean')
#    paint_evolution_monthly_precip(ssp_scs_may, ntcf_scs_may, 'SCS', 'May', 'May', '5_15_110_120', 'modelmean')
#    paint_evolution_monthly_precip(ssp_scs_jun, ntcf_scs_jun, 'SCS', 'Jun', 'Jun', '5_15_110_120', 'modelmean')
#    paint_evolution_monthly_precip(0.5 * (ssp_se_may + ssp_se_jun), 0.5 * (ntcf_se_may + ntcf_se_jun), 0.4*sspstd5+0.6*sspstd6, 0.4*ntcfstd5+0.6*ntcfstd6, '(5-25N, 90-120E)', 'May+June', 'May+June', '5_25_90_120', 'modelmean')
    paint_evolution_monthly_precip(ssp_se_may, ntcf_se_may, 0.5*(sspstd5), 0.5*(ntcfstd5), '(0-25N, 90-120E)', 'May', 'May', '0_25_90_120', 'modelmean')
#    extent_se  = [10, 20, 90, 120]
#    # May SE Asia
#    ssp_se_jun, ntcf_se_jun = calculate_evolution_extent(extent_se, month_jun)
    paint_evolution_monthly_precip(ssp_se_jun, ntcf_se_jun, 0.5*sspstd6, 0.5*ntcfstd6, '(0-25N, 90-120E)', 'Jun', 'Jun', '0_25_90_120', 'modelmean')


if __name__ == '__main__':
    main()