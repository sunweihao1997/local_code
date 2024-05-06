'''
2024-5-2
This script is to plot the EOF result for the 8-20 and 20-70 bandpass results
'''

import xarray as xr
import numpy as np

# ========= File Information ==========

data_path  =  '/home/sun/data/process/analysis/AerChem/'

high_EOF    =  xr.open_dataset(data_path + 'AerchemMIP_Asia_EOF_land_summertime_8-20_precipitation_hist_SSP370_NTCF.nc')
low_EOF     =  xr.open_dataset(data_path + 'AerchemMIP_Asia_EOF_land_summertime_20-70_precipitation_hist_SSP370_NTCF.nc')

lon        =  low_EOF.lon.data ; lat      =  low_EOF.lat.data

# =====================================

varname    =  'ntcf' # Modify this variable to change which result to plot

# ========= Painting Part =============

def plot_change_hw_day(high_frq, low_frq, left_string, figname, lon, lat, ct_level=np.linspace(-1., 1., 11)):
    '''
    This function is to plot the changes in the wet day among the SSP370 and SSP370lowNTCF

    This figure contains three subplot: 1. changes between SSP370 and historical 2. changes between SSP370lowNTCF and historical 3. NTCF mitigation (ssp370 - ssp370lowNTCF)
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    import sys
    sys.path.append("/home/sun/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  60,140,0,60
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(40,20))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=1)

    left_title = '{} '.format(left_string)
    right_title= ['8-20 days', '20-70 days']

    pet        = [high_frq, low_frq]


    # ------      paint    -----------
    for row in range(2):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(60,140,9,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

        im  =  ax.contourf(lon, lat, pet[row][0], ct_level, cmap='coolwarm', alpha=1, extend='both')

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)


        # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/home/sun/paint/AerMIP/AerChemMIP_EOF1_MJJAS_{}.png".format(figname))

if __name__ == '__main__':

    # Plot
    plot_change_hw_day(high_frq=high_EOF['eof1_'+varname], low_frq=low_EOF['eof1_'+varname], left_string='EOF1', figname=varname, lon=lon, lat=lat, ct_level=np.linspace(-0.8, 0.8, 17))