'''
2024-5-27
This script is to plot the changes in MJJAS ts between SSP370 and SSP370lowNTCF, the simulation of historical is ignored
'''
import xarray as xr
import numpy as np
from scipy import stats
import cartopy.util as cutil
from scipy.stats import kendalltau

path_in   =  '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', ] # GISS provide no daily data
#models_label = ['EC-Earth3-AerChem','UKESM1-0-LL', 'GFDL-ESM4','MRI-ESM2'] # GISS provide no daily data
#models_label = ['MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data

varname      = 'div'

gen_f     = xr.open_dataset('/home/sun/data/topography/geo_1279l4_0.1x0.1.grib2_v4_unpack.nc')

z         = gen_f['z'].data[0] / 9.8

def cal_multiple_model_avg(f0, exp_tag, timeaxis,):
    '''
    Because the input data is single model, so this function is to calculate the model-averaged data

    timeaxis is 65 for historical and 36 for furture simulation
    '''
    # 1. Generate the averaged array
    lat = f0.lat.data ; lon = f0.lon.data ; time = f0[timeaxis].data ; 

    multiple_model_avg = np.zeros((len(time), len(lat), len(lon)))

    # 2. Calculation
    models_num = len(models_label)

    for mm in models_label:
        varname1 = mm + '_' + exp_tag

        multiple_model_avg += (f0[varname1].data / models_num)

    #
    return multiple_model_avg

def plot_change_wet_day(ssp, sspntcf, left_string, figname, lon, lat, ttest, ct_level=np.linspace(-10., 10., 21),):
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
    lonmin,lonmax,latmin,latmax  =  5,355,0,75
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    #proj  =    ccrs.Robinson(central_longitude=180)
    proj   =    ccrs.PlateCarree(central_longitude=180)
    fig1    =  plt.figure(figsize=(15,6))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    left_title = '{}'.format(left_string)
    right_title= ['SSP370 - SSP370lowNTCF']

    pet        = [ssp-sspntcf]

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
        ax = fig1.add_subplot(spec1[row,col], projection=ccrs.PlateCarree(central_longitude=180))
        ax.set_global()
        

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.arange(10,355,30,dtype=int),yticks=np.linspace(0,70,8,dtype=int),nx=1,ny=1,labelsize=15)

        # 添加赤道线
        #ax.plot([40,150],[0,0],'k--')

        # add cyclic point
#        lon2d, lat2d = np.meshgrid(lon, lat)
#        cdata, clon2d, clat2d = cutil.add_cyclic(pet[row], lon2d, lat2d)
#
#        im  =  ax.contourf(clon2d, clat2d, cdata, ct_level, cmap=new_cmap, alpha=1, extend='both')
        im  =  ax.contourf(lon, lat, pet[row], ct_level, cmap='coolwarm', alpha=1, extend='both', transform=ccrs.PlateCarree())

        # t 检验
        sp  =  ax.contourf(lon, lat, ttest, levels=[0., 0.05], colors='none', hatches=['..'])


        # 海岸线
        ax.coastlines(resolution='110m',lw=1.65)

        #topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='brown', linewidths=3)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

        # wind
#        q  =  ax.quiver(lon, lat, u, v, 
#                regrid_shape=20, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
#                scale_units='xy', scale=0.7,        # scale是参考矢量，所以取得越大画出来的箭头就越短
#                units='xy', width=0.4,
#                transform=ccrs.PlateCarree(),
#                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)


    plt.savefig("/home/sun/paint/AerChemMIP/AerChemMIP_modelgroup_spatial_MJJAS_ssp370_ntcf_{}.png".format(figname))

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
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_column_cdnc_month_MJJAS.nc')

    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    ttest     =  cal_student_ttest(ssp0, ntcf0)

    #print(np.nanmax(ssp0))

    #print(np.nanmean(psidev))

    # Wave activity flux
#    f1  =  xr.open_dataset("/home/sun/data/AerChemMIP/process/AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fx.MJJAS.nc").sel(level=300)
#    f2  =  xr.open_dataset("/home/sun/data/AerChemMIP/process/AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fy.MJJAS.nc").sel(level=300)

#    f1.Fx.data[abs(f1.Fx.data) > 0.1] = np.nan
#    f2.Fy.data[abs(f2.Fy.data) > 0.1] = np.nan
#    print(np.nanmax(f1.Fx.data))



    # Note that the variable in the above is three-dimension while the first is the number os the year
    #levels    =  [-14, -12, -10, -8, -6, -4, -2, -1, 1, 2, 4, 6, 8, 10, 12, 14]
    #levels    =  [-1.0, -.8, -.6, -.4, -.2, -0.1, -.05, .05, 0.1, .2, .4, .6, .8, 1.0,]

    levels    =  np.array([-10, -8, -6, -4, -3, -2, -1, 0, 1, 2, 3, 4, 6, 8, 10])

    # Calculate slope
#    fxg = np.zeros((91, 180))
#    fyg = np.zeros((91, 180))
#    for i in range(91):
#        for j in range(180):
#            if any(np.isnan(f1.Fx.data[:, i, j])) or any(np.isnan(f2.Fy.data[:, i, j])):
#                fxg[i, j] = np.nan ; fyg[i, j] = np.nan
#            else:
#                slope, intercept = np.polyfit(np.linspace(1, 20, 20), f1.Fx.data[:, i, j], 1)
#                tau, p_value = kendalltau(np.linspace(1, 20, 20), f1.Fx.data[:, i, j])
#
#                if p_value < 1:
#                    fxg[i, j] = slope
#                else:
#                    fxg[i, j] = np.nan
#
#                slope, intercept = np.polyfit(np.linspace(1, 20, 20), f2.Fy.data[:, i, j], 1)
#                tau, p_value = kendalltau(np.linspace(1, 20, 20), f2.Fy.data[:, i, j])
#                if p_value <1 :
#                    fyg[i, j] = slope
#                else:
#                    fyg[i, j] = np.nan
#
    print(np.nanmean(ssp0))

    #plot_change_wet_day(np.nanmean(ssp0, axis=0) * 10e2, np.nanmean(ntcf0, axis=0) * 10e2, '200hPa v (MJJAS)', '200hPa v (MJJAS)', f0.lon.data, f0.lat.data, ttest, levels)
    #plot_change_wet_day(np.nanmean(ssp0, axis=0), np.nanmean(ntcf0, axis=0), fxg * 100, fyg * 100, '300hPa v (MJJAS)', '300hPa v (MJJAS)', f0.lon.data, f0.lat.data, ttest, levels/10)
    plot_change_wet_day(np.nanmean(ssp0, axis=0), np.nanmean(ntcf0, axis=0), 'Column CDNC (MJJAS)', 'Column CDNC (MJJAS)', f0.lon.data, f0.lat.data, ttest, levels)