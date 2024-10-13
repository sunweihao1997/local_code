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

def five_points_smoother(array):
    from scipy.ndimage import convolve

    kernel = np.array([
        [0, 1, 0],
        [1, 4, 1],
        [0, 1, 0]
    ]) / 8.0  # 总权重为8

    return convolve(array, kernel, mode='constant', cval=0.0)

f1  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/modelmean_onset_day_threshold4_10_harmonics.nc')
f0  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/modelmean_withdraw_day_threshold4_reverse.nc')

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(15, 10))

lonmin,lonmax,latmin,latmax  =  60,130,5,40
extent     =  [lonmin,lonmax,latmin,latmax]

cmap = plt.get_cmap('coolwarm').copy()
#cmap.set_extremes(under='white', over='white')

set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

rainyseason = 1*(five_points_smoother((f0['withdraw_ntcf'].data - f1['onset_ntcf'].data) - (f0['withdraw_ssp3'].data - f1['onset_ssp3'].data)))
rainyseason[(f1['onset_ssp3'].data-f1['onset_hist'].data)==0] = np.nan
im = ax.pcolormesh(f0.lon.data, f0.lat.data, rainyseason, cmap=newcmp, vmin=-20, vmax=20)#df = pd.DataFrame(data=1.25*(f0['onset_ssp3'].data - f0['onset_ntcf'].data), columns=f0.lon.data, index=f0.lat.data)
#df = pd.DataFrame(data=1.25*(f0['onset_ssp3'].data - f0['onset_ntcf'].data), columns=f0.lon.data, index=f0.lat.data)
#sns.heatmap(df)

#ax.set_title('multi-model mean', loc='left', fontsize=15)
ax.set_title('Air-pollution mitigation', loc='right', fontsize=25)

ax.coastlines(resolution='50m',lw=2)
cbar = fig.colorbar(im, ax=ax, extend='both', orientation='horizontal')

# 设置 colorbar 的标签
cbar.set_label('Day', size=25)  # 设置 colorbar 标签的文本和大小

# 设置 colorbar 的刻度标签大小
cbar.ax.tick_params(labelsize=20)  # 可以调整刻度标签的大小

plt.savefig('/home/sun/paint/AerMIP/Article_rainyseason_Bingwang_diff_threshold4_ssp370_minus_ssp370ntcf.pdf')
