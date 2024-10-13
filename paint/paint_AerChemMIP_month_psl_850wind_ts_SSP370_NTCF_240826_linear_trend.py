'''
2024-8-26
This script is to plot the changes in MJJAS ts between SSP370 and SSP370lowNTCF, the simulation of historical is ignored

This script calculate the linear trend for 2015-2050
'''
import xarray as xr
import numpy as np
from scipy import stats
import sys
from sklearn.linear_model import LinearRegression

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import set_cartopy_tick,save_fig,add_vector_legend

#path_in   =  '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data
#models_label = ['EC-Earth3-AerChem','GFDL-ESM4','MRI-ESM2'] # GISS provide no daily data
#models_label = ['MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data

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
    # 3. calculate the trend
    trend = np.zeros((len(lat), len(lon)))

    for i in range(len(lat)):
        for j in range(len(lon)):
            if np.isnan(multiple_model_avg[:, i, j]).any():
                #print('NAN')
                continue
            else:
                #print(np.isnan(multiple_model_avg[:, i, j].any()))
                # 提取 (i, j) 位置上的时间序列
                y = multiple_model_avg[:, i, j]
                #print(y)
                #print(print(np.isnan(y.all())))
                X_time = np.arange(len(time)).reshape(-1, 1)

                # 创建并训练线性回归模型
                model = LinearRegression()
                model.fit(X_time, y)

                # 存储趋势 (斜率)
                trend[i, j] = model.coef_[0]

    return trend

def plot_change_wind_psl(u, v, psl, left_string, figname, lon, lat, parray, ct_level=np.linspace(-10., 10., 21),):
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

#    import sys
#    sys.path.append("/home/sun/local_code/module/")
#    from module_sun import set_cartopy_tick
    u[(u**2+v**2)<0.0008] = np.nan

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  40,280,-30,30
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree(central_longitude=180)
    fig1    =  plt.figure(figsize=(10,8))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    left_title = '{}'.format(left_string)
    right_title= ['SSP370 - SSP370lowNTCF']

    #pet        = [(ssp - sspntcf)]
    #pet        = [(ssp-sspntcf)]

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

    from cartopy.util import add_cyclic_point
    import cartopy.util as cutil
    #lon = (lon + 180) % 360 - 180
    #print(lon)
    psl1, clon1, clat1 = cutil.add_cyclic(psl, lon, lat)
    u,   clon, clat = cutil.add_cyclic(u,lon, lat)
    v,   clon, clat = cutil.add_cyclic(v,lon, lat)
    #clon = lon ; clat = lat

    # ------      paint    -----------
    for row in range(1):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(40,280,13,dtype=int),yticks=np.linspace(-30,30,3,dtype=int),nx=1,ny=1,labelsize=12)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im   =  ax.contourf(clon1, clat1, psl1, ct_level, cmap='coolwarm', alpha=1, extend='both',transform=ccrs.PlateCarree())

        #im2  =  ax.contourf(lon, lat, psl, np.linspace(-10, 0, 11), colors='grey', alpha=1,)

        # t 检验
        #sp  =  ax.contourf(lon, lat, parray, levels=[0., 0.05], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='110m',lw=1.65)

        #topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='brown', linewidths=3)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

        # wind
        q  =  ax.quiver(clon, clat, u, v, 
                regrid_shape=13, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=0.02,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.45,transform=ccrs.PlateCarree(),
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    cb.set_ticks(ct_level)
    cb.set_ticklabels(ct_level)

    #add_vector_legend(ax=ax, q=q, speed=0.1)

    plt.savefig("/home/sun/paint/AerChemMIP/AerChemMIP_modelgroup_global_MA_ssp370_linear_trend_{}.pdf".format(figname))

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

    # -------- u --------------
#    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_ua_month_MA.nc').sel(plev=85000)
#
#    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
#    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')
#
#    u         =  ssp0
#    u         =  np.nanmean(ssp0[-15:], axis=0) - np.nanmean(ssp0[:15], axis=0)
#    u         =  -1*(np.gradient(ssp0, axis=0) - np.gradient(ntcf0, axis=0))
#    sys.exit(u.shape)
#    u         =  ssp0

    # -------- v ---------------
#    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_va_month_MA.nc').sel(plev=85000)
#
#    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
#    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')
#
#    v         =  ssp0
#    v         =  np.nanmean(ssp0[-15:], axis=0) - np.nanmean(ssp0[:15], axis=0)
#    v         =  -1*(np.gradient(ssp0, axis=0) - np.gradient(ntcf0, axis=0))
#    v         =  ssp0

    # -------- psl -------------
    f0  =  xr.open_dataset('/Volumes/Untitled/AerChemMIP/process/multiple_model_climate_tas_month_March_April_36years.nc')

    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    psl         = ssp0
    sys.exit()
#    print(psl[45, :])
#    psl         =  np.nanmean(ssp0[-15:], axis=0) - np.nanmean(ssp0[:15], axis=0)
#    psl         =  -1*(np.gradient(ssp0, axis=0) - np.gradient(ntcf0, axis=0))
#    print(psl.shape)
#    ttest     =  cal_student_ttest(ssp0, ntcf0)
    ttest     =  0

    # Note that the variable in the above is three-dimension while the first is the number os the year
    levels    =  [-3, -2.5, -2, -1.5, -1, -.05, .05, 1, 1.5, 2, 2.5, 3]
    levels    =  np.linspace(-10, 10, 11, dtype=int)
    plot_change_wind_psl(u*10, v*10, psl*10, '850 hPa', '850 hPa', f0.lon.data, f0.lat.data, ttest, levels)