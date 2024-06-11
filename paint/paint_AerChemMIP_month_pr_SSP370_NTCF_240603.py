'''
2024-5-20
This script is to plot the changes in MJJAS ts between SSP370 and SSP370lowNTCF, the simulation of historical is ignored
'''
import xarray as xr
import numpy as np
from scipy import stats

path_in   =  '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data
#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2'] # GISS provide no daily data
#models_label = ['EC-Earth3-AerChem'] # GISS provide no daily data

varname      = 'tasmin'

gen_f     = xr.open_dataset('/data/AerChemMIP/geopotential/geo_1279l4_0.1x0.1.grib2_v4_unpack.nc')

z         = gen_f['z'].data[0] / 9.8

def cal_multiple_model_avg_modified(f0, exp_tag1, exp_tag2,):
    '''
    Because the input data is single model, so this function is to calculate the model-averaged data

    timeaxis is 65 for historical and 36 for furture simulation
    '''
    # 1. Generate the averaged array
    lat = f0.lat.data ; lon = f0.lon.data

    multiple_model_avg_diff = np.zeros((len(lat), len(lon)))

    # 2. Calculation
    models_num = len(models_label)

    agreement          = np.zeros((models_num, len(lat), len(lon)))
    signs              = np.zeros((len(lat), len(lon)))
    threshold          = 6

    mnum = 0
    for mm in models_label:
        varname1 = mm + '_' + exp_tag1
        varname2 = mm + '_' + exp_tag2

        single_diff = ((np.average(f0[varname1].data, axis=0)) - (np.average(f0[varname2].data, axis=0))) / (np.average(f0[varname1].data, axis=0))
        agreement[mnum][single_diff > 0] = 1 ; agreement[mnum][single_diff < 0] = -1 

        multiple_model_avg_diff += (single_diff / models_num)
        mnum += 1

    #print(agreement[:, 50, 50])

    for ii in range(len(lat)):
        for jj in range(len(lon)):
            #print(np.sum(agreement[:, ii, jj]==1))
            if np.sum(agreement[:, ii, jj]==1) >= threshold or np.sum(agreement[:, ii, jj]==-1) >= threshold:
                
                signs[ii, jj] = 1


    return multiple_model_avg_diff, signs

def plot_change_wet_day(diff, left_string, figname, lon, lat, parray, ct_level=np.linspace(-10., 10., 21),):
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

    pet        = [(diff)]

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

        im  =  ax.contourf(lon, lat, pet[row], ct_level, cmap='coolwarm', alpha=1, extend='both')

        # t 检验
        sp  =  ax.contourf(lon, lat, parray, levels=[0.5, 1], colors='none', hatches=['..'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='red', linewidth=4.5)

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

def plot_change_wet_day_northern(diff, left_string, figname, lon, lat, parray, ct_level=np.linspace(-10., 10., 21),):
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
    lonmin,lonmax,latmin,latmax  =  5,355,0,75
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj    =    ccrs.PlateCarree(central_longitude=180)
    fig1    =  plt.figure(figsize=(15,8))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    left_title = '{}'.format(left_string)
    right_title= ['SSP370 - SSP370lowNTCF']

    pet        = [(diff)]

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
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.arange(10,355,30,dtype=int),yticks=np.linspace(0,70,8,dtype=int),nx=1,ny=1,labelsize=15)

        # 添加赤道线
        #ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, pet[row], ct_level, cmap=new_cmap, alpha=1, extend='both', transform=ccrs.PlateCarree())

        # t 检验
        sp  =  ax.contourf(lon, lat, parray, levels=[0.5, 1], colors='none', hatches=['..'], transform=ccrs.PlateCarree())

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        #topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='red', linewidth=4.5)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    cb.set_ticks(ct_level)
    cb.set_ticklabels(ct_level)

    plt.savefig("/data/paint/AerChemMIP_modelgroup_spatial_MJJAS_ssp370_ntcf_{}_northern_hemisphere.png".format(figname))


if __name__ == '__main__':
    f0  =  xr.open_dataset('/data/AerChemMIP/process/multiple_model_climate_pr_month_MJJAS.nc')

#    ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
#    ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

#    ttest     =  cal_student_ttest(ssp0, ntcf0)

    diff_avg, sign   =  cal_multiple_model_avg_modified(f0, 'ssp',  'sspntcf')
    #print(np.nanmax(diff_avg))
    #print(sign)

    # Note that the variable in the above is three-dimension while the first is the number os the year
    #levels    =  [-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
    #plot_change_wet_day(diff_avg*86400, 'pr (MJJAS)', 'pr (MJJAS)', f0.lon.data, f0.lat.data, sign, levels)
    levels    =  np.array([-10, -8, -6, -4, -2, -0.5, 0.5, 2, 4, 6, 8, 10])

    plot_change_wet_day_northern(diff_avg*100, 'pr (MJJAS)', 'pr (MJJAS)', f0.lon.data, f0.lat.data, sign, levels)