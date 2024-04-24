'''
2024-4-24
This script is to plot the changes in JJAS tasmin between SSP370 and SSP370lowNTCF, comparing with the historical simulation
'''
import xarray as xr
import numpy as np

path_in   =  '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data

varname      = 'tasmin'

def cal_multiple_model_avg(f0, exp_tag, timeaxis,):
    '''
    Because the input data is single model, so this function is to calculate the model-averaged data

    timeaxis is 65 for historical and 36 for furture simulation
    '''
    # 1. Generate the averaged array
    lat = f0.lat.data ; lon = f0.lon.data ; time = f0[timeaxis].data

    multiple_model_avg = np.zeros((len(time), len(lat), len(lon)))

    # 2. Calculation
    models_num = len(models_label)

    for mm in models_label:
        varname1 = mm + '_' + exp_tag

        multiple_model_avg += (f0[varname1].data / models_num)

    #
    return multiple_model_avg

def plot_change_wet_day(hist, ssp, sspntcf, left_string, figname, lon, lat, ct_level=np.linspace(-10., 10., 21)):
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
    sys.path.append("/root/local_code/module/")
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

    plt.savefig("/data/paint/AerChemMIP_modelgroup_spatial_JJAS_hist_ssp370_ntcf_{}.png".format(figname))

if __name__ == '__main__':
    f0  =  xr.open_dataset('/data/AerChemMIP/process/multiple_model_climate_tasmin_month_JJAS.nc')


    hist0     =  cal_multiple_model_avg(f0, 'hist', 'time_hist')
    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    print(np.nanmean(hist0))
    # Note that the variable in the above is three-dimension while the first is the number os the year
    plot_change_wet_day(np.nanmean(hist0[-40:], axis=0), np.nanmean(ssp0[-20:], axis=0), np.nanmean(ntcf0[-20:], axis=0), 'Tasmin (JJAS)', 'Tasmin (JJAS)', f0.lon.data, f0.lat.data, np.linspace(-1., 1., 11))