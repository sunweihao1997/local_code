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
from scipy.interpolate import griddata

file_name = 'modelmean_total_precip_rainy_season_diff_SSP370_SSP370lowNTCF.nc'
file_path = '/home/sun/data/process/analysis/AerChem/'

file0     = xr.open_dataset(file_path + file_name)

lat       = file0.lat.data
lon       = file0.lon.data

# Here I need to intepolate to fill the nan in the china | (100, 25), 10, 8
#print(lat[58]) ; print(lat[62])
#print(lon[50]) ; print(lon[55])

# ====================================================
def interp_data(data):
    n_rows, n_cols = data.shape
    # 找到非零和零的索引位置
    nonzero_indices = np.where(~np.isnan(data))
    zero_indices = np.where(np.isnan(data))

    # 对非零的点进行插值，准备数据点（X，Y）和值（Z）
    points = np.array(nonzero_indices).T
    values = data[nonzero_indices]

    # 准备需要插值的点的坐标
    grid_x, grid_y = np.mgrid[0:n_rows, 0:n_cols]

    # 执行插值
    data_interpolated = griddata(points, values, (grid_x, grid_y), method='cubic')

    # 将插值结果填回原始数组（对于边界外的插值可能为nan，可选择处理或保留）
    data[zero_indices] = np.round(data_interpolated[zero_indices])

    return data

total0 = file0['rain_change_total_modelmean'].data
inten0 = file0['rain_change_intensity_modelmean'].data

#print(total0[58:62, 50:55])
total0[58:62, 50:55] = interp_data(total0[58:62, 50:55])
inten0[58:62, 50:55] = interp_data(inten0[58:62, 50:55])
#print(np.average(total0[58:62, 50:55]))


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

    im  =  ax1.contourf(lon, lat, total, np.linspace(-200, 200, 21), cmap='coolwarm_r', alpha=1, extend='both')

    rect_indian = patches.Rectangle((100, 25), 10, 8, linewidth=3, edgecolor='r', facecolor='none')
    ax1.add_patch(rect_indian)

    fig.colorbar(im, ax=ax1, location='right', anchor=(0, 0.5), shrink=0.7)

    ax1.coastlines(resolution='10m',lw=1.65)

    ax1.set_title('total rain', loc='left', fontsize=20.5)
    ax1.set_title('SSP370 - SSP370lowNTCF', loc='right', fontsize=20.5)


    # ---- intensity ----
    im2  =  ax2.contourf(lon, lat, intensity, np.linspace(-1, 1, 21), cmap='coolwarm_r', alpha=1, extend='both')

    fig.colorbar(im2, ax=ax2, location='right', anchor=(0, 0.5), shrink=0.7)

    set_cartopy_tick(ax=ax2,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

    ax2.coastlines(resolution='10m',lw=1.65)

    ax2.set_title('intensity of rain (mm/day)', loc='left', fontsize=20.5)
    ax2.set_title('SSP370 - SSP370lowNTCF', loc='right', fontsize=20.5)

    # save figure
    plt.savefig("/home/sun/paint/AerMIP/precipitation_in_rainy_season_difference_model_mean.png")

paint_diff_precip(total0, inten0)