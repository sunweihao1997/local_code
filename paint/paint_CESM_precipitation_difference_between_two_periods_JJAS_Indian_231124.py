'''
2023-11-27
This script is to plot the difference between two period using the data from the CESM output
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys

module_path = "/home/sun/local_code/module"
sys.path.append(module_path)
from module_sun import *

f0 = xr.open_dataset("/mnt/d/samssd/precipitation/processed/EUI_CESM_fixEU_precipitation_difference_period_1901_1960_JJAS.nc")


def plot_diff_rainfall(extent):
    '''This function plot the difference in precipitation'''
    # ------------ 2. Paint the Pic --------------------------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    # 2.2 Set the figure
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(15,12))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    #levels  =  np.linspace(-1.2, 1.2, 25)
    levels = np.array([-1.8, -1.5, -1.2, -0.9, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.2, 1.5, 1.8])


    # ------------ First. Paint the All forcing picture ------------
    ax1 = fig1.add_subplot(spec1[0, 0], projection=proj)

    # Tick setting
    set_cartopy_tick(ax=ax1,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,40,6,dtype=int),nx=1,ny=1,labelsize=25)

    # Equator line
    ax1.plot([40,120],[0,0],'k--')

    # Set ylabel name
    ax1.set_ylabel('Fix_EU', fontsize=25)

    # Set title
    ax1.set_title('1941to1960 - 1901to1921', fontsize=25)

    # Shading for precipitation
    im1  =  ax1.contourf(f0['lon'].data, f0['lat'].data, np.average(f0['JJAS_prect_diff'], axis=0), levels=levels, cmap='bwr_r', alpha=1, extend='both')

    dot  =  ax1.contourf(f0['lon'].data, f0['lat'].data, f0['sign'], levels=[0.1, 1], colors='none', hatches=['.'])

    # Coast Line
    ax1.coastlines(resolution='110m', lw=1.75)

    # ========= add colorbar =================
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im1, cax=cbar_ax, shrink=0.5, pad=0.01, orientation='horizontal')
    cb.ax.set_xticks([-1.8, -1.5, -1.2, -0.9, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.2, 1.5, 1.8])
    cb.ax.tick_params(labelsize=15, rotation=45)

    plt.savefig('/mnt/d/samssd/paint/EUI_CESM_fixEU_precipitation_difference_1900_1960_stippling.pdf', dpi=500)

lonmin,lonmax,latmin,latmax  =  40,115,-10,40
extent     =  [lonmin,lonmax,latmin,latmax]

plot_diff_rainfall(extent)