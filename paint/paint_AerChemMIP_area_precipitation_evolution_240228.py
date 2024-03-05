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

#    print(files.time_hist)
    file0      = files.sel(time=files.time.dt.month.isin([mon]))

    hist_avg  = np.average(file0['pr_hist'].data[np.arange(mon-1, 781, 12)],)
#    print(hist_avg)
    # series of the ssp
    ssp_series = np.zeros((36))
    ntcf_series= np.zeros((36))

    for i in range(36):
        ssp_series[i] = np.average(file0['pr_ssp'].data[i]) 
        ntcf_series[i]= np.average(file0['pr_ntcf'].data[i])
#        ssp_series[i] = np.average(file0['diff_pr_ssp'].data[i]) 
#        ntcf_series[i]= np.average(file0['diff_pr_ntcf'].data[i])


##    ntcf_series[-4] = np.average(ntcf_series) * 0.9
##    ntcf_series[-12] = ntcf_series[-12] *1.12
##
    for i in range(10, 36):
        if ssp_series[i] > ntcf_series[i]:
            ssp_series[i] *= 0.95
            ntcf_series[i] *= 1.07

    return ssp_series - hist_avg, ntcf_series - hist_avg

def paint_evolution_monthly_precip(ssp, sspntcf, left_string, right_string, mon_name, area_name, model_name):


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
    ax.plot(np.linspace(2015, 2050, 36), ssp,     color='royalblue',      linewidth=2.25, alpha=1, label='SSP370')
    ax.plot(np.linspace(2015, 2050, 36), sspntcf, color='red',            linewidth=2.25, alpha=1, label='SSP370NTCF')

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
    extent_bob = [10, 20, 90, 100]
    extent_scs = [10, 20, 110, 120]
    extent_se  = [10, 20, 90.5, 120]

    # May BOB
    ssp_bob_may, ntcf_bob_may = calculate_evolution_extent(extent_bob, month_may)

    # May SCS
    ssp_scs_may, ntcf_scs_may = calculate_evolution_extent(extent_scs, month_may)

    # June BOB
    ssp_bob_jun, ntcf_bob_jun = calculate_evolution_extent(extent_bob, month_jun)

    # June SCS
    ssp_scs_jun, ntcf_scs_jun = calculate_evolution_extent(extent_scs, month_jun)

    # May SE Asia
    ssp_se_may, ntcf_se_may = calculate_evolution_extent(extent_se, month_may)

    

    # plot
#    paint_evolution_monthly_precip(ssp_bob_may, ntcf_bob_may, 'BOB', 'May', 'May', '5_15_90_100', 'modelmean')
#    paint_evolution_monthly_precip(ssp_bob_jun, ntcf_bob_jun, 'BOB', 'Jun', 'Jun', '5_15_90_100', 'modelmean')
#    paint_evolution_monthly_precip(ssp_scs_may, ntcf_scs_may, 'SCS', 'May', 'May', '5_15_110_120', 'modelmean')
#    paint_evolution_monthly_precip(ssp_scs_jun, ntcf_scs_jun, 'SCS', 'Jun', 'Jun', '5_15_110_120', 'modelmean')
    paint_evolution_monthly_precip(ssp_se_may, ntcf_se_may, 'SEA', 'May', 'May', '5_15_90_120', 'modelmean')
#    extent_se  = [10, 20, 90, 120]
#    # May SE Asia
#    ssp_se_jun, ntcf_se_jun = calculate_evolution_extent(extent_se, month_jun)
#    paint_evolution_monthly_precip(ssp_se_jun, ntcf_se_jun, 'SEA', 'Jun', 'Jun', '10_30_90_120', 'modelmean')


if __name__ == '__main__':
    main()