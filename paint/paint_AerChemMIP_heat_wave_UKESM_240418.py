'''
2024-4-19
This script is to check the result from the UKESM for heatwave
'''
import xarray as xr
import numpy as np
import os

f1  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/heat_wave/result/EC-Earth3-AerChem_heat_wave_r1i1p1f1.nc')
f2  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/heat_wave/UKESM1-0-LL_heat_wave_r2i1p1f2.nc')
f3  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/heat_wave/UKESM1-0-LL_heat_wave_r3i1p1f2.nc')

#print(f1)
def plot_change_wet_day(hist, ssp, sspntcf, left_string, figname, lon, lat, ct_level=np.linspace(-5., 5., 11)):
    '''
    This function is to plot the changes in the wet day among the SSP370 and SSP370lowNTCF

    This figure contains three subplot: 1. changes between SSP370 and historical 2. changes between SSP370lowNTCF and historical 3. NTCF mitigation (ssp370 - ssp370lowNTCF)
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    import sys
    sys.path.append("/home/sun/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  40,150,-10,60
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(20,30))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=1)

    left_title = '{} (JJAS)'.format(left_string)
    right_title= ['SSP370 - Hist', 'SSP370lowNTCF - Hist', 'NTCF mitigation']

    pet        = [(ssp - hist), (sspntcf - hist), (ssp - sspntcf)]

    # ------      paint    -----------
    for row in range(3):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(40,150,7,dtype=int),yticks=np.linspace(-10,60,8,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, pet[row], ct_level, cmap='coolwarm', alpha=1, extend='both')

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/home/sun/paint/AerMIP/AerChemMIP_UK_heatwave_ssp370_ntcf_{}.png".format(figname))

if __name__ == '__main__':
    plot_change_wet_day(np.nanmean(f1.hist_hw_tasmax.data[2, -30:, :, :], axis=0), np.nanmean(f1.ssp_hw_tasmax.data[2, -20:, :, :], axis=0), np.nanmean(f1.ntcf_hw_tasmax.data[2, -20:, :, :], axis=0), 'UKESM', 'UKESM', f1.lon.data, f1.lat.data)
    print(np.nanmin(f1.hist_hw_tasmax.data))