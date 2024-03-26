'''
2024-2-27
This script is to show the difference between the SSP370 and SSP370NTCF for the period 2031-2050
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import scipy.stats as stats

data_path = '/data/AerChemMIP/LLNL_download/model_average/'
diff_f    = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_precipitation_2015-2050_new.nc'

file0     = xr.open_dataset(data_path + diff_f)

lat       = file0.lat.data
lon       = file0.lon.data

May_diff  = file0.sel(time=file0.time.dt.month.isin([9]))
Jun_diff  = file0.sel(time=file0.time.dt.month.isin([10]))

p_value_may = np.zeros((121, 241))
p_value_Jun = np.zeros((121, 241))

print(p_value_Jun.shape)

for i in range(len(lat)):
    for j in range(len(lon)):
        t_stat, p_value = stats.ttest_ind(May_diff['pr_ssp'].data[:, i, j], May_diff['pr_ntcf'].data[:, i, j])

        p_value_may[i, j] = p_value

        t_stat, p_value = stats.ttest_ind(Jun_diff['pr_ssp'].data[:, i, j], Jun_diff['pr_ntcf'].data[:, i, j])

        p_value_Jun[i, j] = p_value

def paint_pentad_circulation(prect, p_value):
    '''This function paint pentad circulation based on b1850 experiment'''
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/root/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,-10,35
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(32,10))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=2)

    j  =  0

    left_title = ['Sep', 'Oct'] ; right_title = 'SSP370 - SSP370NTCF'
    # ------       paint    ------------
    for col in range(2):
        row = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, prect[col], np.linspace(-1.5, 1.5, 13), cmap='coolwarm_r', alpha=1, extend='both')

        sp  =  ax.contourf(lon, lat, p_value[col], levels=[0., 0.05], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='10m',lw=1.65)

        ax.set_title(left_title[col], loc='left', fontsize=20.5)
        ax.set_title(right_title, loc='right', fontsize=20.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/modelgroup_segment_adjust_spatial_Sep_Oct_SSP370-SSP370NTCF_precip.png")

def main():
    prect0 = [np.average(May_diff['pr_ssp'].data[-20:], axis=0) - np.average(May_diff['pr_ntcf'].data[-20:], axis=0), np.average(Jun_diff['pr_ssp'].data[-20:], axis=0) - np.average(Jun_diff['pr_ntcf'].data[-20:], axis=0)]

    p_value = [p_value_may, p_value_Jun]
    paint_pentad_circulation(prect0, p_value)

if __name__ == '__main__':
    main()