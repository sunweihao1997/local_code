'''
2024-3-29
This script is to plot the area of the global monsoon
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import scipy.stats as stats
from matplotlib import cm
from matplotlib.colors import ListedColormap

import sys
sys.path.append("/home/sun/local_code/module/")
from module_sun import set_cartopy_tick

data_path = '/home/sun/data/process/analysis/AerChem/'
data_name = 'globalmonsoon_area_modelmean_hist_ssp370_ssp370ntcf_300mm_dry_150.nc'

file0     = xr.open_dataset(data_path + data_name)

lat       = file0.lat.data ; lon      = file0.lon.data

# -------   cartopy extent  -----
lonmin,lonmax,latmin,latmax  =  45,150,-10,80
extent     =  [lonmin,lonmax,latmin,latmax]

fig, ax1 = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

#set_cartopy_tick(ax=ax1,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,60,8,dtype=int),nx=1,ny=1,labelsize=15)

im1  =  ax1.contour(lon, lat, file0['hist_area'], [0], colors='k', alpha=1, linewidths = 1.5)
im2  =  ax1.contour(lon, lat, file0['ssp_area'],  [0], colors='r', alpha=1, linewidths = 1.)
im3  =  ax1.contour(lon, lat, file0['ntcf_area'], [0], colors='b', alpha=1, linewidths = 1.)

ax1.coastlines(resolution='110m',lw=0.9)

plt.savefig('/home/sun/paint/AerMIP/global_monsoon_area.pdf', dpi=1000)