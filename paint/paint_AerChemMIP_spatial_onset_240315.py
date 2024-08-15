'''
2024-3-12
This script is for testing of heatmap for the spatial onset dates
'''

import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib import cm
from matplotlib.colors import ListedColormap

import sys
sys.path.append("/home/sun/local_code/module/")
from module_sun import set_cartopy_tick

# 2.1 Set the colormap
viridis = cm.get_cmap('coolwarm', 22)
newcolors = viridis(np.linspace(0, 1, 22))
newcmp = ListedColormap(newcolors)
#newcmp.set_under('white')
#newcmp.set_over('white')

f0  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/modelmean_onset_day_threshold5.nc')

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(20, 15))

lonmin,lonmax,latmin,latmax  =  60,130,5,30
extent     =  [lonmin,lonmax,latmin,latmax]

cmap = plt.get_cmap('coolwarm').copy()
#cmap.set_extremes(under='white', over='white')

set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

im = ax.pcolormesh(f0.lon.data, f0.lat.data, 1.*(f0['onset_ssp3'].data - f0['onset_ntcf'].data), cmap=newcmp, vmin=-15, vmax=15)
#df = pd.DataFrame(data=1.25*(f0['onset_ssp3'].data - f0['onset_ntcf'].data), columns=f0.lon.data, index=f0.lat.data)
#sns.heatmap(df)

ax.set_title('multi-model mean', loc='left', fontsize=15)
ax.set_title('Criterion BinWang', loc='right', fontsize=15)

ax.coastlines(resolution='50m',lw=1.65)
plt.colorbar(im, extend='both', orientation='horizontal')

plt.savefig('/home/sun/paint/AerMIP/Article_onset_Bingwang_diff_threshold5_ssp370_minus_ssp370ntcf.png')
