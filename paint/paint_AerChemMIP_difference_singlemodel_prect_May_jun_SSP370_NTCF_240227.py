'''
2024-3-2
This script is to show the difference between the SSP370 and SSP370NTCF for the period 2031-2050,

modified from paint_AerChemMIP_difference_prect_May_jun_SSP370_NTCF_240227.py
The difference is to show the single models result
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import scipy.stats as stats
import os

data_path = '/data/AerChemMIP/LLNL_download/postprocess_samegrids/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'CESM2-WACCM', 'BCC-ESM1']
exps_label   = ['historical', 'SSP370', 'SSP370NTCF']
#exps_label   = ['SSP370', 'SSP370NTCF']

ssp370_f  = 'CMIP6_model_SSP370_monthly_precipitation_2015-2050.nc'
#sspntcf_f = 'CMIP6_model_SSP370NTCF_monthly_precipitation_2015-2050.nc'
#
f_ref     = xr.open_dataset(data_path + ssp370_f)
#
#May_ssp   = xr.open_dataset(data_path + ssp370_f).sel(time=f_ref.time.dt.month.isin([5, ]))  ; Jun_ssp   =  xr.open_dataset(data_path + ssp370_f).sel(time=f_ref.time.dt.month.isin([6, ]))
#May_NTCF  = xr.open_dataset(data_path + sspntcf_f).sel(time=f_ref.time.dt.month.isin([5, ])) ; Jun_NTCF  =  xr.open_dataset(data_path + sspntcf_f).sel(time=f_ref.time.dt.month.isin([6, ]))
#
#May_diff  = np.average(May_ssp['pr'].data[-25:], axis=0) - np.average(May_NTCF['pr'].data[-25:], axis=0)
#Jun_diff  = np.average(Jun_ssp['pr'].data[-25:], axis=0) - np.average(Jun_NTCF['pr'].data[-25:], axis=0)
#
lat       = f_ref.lat.data
lon       = f_ref.lon.data
#
#p_value_may = np.zeros(May_diff.shape)
#p_value_Jun = np.zeros(Jun_diff.shape)
#
#for i in range(len(lat)):
#    for j in range(len(lon)):
#        t_stat, p_value = stats.ttest_ind(May_ssp['pr'].data[:, i, j], May_NTCF['pr'].data[:, i, j])
#
#        p_value_may[i, j] = p_value
#
#        t_stat, p_value = stats.ttest_ind(Jun_ssp['pr'].data[:, i, j], Jun_NTCF['pr'].data[:, i, j])
#
#        p_value_Jun[i, j] = p_value

def cal_single_models_diff(model_name, exp_name, month):
    # Get the list including the model name
    list0 = os.listdir(data_path)

    model_list = []
    for ff in list0:
        if model_name in ff and '_'+exp_name+'_' in ff:
            model_list.append(ff)
        else:
            continue

    print(f'Now it is dealing with {model_name} {exp_name}, it contains {len(model_list)}')

    if 'SSP' in exp_name:
        f0 = xr.open_dataset(data_path + model_list[0])
        f0 = xr.open_dataset(data_path + model_list[0]).sel(time=f0.time.dt.year.isin(np.linspace(2015, 2050, 36)))
        f0 = f0.sel(time=f0.time.dt.month.isin([month]))
    else:
        f0 = xr.open_dataset(data_path + model_list[0])
        f0 = f0.sel(time=f0.time.dt.month.isin([month]))

    model_avg = np.zeros(f0['pr'].shape)

    for nn in range(len(model_list)):
        if 'SSP' in exp_name:
            f1 = xr.open_dataset(data_path + model_list[nn])
            f1 = xr.open_dataset(data_path + model_list[nn]).sel(time=f1.time.dt.year.isin(np.linspace(2015, 2050, 36)))
            f1 = f1.sel(time=f1.time.dt.month.isin([month]))
        else:
            f1 = xr.open_dataset(data_path + model_list[nn])
            f1 = f1.sel(time=f1.time.dt.month.isin([month]))

        model_avg += f1['pr'].data / len(model_list)

    return model_avg

def paint_pentad_circulation(hist_average, prect, p_value):
    '''This function paint pentad circulation based on b1850 experiment'''
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/root/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,-10,35
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(40,50))
    spec1   =  fig1.add_gridspec(nrows=7,ncols=3)

    j  =  0
    contour_level = np.linspace(-2.5, 2.5, 21)
    #print(len(prect))
    # ------       paint    ------------
    for row in range(7):
        # First column: SSP370
        ax = fig1.add_subplot(spec1[row,0],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')
        #print(len(prect[row]))
        im  =  ax.contourf(lon, lat, np.average(prect[row][1][-25:], axis=0) - hist_average, contour_level, cmap='coolwarm', alpha=1, extend='both')

        #sp  =  ax.contourf(lon, lat, p_value[col], levels=[0., 0.05], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(models_label[row], loc='left', fontsize=23)
        ax.set_title('SSP370', loc='right', fontsize=23)

        # ----------------------------------------------------------------------
        # Second column: SSP370lowNTCF
        ax = fig1.add_subplot(spec1[row,1],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, np.average(prect[row][2][-25:], axis=0) - hist_average, contour_level, cmap='coolwarm', alpha=1, extend='both')

        #sp  =  ax.contourf(lon, lat, p_value[col], levels=[0., 0.05], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(models_label[row], loc='left', fontsize=23)
        ax.set_title('SSP370lowNTCF', loc='right', fontsize=23)

        # ----------------------------------------------------------------------
        # Third column: NTCF mitigation
        ax = fig1.add_subplot(spec1[row,2],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, (np.average(prect[row][1][-25:], axis=0) - hist_average) - (np.average(prect[row][2][-25:], axis=0) - hist_average), contour_level, cmap='coolwarm', alpha=1, extend='both')

        #sp  =  ax.contourf(lon, lat, p_value[col], levels=[0., 0.05], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(models_label[row], loc='left', fontsize=23)
        ax.set_title('NTCF mitigation', loc='right', fontsize=23)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    plt.savefig("/data/paint/spatial_SSP370-SSP370NTCF_precip_multiple_model.png")

def main():
#    prect0 = [May_diff, Jun_diff]
#
#    p_value = [p_value_may, p_value_Jun]
#    paint_pentad_circulation(prect0, p_value)
    seven_model_three_exp = []
    month = 5
    for modell in models_label:
        hist = cal_single_models_diff(modell, exps_label[0], month)
        ssp370 = cal_single_models_diff(modell, exps_label[1], month)
        ssp370NTCF = cal_single_models_diff(modell, exps_label[2], month)

        seven_model_three_exp.append([hist * 86400, ssp370 * 86400, ssp370NTCF * 86400])

    # calculate the historical average
    hist_avg = np.zeros((121, 241))
    for i in range(7): 
        hist_avg += np.average(seven_model_three_exp[i][0][-40:], axis=0) / 7

    #print(hist_avg)
    
    #print(seven_model_three_exp[0][1].shape)
    paint_pentad_circulation(hist_avg, seven_model_three_exp, 0)


    

if __name__ == '__main__':
    main()