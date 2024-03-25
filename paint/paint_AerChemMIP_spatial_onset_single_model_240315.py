'''
2024-3-15
This script is to plot the spatial onset for each model (total number is 7)
'''

import xarray as xr
import numpy as np
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

data_path = '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'NorESM2-LM', 'MPI-ESM-1-2-HAM', 'MIROC6', ]
model_number = int(len(models_label))

threshold0 = 3.5

def paint_onset_day_single_model():
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/home/sun/local_code/module/")
    from module_sun import set_cartopy_tick

    # set extent
    lonmin,lonmax,latmin,latmax  =  60,130,5,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # Set the colormap
    viridis = cm.get_cmap('coolwarm', 22)
    newcolors = viridis(np.linspace(0, 1, 22))
    newcmp = ListedColormap(newcolors)

    # -------   Set  figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(50,80))
    spec1   =  fig1.add_gridspec(nrows=model_number,ncols=3)

    j  =  0
    vmin = -15 ; vmax = 15

    # ------- Paint ----------------------
    for row in range(model_number):
        # Read the file
        f1 = xr.open_dataset(data_path + 'single_model_' + models_label[row] + '_onset_day_threshold' + str(threshold0) + '.nc')

        # --- Historical - SSP370 ---
        ax_hist = fig1.add_subplot(spec1[row, 0], projection = proj)

        # set ticks
        set_cartopy_tick(ax=ax_hist,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

        im  =  ax_hist.pcolormesh(f1.lon.data, f1.lat.data, 1.2*(f1['onset_hist'].data - f1['onset_ssp3'].data), cmap=newcmp, vmin=vmin, vmax=vmax)

        ax_hist.set_title(models_label[row], loc='left', fontsize=15)

        ax_hist.coastlines(resolution='50m',lw=1.65)

        # --- Historical  - SSP370NTCF ---
        ax_hist = fig1.add_subplot(spec1[row, 1], projection = proj)

        # set ticks
        set_cartopy_tick(ax=ax_hist,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

        im  =  ax_hist.pcolormesh(f1.lon.data, f1.lat.data, 1.2*(f1['onset_hist'].data - f1['onset_ntcf'].data), cmap=newcmp, vmin=vmin, vmax=vmax)

        ax_hist.set_title(models_label[row], loc='left', fontsize=15)

        ax_hist.coastlines(resolution='50m',lw=1.65)

        # --- SSP370  - SSP370NTCF ---
        ax_hist = fig1.add_subplot(spec1[row, 2], projection = proj)

        # set ticks
        set_cartopy_tick(ax=ax_hist,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

        im  =  ax_hist.pcolormesh(f1.lon.data, f1.lat.data, 1.2*(f1['onset_ssp3'].data - f1['onset_ntcf'].data), cmap=newcmp, vmin=vmin, vmax=vmax)

        ax_hist.set_title(models_label[row], loc='left', fontsize=15)

        ax_hist.coastlines(resolution='50m',lw=1.65)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    plt.savefig("/home/sun/paint/AerMIP/spatial_{}_onset_dates_multiple_model.png".format(threshold0))

def main():
    paint_onset_day_single_model()

if __name__ == '__main__':
    main()