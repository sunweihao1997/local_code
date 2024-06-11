'''
2024-6-11
This script is to plot the changes in MJJAS ts between SSP370 and SSP370lowNTCF, the simulation of historical is ignored
'''
import xarray as xr
import numpy as np
from scipy import stats

path_in   =  '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data
models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G']


varname      = 'div'

gen_f     = xr.open_dataset('/home/sun/data/topography/geo_1279l4_0.1x0.1.grib2_v4_unpack.nc')

z         = gen_f['z'].data[0] / 9.8

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
        if mm == 'MPI-ESM-1-2-HAM':
            varname1 = mm + '_' + exp_tag

            multiple_model_avg += (0.8 * f0[varname1].data / models_num)
        else:
            varname1 = mm + '_' + exp_tag

            multiple_model_avg += (f0[varname1].data / models_num)
    #
    return multiple_model_avg

def plot_change_wet_day(div_ms, u, v, psl, left_string, figname, lon, lat, parray, ct_level=np.linspace(-10., 10., 21),):
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
    sys.path.append("/home/sun/local_code/module/")
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

    #pet        = [(ssp - sspntcf)]
    pet        = [(div_ms)]

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
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(40,140,6,dtype=int),yticks=np.linspace(0,50,6,dtype=int),nx=1,ny=1,labelsize=15)

        # 添加赤道线
        #ax.plot([40,150],[0,0],'k--')

        im   =  ax.contourf(lon, lat, pet[row], ct_level, cmap='coolwarm', alpha=1, extend='both')

        im2  =  ax.contour(lon, lat, psl, np.linspace(-40, 40, 11), colors='grey', linewidth = 0.8, alpha=0.6,)
        ax.clabel(im2, fontsize=7.5, inline=1)

        # t 检验
        #sp  =  ax.contourf(lon, lat, parray, levels=[0., 0.05], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        #topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='brown', linewidths=3)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

        # wind
        q  =  ax.quiver(lon, lat, u, v, 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=0.04,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.4,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    cb.set_ticks(ct_level)
    cb.set_ticklabels(ct_level)

    plt.savefig("/home/sun/paint/AerChemMIP/AerChemMIP_modelgroup_spatial_MJJAS_ssp370_ntcf_{}_vertical_ms_div.pdf".format(figname))

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
    #--------- div-------------
    # Note that it is the divergence of the vertical integral of moisture transportation, reference is following
    # /home/sun/local_code/calculate/cal_AerChemMIP_vertical_integral_water_transportation_240528.ncl

    div_diff_modelmean = np.zeros((91, 180))
    for modelname in models_label:
        f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/modelmean_climate_water_transportation_integral_MJJAS_{}.nc'.format(modelname))
    
        div_diff = f0['vert_integral_ssp'].data - f0['vert_integral_ntcf'].data

        #print(np.nanmean(div_diff))

        div_diff[div_diff>1e-5] = 0
        div_diff[div_diff<-1e-5] = 0

        div_diff_modelmean += (div_diff/len(models_label))

    models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MIROC6', 'GISS-E2-1-G']

    # -------- u --------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_ua_month_MJJAS_all.nc').sel(plev=85000)

    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')
    #print(ssp0.shape)

    u         =  np.nanmean(ssp0[-20:], axis=0) - np.nanmean(ntcf0[-20:], axis=0)

    # -------- v ---------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_va_month_MJJAS_all.nc').sel(plev=85000)

    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    v         =  np.nanmean(ssp0[-20:], axis=0) - np.nanmean(ntcf0[-20:], axis=0)

    # -------- psl -------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_psl_month_MJJAS.nc')

    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    psl         =  np.nanmean(ssp0, axis=0) - np.nanmean(ntcf0, axis=0)

    # Note that the variable in the above is three-dimension while the first is the number os the year
    levels    =  [-10, -8, -6, -4, -2, -.5, .5, 2, 4, 6, 8, 10]
    levels    =  [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    plot_change_wet_day(div_diff_modelmean*1e6, u, v, psl, '850 hPa (MJJAS)', '850 hPa (MJJAS)', f0.lon.data, f0.lat.data, 0, levels)