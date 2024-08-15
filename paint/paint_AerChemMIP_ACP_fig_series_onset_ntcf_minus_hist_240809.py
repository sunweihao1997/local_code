'''
2024-8-9
This script is for showing the changes in onsetdate under different scenarios and areas
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

f0         =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/modelmean_onset_day_threshold4_10_harmonics.nc')
mask_file  =  xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid2x2.nc')


# ========== Define a function which could masked the value for land or ocean ==========
def mask_value(data_file, lat_slice, lon_slice, maskdata, opt, varname):
    # 1. select the range of data
    data_1    = data_file.sel(lat=lat_slice, lon=lon_slice)
    maskdata1 = maskdata.sel(latitude=lat_slice, longitude=lon_slice)

    mask      = maskdata1.lsm.data[0]

    if opt ==1 : # land
        data_1[varname].data[mask<0.2] = np.nan
    else: # ocean
        data_1[varname].data[mask>0.2] = np.nan

    data_1[varname].data[data_1[varname].data>300] = np.nan

    avg_data = np.nanmean(data_1[varname].data)

    print(avg_data)

# ============= Calculate the area mean ===============

china_north = mask_value(f0, slice(30, 40), slice(100, 130), mask_file, 1, 'onset_hist')
china_north = mask_value(f0, slice(30, 40), slice(100, 130), mask_file, 1, 'onset_ssp3')
china_north = mask_value(f0, slice(30, 40), slice(100, 130), mask_file, 1, 'onset_ntcf')

china_south = mask_value(f0, slice(20, 30), slice(100, 130), mask_file, 1, 'onset_hist')
china_south = mask_value(f0, slice(20, 30), slice(100, 130), mask_file, 1, 'onset_ssp3')
china_south = mask_value(f0, slice(20, 30), slice(100, 130), mask_file, 1, 'onset_ntcf')

indochina   = mask_value(f0, slice(10, 20), slice(100, 110), mask_file, 1, 'onset_hist')
indochina   = mask_value(f0, slice(10, 20), slice(100, 110), mask_file, 1, 'onset_ssp3')
indochina   = mask_value(f0, slice(10, 20), slice(100, 110), mask_file, 1, 'onset_ntcf')

indian      = mask_value(f0, slice(10, 25), slice(70,  90), mask_file, 1, 'onset_hist')
indian      = mask_value(f0, slice(10, 25), slice(70,  90), mask_file, 1, 'onset_ssp3')
indian      = mask_value(f0, slice(10, 25), slice(70,  90), mask_file, 1, 'onset_ntcf')

sys.exit()

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(15, 10))

lonmin,lonmax,latmin,latmax  =  60,130,5,40
extent     =  [lonmin,lonmax,latmin,latmax]

cmap = plt.get_cmap('coolwarm').copy()
#cmap.set_extremes(under='white', over='white')

set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=25)

# Set non-monsoon area as nan
diff_onset = f0['onset_ntcf'].data - f0['onset_hist'].data
#print(diff_onset[:, 50])
diff_onset[diff_onset == 0.] = np.nan
im = ax.pcolormesh(f0.lon.data, f0.lat.data, 1.*(diff_onset), cmap=newcmp, vmin=-15, vmax=15)
#df = pd.DataFrame(data=1.25*(f0['onset_ssp3'].data - f0['onset_ntcf'].data), columns=f0.lon.data, index=f0.lat.data)
#sns.heatmap(df)

#ax.set_title('multi-model mean', loc='left', fontsize=15)
ax.set_title('SSP370lowNTCF - Hist', loc='right', fontsize=25)

ax.coastlines(resolution='50m',lw=2)
cbar = fig.colorbar(im, ax=ax, extend='both', orientation='horizontal')

# 设置 colorbar 的标签
cbar.set_label('Day', size=25)  # 设置 colorbar 标签的文本和大小

# 设置 colorbar 的刻度标签大小
cbar.ax.tick_params(labelsize=20)  # 可以调整刻度标签的大小

plt.savefig('/home/sun/paint/AerMIP/Article_onset_Bingwang_diff_threshold4_ssp370ntcf_minus_hist.pdf')
