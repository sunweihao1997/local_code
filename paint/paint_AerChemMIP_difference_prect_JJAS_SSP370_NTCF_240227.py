'''
2024-3-26
This script is to show the difference between the SSP370 and SSP370NTCF for the period 2031-2050 in the JJAS averages precipitation
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

gen_f     = xr.open_dataset('/data/AerChemMIP/geopotential/geo_1279l4_0.1x0.1.grib2_v4_unpack.nc')

# Read and deal with the topography
z         = gen_f['z'].data[0] / 9.8

file0     = xr.open_dataset(data_path + diff_f)

lat       = file0.lat.data
lon       = file0.lon.data

JJAS_f    = file0.sel(time=file0.time.dt.month.isin([6, 7, 8, 9]))

p_value_jjas = np.zeros((121, 241))

#print(p_value_Jun.shape)

# ========= Calculate the JJAS average ===========
year_list    = np.linspace(2031, 2050, 20)

pr_ssp_JJAS  = np.zeros((len(year_list), 121, 241))
pr_ntcf_JJAS = np.zeros((len(year_list), 121, 241))

k = 0
for yy in year_list:
    # 1. Select the variable this year
    JJAS_f_year = JJAS_f.sel(time=JJAS_f.time.dt.year.isin([yy]))

    #print(JJAS_f_year.time.shape)
    pr_ssp_JJAS[k]  = np.average(JJAS_f_year['pr_ssp'].data, axis=0) 
    pr_ntcf_JJAS[k] = np.average(JJAS_f_year['pr_ntcf'].data, axis=0)

    k += 1


for i in range(len(lat)):
    for j in range(len(lon)):
        t_stat, p_value = stats.ttest_ind(pr_ssp_JJAS[:, i, j], pr_ntcf_JJAS[:, i, j])

        p_value_jjas[i, j] = p_value

def paint_pentad_circulation(prect, p_value):
    '''This function paint pentad circulation based on b1850 experiment'''
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches

    import sys
    sys.path.append("/root/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,-10,60
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(32,14))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    j  =  0

    # -------     points     ---------------
    points_indian = (70, 15)
    points_indo   = (90, 10)
    points_scs    = (110, 10)
    points_tp     = (80, 27.5)
    points_ea     = (110, 22.5)

    left_title = 'JJAS' ; right_title = 'SSP370 - SSP370lowNTCF'
    # ------       paint    ------------
    for col in range(1):
        row = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,60,8,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, prect, np.linspace(-1., 1., 21), cmap='coolwarm_r', alpha=1, extend='both')

        sp  =  ax.contourf(lon, lat, p_value, levels=[0., 0.1], colors='none', hatches=['..'])

        topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='red', lineswidth=4.5)

        

#        # add rectangle
#
#        rect_indian = patches.Rectangle(points_indian, 17.5, 10, linewidth=3, edgecolor='r', facecolor='none')
#        ax.add_patch(rect_indian)
#
#        rect_indo    = patches.Rectangle(points_indo, 18, 16.5, linewidth=3, edgecolor='purple', facecolor='none')
#        ax.add_patch(rect_indo)
#
#        rect_scs     = patches.Rectangle(points_scs, 10, 10, linewidth=3, edgecolor='yellow', facecolor='none')
#        ax.add_patch(rect_scs)
#
#        rect_tp      = patches.Rectangle(points_tp, 25, 10, linewidth=3, edgecolor='blue', facecolor='none')
#        ax.add_patch(rect_tp)
#
#        rect_ea      = patches.Rectangle(points_ea, 12.5, 12, linewidth=3, edgecolor='green', facecolor='none')
#        ax.add_patch(rect_ea)
        # 海岸线
        ax.coastlines(resolution='10m',lw=1.65)

        ax.set_title(left_title, loc='left', fontsize=20.5)
        ax.set_title(right_title, loc='right', fontsize=20.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/modelgroup_spatial_MJJAS_SSP370-SSP370NTCF_precip.png")

def main():
    prect0 = np.average(pr_ssp_JJAS, axis=0) - np.average(pr_ntcf_JJAS, axis=0)

    p_value = p_value_jjas
    paint_pentad_circulation(prect0, p_value)

if __name__ == '__main__':
    main()