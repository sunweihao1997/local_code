'''
2023-12-1
This script is to paint wave activity fot CESM BTAL experiment, period is 1940 to 1960, JJAS
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys

sys.path.append("/Users/sunweihao/local-code/module/")
from module_sun import *

from cartopy.util import add_cyclic_point

# ========================== File location =================================

path_src0  = '/Volumes/samssd/data/wave_activity/CESM_BTAL_1900_1920/'
path_src   = '/Volumes/samssd/data/wave_activity/CESM_BTAL_1940_1960/'

file_src_x0 = 'TN2001-Fx.monthly.1900_1920.nc'
file_src_y0 = 'TN2001-Fy.monthly.1900_1920.nc'
file_src_x  = 'TN2001-Fx.monthly.1940_1960.nc'
file_src_y  = 'TN2001-Fy.monthly.1940_1960.nc'

fx_1        = xr.open_dataset(path_src0 + file_src_x0).sel(level=200)
fy_1        = xr.open_dataset(path_src0 + file_src_y0).sel(level=200)
fx_2        = xr.open_dataset(path_src + file_src_x).sel(level=200)
fy_2        = xr.open_dataset(path_src + file_src_y).sel(level=200)

lon        = fx_1.lon.data
lat        = fx_1.lat.data

#print(len(lon)/2)
print(lon[int(len(lon)/2)])
# ==========================================================================

def paint_wave_flux(flux_u, flux_v):
    '''This function paint the Wave flux activity'''
    proj       =  ccrs.PlateCarree()
    ax         =  plt.subplot(projection=proj)

    # Create the subplot
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

    #cyclic_data_u, cyclic_lon = add_cyclic_point(flux_u, coord=lon)
    #cyclic_data_v, cyclic_lon = add_cyclic_point(flux_v, coord=lon)
    flux_u_copy = flux_u.copy() ; flux_v_copy = flux_v.copy()
    flux_u_copy[:, 0:int(len(lon)/2)] = flux_u[:, int(len(lon)/2):] ; flux_u_copy[:, int(len(lon)/2):] = flux_u[:, 0:int(len(lon)/2)]
    flux_v_copy[:, 0:int(len(lon)/2)] = flux_v[:, int(len(lon)/2):] ; flux_v_copy[:, int(len(lon)/2):] = flux_v[:, 0:int(len(lon)/2)]
    # Tick setting
    # extent
    # extent     =  [lonmin,lonmax,latmin,latmax]

    #set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(0,140,8,dtype=int),yticks=np.linspace(-10,70,9,dtype=int),nx=1,ny=1,labelsize=12.5)

    # contourf for the geopotential height
    #im1  =  ax.contourf(lon, lat, w*10e2 , levels=np.linspace(-4, 4, 17), cmap='coolwarm', alpha=1, extend='both')

    # stippling
    #plt.rcParams.update({'hatch.color': 'gray'})
    #sp  =  ax.contourf(lon, lat, p, levels=[0.1, 1], colors='none', hatches=['+++'])

    # Vector Map
    q  =  ax.quiver(lon - 180, lat, flux_u_copy, flux_v_copy, 
        regrid_shape=20, angles='uv',        # regrid_shape这个参数越小，是两门就越稀疏
        scale_units='xy', scale=0.001,        # scale是参考矢量，所以取得越大画出来的箭头就越短
        units='xy', width=0.5,              # width控制粗细
        transform=proj,
        color='k', headlength = 5, headaxislength = 4, headwidth = 4, alpha=0.8)

    ax.coastlines(resolution='50m', lw=1.2)

    #ax.set_ylabel("BTAL Long-term Changes", fontsize=11)

    ax.set_title('1901-1920', fontsize=12.5)

    # Add colorbar
    #plt.colorbar(im1, orientation='horizontal')

    #plt.savefig('/exports/csce/datastore/geos/users/s2618078/paint/analysis_EU_aerosol_climate_effect/circulation/BTAL_diff_JJAS_200_uv_500_OMEGA_no_stipplling.pdf')
    plt.savefig('test.png', dpi=700)

#paint_wave_flux(flux_u=(fx_2['Fx'] - fx_1['Fx']), flux_v=(fy_2['Fy'] - fy_1['Fy']))
paint_wave_flux(flux_u=(fx_2['Fx']), flux_v=(fy_2['Fy']))
#paint_wave_flux(flux_u=(fx_1['Fx']), flux_v=(fy_1['Fy']))