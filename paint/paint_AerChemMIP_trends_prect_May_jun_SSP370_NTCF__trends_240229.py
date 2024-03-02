'''
2024-2-29
This script is to show the spatial linear trends from different experiments and their difference
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import scipy.stats as stats

data_path = '/data/AerChemMIP/LLNL_download/postprocess_samegrids/'
data_name = 'CMIP6_model_SSP370_SSP370NTCF_month56_precipitation_trends_2015-2050.nc'

f0        = xr.open_dataset(data_path + data_name)

lat       = f0.lat.data
lon       = f0.lon.data


def paint_pentad_circulation(prect, p_value, figname):
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
    fig1    =  plt.figure(figsize=(32,20))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

    j  =  0

    left_title = ['May', 'Jun'] ; right_title = ['SSP370', 'SSP370NTCF']
    # ------       paint    ------------
    j = 0 # range 0-3
    for row in range(2):
        m = 0
        for col in range(2):
            ax = fig1.add_subplot(spec1[row,col],projection=proj)

            # 设置刻度
            set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

            # 添加赤道线
            ax.plot([40,150],[0,0],'k--')

            im  =  ax.contourf(lon, lat, 10* prect[j], np.linspace(-0.5, 0.5, 11), cmap='coolwarm', alpha=1, extend='both')

            sp  =  ax.contourf(lon, lat, p_value[j], levels=[0., 0.1], colors='none', hatches=['..'])

            # 海岸线
            ax.coastlines(resolution='10m',lw=1.65)

            ax.set_title(left_title[m], loc='left', fontsize=20.5)
            ax.set_title(right_title[row], loc='right', fontsize=20.5)

            m += 1
            j += 1

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/" + figname)

def paint_pentad_circulation_diff(prect, p_value, figname):
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
    fig1    =  plt.figure(figsize=(32,10))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=2)

    j  =  0

    # ------       paint    ------------
    ax = fig1.add_subplot(spec1[0,0],projection=proj)

    # 设置刻度
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

    # 添加赤道线
    ax.plot([40,150],[0,0],'k--')

    im  =  ax.contourf(lon, lat, 10*(prect[0] - prect[2]), np.linspace(-0.5, 0.5, 11), cmap='coolwarm', alpha=1, extend='both')

#    sp  =  ax.contourf(lon, lat, p_value[j], levels=[0., 0.1], colors='none', hatches=['..'])

    # 海岸线
    ax.coastlines(resolution='10m',lw=1.65)

    ax.set_title('May', loc='left', fontsize=20.5)
    ax.set_title('SSP370 - SSP370NTCF', loc='right', fontsize=20.5)

    # --------------------------------------------------------------

    ax = fig1.add_subplot(spec1[0,1],projection=proj)

    # 设置刻度
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

    # 添加赤道线
    ax.plot([40,150],[0,0],'k--')

    im  =  ax.contourf(lon, lat, prect[1] - prect[3], np.linspace(-0.07, 0.07, 15), cmap='coolwarm', alpha=1, extend='both')

#    sp  =  ax.contourf(lon, lat, p_value[j], levels=[0., 0.1], colors='none', hatches=['..'])

    # 海岸线
    ax.coastlines(resolution='10m',lw=1.65)

    ax.set_title('Jun', loc='left', fontsize=20.5)
    ax.set_title('SSP370 - SSP370NTCF', loc='right', fontsize=20.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/" + figname)

def main():
    prect0 = [f0['pr_trend_May_SSP370'].data, f0['pr_trend_Jun_SSP370'].data, f0['pr_trend_May_SSP370NTCF'].data, f0['pr_trend_Jun_SSP370NTCF'].data,]

    p_value = [f0['p_trend_May_SSP370'].data, f0['p_trend_Jun_SSP370'].data, f0['p_trend_May_SSP370NTCF'].data, f0['p_trend_Jun_SSP370NTCF'].data,]
    paint_pentad_circulation(prect0, p_value, "SSP370_SSP370NTCF_May_June_trends_precip.png")
    paint_pentad_circulation_diff(prect0, p_value, "SSP370_SSP370NTCF_diff_May_June_trends_precip.png")

if __name__ == '__main__':
    main()