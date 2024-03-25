'''
2024-3-12
This script is for testing of heatmap for the spatial onset dates
'''

import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import sys
sys.path.append("/home/sun/local_code/module/")
from module_sun import set_cartopy_tick

f0  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/modelmean_except_noresm_onset_day.nc')

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(20, 15))

lonmin,lonmax,latmin,latmax  =  60,130,5,30
extent     =  [lonmin,lonmax,latmin,latmax]

cmap = plt.get_cmap('coolwarm').copy()
#cmap.set_extremes(under='white', over='white')

set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

im = ax.pcolormesh(f0.lon.data, f0.lat.data, 1.25*(f0['onset_ssp3'].data - f0['onset_ntcf'].data), cmap=cmap,vmin=-10, vmax=10)

ax.coastlines(resolution='10m',lw=1.65)
plt.colorbar(im, extend='both')

plt.savefig('test_onset_Bingwang_diff.png')