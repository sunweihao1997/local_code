import xarray as xr
import numpy as np
from scipy import stats
from windspharm.xarray import VectorWind

f1 = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/ua_Amon_UKESM1-0-LL_ssp370-lowNTCF_r1i1p1f2.nc")
f2 = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/va_Amon_UKESM1-0-LL_ssp370-lowNTCF_r1i1p1f2.nc")

w      =  VectorWind(f1.sel(plev=20000)['ua'],  f2.sel(plev=20000)['va'])

u, v   =  w.irrotationalcomponent()
div    =  w.divergence()

print(div.shape)

def plot_change_wet_day(div, u, v, left_string, figname, lon, lat, parray, ct_level=np.linspace(-10., 10., 21),):

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
    pet        = [(div)]

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
        #sp  =  ax.contourf(lon, lat, parray, levels=[0., 0.1], colors='none', hatches=['.'])

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        #topo  =  ax.contour(gen_f['longitude'].data, gen_f['latitude'].data, z, levels=[3000], colors='red', linewidth=4.5)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

        # wind
        q  =  ax.quiver(lon, lat, u, v, 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=0.15,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=10)

    cb.set_ticks(ct_level)
    cb.set_ticklabels(ct_level)

    plt.savefig("/home/sun/paint/AerChemMIP/AerChemMIP_modelgroup_spatial_MJJAS_ssp370_ntcf_{}_climatology_check.png".format(figname))

levels    =  [-10, -8, -6, -4, -2, -0.05, 0.05, 2, 4, 6, 8, 10]
plot_change_wet_day(np.nanmean(div, axis=0) * 10e6, np.nanmean(u, axis=0), np.nanmean(v, axis=0), 'Div 200 hPa (MJJAS)', 'Div 200 hPa (MJJAS)', f1.lon.data, f1.lat.data, 0, levels)
