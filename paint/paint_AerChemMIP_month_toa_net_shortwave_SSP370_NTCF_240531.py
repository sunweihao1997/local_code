'''
2024-5-20
This script is to plot the changes in MJJAS ts between SSP370 and SSP370lowNTCF, the simulation of historical is ignored
'''
import xarray as xr
import numpy as np
from scipy import stats

path_in   =  '/data/AerChemMIP/process/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G']
#models_label = ['MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G']
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2']
#models_label = ['UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MIROC6',]

varname      = 'div'

#gen_f     = xr.open_dataset('/home/sun/data/topography/geo_1279l4_0.1x0.1.grib2_v4_unpack.nc')
#
#z         = gen_f['z'].data[0] / 9.8

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

def plot_change_wet_day(ssp, sspntcf, left_string, figname, lon, lat, parray, ct_level=np.linspace(-10., 10., 21),):
    '''
    This function is to plot the changes in the wet day among the SSP370 and SSP370lowNTCF

    This figure contains three subplot: 1. changes between SSP370 and historical 2. changes between SSP370lowNTCF and historical 3. NTCF mitigation (ssp370 - ssp370lowNTCF)
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    import sys
    sys.path.append("/root/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  40,150,0,50
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(10,8))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    left_title = '{}'.format(left_string)
    right_title= ['SSP370 - SSP370lowNTCF']

    pet        = [(ssp - sspntcf)]

    # -------    colormap --------------
    coolwarm = plt.get_cmap('coolwarm')

    colors = [
    (coolwarm(0.0)),  # 对应level -3
    (coolwarm(0.25)), # 对应level -2
    (1, 1, 1, 1),     # 插入白色，对应level -1到1
    (coolwarm(0.75)), # 对应level 2
    (coolwarm(1.0))   # 对应level 3
    ]

    new_cmap = LinearSegmentedColormap.from_list('custom_coolwarm', colors)

    # ------      paint    -----------
    for row in range(1):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(40,150,7,dtype=int),yticks=np.linspace(0,50,6,dtype=int),nx=1,ny=1,labelsize=15)

        # 添加赤道线
        #ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, pet[row], ct_level, cmap=new_cmap, alpha=1, extend='both')

        # t 检验
        sp  =  ax.contourf(lon, lat, parray, levels=[0., 0.05], colors='none', hatches=['.'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        #topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='brown', linewidths=3)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    cb.set_ticks(ct_level)
    cb.set_ticklabels(ct_level)

    plt.savefig("/data/paint/AerChemMIP_modelgroup_spatial_MJJAS_ssp370_ntcf_{}.png".format(figname))

def cal_student_ttest(array1, array2):
    '''
        This function is to calculate the student ttest among the array1 and array2
    '''
    p_value = np.zeros((array1.shape[1], array2.shape[2]))

    for i in range(array1.shape[1]):
        for j in range(array2.shape[2]):
            #print(i)
            p_value[i, j] = stats.ttest_rel(array1[:, i, j], array2[:, i, j])[1]

    return p_value

if __name__ == '__main__':
    f0  =  xr.open_dataset('/data/AerChemMIP/process/multiple_model_climate_rsdt_month_MJJAS.nc')
    f1  =  xr.open_dataset('/data/AerChemMIP/process/multiple_model_climate_rsut_month_MJJAS.nc')
    f2  =  xr.open_dataset('/data/AerChemMIP/process/multiple_model_climate_rsutcs_month_MJJAS.nc')

    ssp0_all      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp') - cal_multiple_model_avg(f1, 'ssp',  'time_ssp')
    ntcf0_all     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp') - cal_multiple_model_avg(f1, 'sspntcf', 'time_ssp')

    ttest_all     =  cal_student_ttest(ssp0_all, ntcf0_all)

    ssp0_cle      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')    - cal_multiple_model_avg(f2, 'ssp',  'time_ssp')
    ntcf0_cle     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp') - cal_multiple_model_avg(f2, 'sspntcf', 'time_ssp')

    ttest_cle     =  cal_student_ttest(ssp0_cle, ntcf0_cle)

    print(np.nanmean(ntcf0_cle))
    # Note that the variable in the above is three-dimension while the first is the number os the year
    levels    =  [-5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5,]
    plot_change_wet_day(np.nanmean(ssp0_cle, axis=0), np.nanmean(ntcf0_cle, axis=0), 'AOD550 (MJJAS)', 'AOD550 (MJJAS)', f0.lon.data, f0.lat.data, ttest_cle, levels)
    #plot_change_wet_day(np.nanmean(ssp0_all, axis=0), np.nanmean(ntcf0_all, axis=0), 'net shortwave (MJJAS)', 'net shortwave (MJJAS)', f0.lon.data, f0.lat.data, ttest_all, levels)