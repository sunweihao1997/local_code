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
ssp370_f  = 'CMIP6_model_SSP370_monthly_precipitation_2031-2050.nc'
sspntcf_f = 'CMIP6_model_SSP370NTCF_monthly_precipitation_2031-2050.nc'

f_ref     = xr.open_dataset(data_path + ssp370_f)

May_ssp   = xr.open_dataset(data_path + ssp370_f).sel(time=f_ref.time.dt.month.isin([5, ]))  ; Jun_ssp   =  xr.open_dataset(data_path + ssp370_f).sel(time=f_ref.time.dt.month.isin([6, ]))
May_NTCF  = xr.open_dataset(data_path + sspntcf_f).sel(time=f_ref.time.dt.month.isin([5, ])) ; Jun_NTCF  =  xr.open_dataset(data_path + sspntcf_f).sel(time=f_ref.time.dt.month.isin([6, ]))

May_diff  = np.average(May_ssp['pr'].data, axis=0) - np.average(May_NTCF['pr'].data, axis=0)
Jun_diff  = np.average(Jun_ssp['pr'].data, axis=0) - np.average(Jun_NTCF['pr'].data, axis=0)

lat       = f_ref.lat.data
lon       = f_ref.lon.data

p_value_may = np.zeros(May_diff.shape)
p_value_Jun = np.zeros(Jun_diff.shape)

for i in range(len(lat)):
    for j in range(len(lon)):
        t_stat, p_value = stats.ttest_ind(May_ssp['pr'].data[:, i, j], May_NTCF['pr'].data[:, i, j])

        p_value_may[i, j] = p_value

        t_stat, p_value = stats.ttest_ind(Jun_ssp['pr'].data[:, i, j], Jun_NTCF['pr'].data[:, i, j])

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

    left_title = ['May', 'Jun'] ; right_title = 'SSP370 - SSP370NTCF'
    # ------       paint    ------------
    for col in range(2):
        row = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, prect[col], np.linspace(-2.5, 2.5, 21), cmap='coolwarm', alpha=1, extend='both')

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

    plt.savefig("/data/paint/spatial_SSP370-SSP370NTCF_precip.png")

def main():
    prect0 = [May_diff, Jun_diff]

    p_value = [p_value_may, p_value_Jun]
    paint_pentad_circulation(prect0, p_value)

if __name__ == '__main__':
    main()