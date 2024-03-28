'''
2024-3-28
This script is to plot the difference in the rainy-season precipitation between SSP370 and SSP370lowNTCF
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import scipy.stats as stats 

file_name = 'modelmean_total_precip_rainy_season_diff_SSP370_SSP370lowNTCF.nc'
file_path = '/home/sun/data/process/analysis/AerChem/'

file0     = xr.open_dataset(file_path + file_name)

lat       = file0.lat.data
lon       = file0.lon.data

def paint_diff_precip(total, intensity):
    '''
        This function plot two pictures, the first is the total rain falling into the rainy season, the second is intensity of rain
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/home/sun/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,10,45
    extent     =  [lonmin,lonmax,latmin,latmax]

    fig, (ax1, ax2) = plt.subplots(figsize=(32, 12), nrows=2, subplot_kw={'projection': ccrs.PlateCarree()})

    set_cartopy_tick(ax=ax1,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

    im  =  ax1.contourf(lon, lat, total, np.linspace(-140, 140, 15), cmap='coolwarm_r', alpha=1, extend='both')

    fig.colorbar(im, ax=ax1, location='right', anchor=(0, 0.3), shrink=0.7)

    ax1.coastlines(resolution='10m',lw=1.65)

    ax1.set_title('total rain', loc='left', fontsize=20.5)
    ax1.set_title('SSP370 - SSP370lowNTCF', loc='right', fontsize=20.5)


    # ---- intensity ----
    im2  =  ax2.contourf(lon, lat, intensity, np.linspace(-1, 1, 21), cmap='coolwarm_r', alpha=1, extend='both')

    fig.colorbar(im2, ax=ax2, location='right', anchor=(0, 0.3), shrink=0.7)

    set_cartopy_tick(ax=ax2,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

    ax2.coastlines(resolution='10m',lw=1.65)

    ax2.set_title('intensity of rain (mm/day)', loc='left', fontsize=20.5)
    ax2.set_title('SSP370 - SSP370lowNTCF', loc='right', fontsize=20.5)

    # save figure
    plt.savefig("/home/sun/paint/AerMIP/precipitation_in_rainy_season_difference_model_mean.png")

paint_diff_precip(file0['rain_change_total_modelmean'].data, file0['rain_change_intensity_modelmean'].data)