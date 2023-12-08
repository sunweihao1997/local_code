'''
2023-11-20
This script is to paint the trend in precipitation for the period 1900 to 1960

2023-11-22 Update:
1. Change the method for stippling, not use M-K trend test. From the advice of Massimo, when the sign among the CESM ensemble is similar, then stipple it
2. Add result of the noEU experiment
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys

sys.path.append("/Users/sunweihao/local-code/module/")
from module_sun import *

# =================== File Location =============================

file_path = '/Volumes/samssd/data/precipitation/processed/'
file_name = 'CESM_GPCC_JJAS_trend_1900_1960_significant_level.nc'

f0        = xr.open_dataset(file_path + file_name)

# ===============================================================

def paint_trend(lat, lon, trend, level, p, title_name, pic_path, pic_name):
    '''
        This function is plot the trend
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    from matplotlib import projections
    import cartopy.crs as ccrs

    # --- Set the figure ---
    proj    =  ccrs.PlateCarree()
    fig, ax =  plt.subplots(figsize=(15, 12), subplot_kw={'projection': proj})

    # --- Set range ---
    lonmin,lonmax,latmin,latmax  =  50,110,-10,40
    extent     =  [lonmin,lonmax,latmin,latmax]

    # --- Tick setting ---
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,40,6,dtype=int),nx=1,ny=1,labelsize=12.5)

    # --- Equator line ---
    ax.plot([40,120],[0,0],'k--')

    # Shading for precipitation trend
    im  =  ax.contourf(lon, lat, trend, levels=level, cmap='bwr_r', alpha=1, extend='both')

    # Stippling picture
    sp  =  ax.contourf(lon, lat, p, levels=[0.1, 1], colors='none', hatches=['..'])

    # --- Coast Line ---
    ax.coastlines(resolution='50m', lw=1.75)

    # --- title ---
    ax.set_title('mm day^-1 decade^-1', loc='right', fontsize=15)
    ax.set_title(title_name, loc='left', fontsize=15)

    # ========= add colorbar =================
    fig.subplots_adjust(top=0.8) 
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig.colorbar(im, cax=cbar_ax, shrink=0.5, pad=0.01, orientation='horizontal')
    #cb.ax.set_xticks(levels)
    #cb.ax.tick_params(labelsize=15, rotation=45)

    plt.savefig(pic_path + pic_name)

def main():
    paint_trend(
        lat=f0['lat1'].data, lon=f0['lon1'].data, trend=f0['trend_cesm'].data, p=f0['p_cesm'].data, title_name='CESM_CON', 
        level=np.linspace(-0.2, 0.2, 21), 
        pic_path='/Volumes/samssd/paint/',
        pic_name='EUI_CESM_trend_spatial_distribution_1900_1960.png'
    )

    paint_trend(
        lat=f0['lat3'].data, lon=f0['lon3'].data, trend=f0['trend_cesm2'].data, p=f0['p_cesm2'].data, title_name='CESM2_CON', 
        level=np.linspace(-0.2, 0.2, 21), 
        pic_path='/Volumes/samssd/paint/',
        pic_name='EUI_CESM2_trend_spatial_distribution_1900_1960.png'
    )

    paint_trend(
        lat=f0['lat2'].data, lon=f0['lon2'].data, trend=f0['trend_gpcc'].data, p=f0['p_gpcc'].data, title_name='GPCC', 
        level=np.linspace(-0.2, 0.2, 21), 
        pic_path='/Volumes/samssd/paint/',
        pic_name='EUI_GPCC_trend_spatial_distribution_1900_1960.png'
    )

    paint_trend(
        lat=f0['lat2'].data, lon=f0['lon2'].data, trend=f0['trend_gpcc'].data, p=f0['p_gpcc'].data, title_name='GPCC', 
        level=np.linspace(-0.6, 0.6, 13), 
        pic_path='/Volumes/samssd/paint/',
        pic_name='EUI_GPCC_trend_spatial_distribution_1900_1960.pdf'
    )

if __name__ == '__main__':
    main()