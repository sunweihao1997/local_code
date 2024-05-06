'''
2024-4-16
This script is to plot the changes in the wetdays between SSP370 and SSP370lowNTCF, comparing with the historical simulation
'''
import xarray as xr
import numpy as np
import os

path_in   =  '/home/sun/data/process/analysis/AerChem/heat_wave/result_regrid/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ] # GISS provide no daily data

type0        = ['hw_tasmin', 'hw_tasmax',]

mask_file    = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid.nc')


def cal_multiple_model_avg(list0,):
    '''
     This function calculate the model-average and single model average
     list0 is all the files under the path
    '''
    # 1. Claim an empty Dataset
    model_set = xr.Dataset()

    # 1.1 Claim the array to save all the model result
    hist_hw_tasmin0 = np.zeros((len(models_label), 3, 50, 121, 241))
    hist_hw_tasmax0 = np.zeros((len(models_label), 3, 50, 121, 241))
    ssp_hw_tasmin0  = np.zeros((len(models_label), 3, 36, 121, 241))
    ssp_hw_tasmax0  = np.zeros((len(models_label), 3, 36, 121, 241))
    ntcf_hw_tasmin0 = np.zeros((len(models_label), 3, 36, 121, 241))
    ntcf_hw_tasmax0 = np.zeros((len(models_label), 3, 36, 121, 241))


    # 2. for each model, calculate its average among the realization
    # 2.1 Select out the single realization subset
    j = 0 # number for model
    for model0 in models_label:
        model_subset  =  [element for element in list0 if model0 in element]

        # 2.2 ref file provides lat/lon information
        ref_file      =  xr.open_dataset(path_in + model_subset[0])
        lat           =  ref_file.lat.data ; lon      = ref_file.lon.data ; time0         = ref_file.time0.data ; time1       =  ref_file.time1.data ; time2       = ref_file.time2.data

        realization_number = len(model_subset)

        print(f'Now it is calculating the single-model average for {model0}, which includes {realization_number}')

        # 3 Claim the averaged array
        hist_hw_tasmin1 = np.zeros((3, len(time0), len(lat), len(lon)))
        hist_hw_tasmax1 = np.zeros((3, len(time0), len(lat), len(lon)))
        ssp_hw_tasmin1  = np.zeros((3, len(time1), len(lat), len(lon)))
        ssp_hw_tasmax1  = np.zeros((3, len(time1), len(lat), len(lon)))
        ntcf_hw_tasmin1 = np.zeros((3, len(time2), len(lat), len(lon)))
        ntcf_hw_tasmax1 = np.zeros((3, len(time2), len(lat), len(lon)))

        for i in range(realization_number):
            f_realization = xr.open_dataset(path_in + model_subset[i])

            hist_hw_tasmin1 += (f_realization['hist_hw_tasmin'].data / realization_number)
            hist_hw_tasmax1 += (f_realization['hist_hw_tasmax'].data / realization_number)
            ssp_hw_tasmin1  += (f_realization['ssp_hw_tasmin'].data  / realization_number)
            ssp_hw_tasmax1  += (f_realization['ssp_hw_tasmax'].data  / realization_number)
            ntcf_hw_tasmin1 += (f_realization['ntcf_hw_tasmin'].data / realization_number)
            ntcf_hw_tasmax1 += (f_realization['ntcf_hw_tasmax'].data / realization_number)
        
        # Now the single model realization-average is completed
        hist_hw_tasmin0[j]  =  hist_hw_tasmin1
        hist_hw_tasmax0[j]  =  hist_hw_tasmax1
        ssp_hw_tasmin0[j]   =  ssp_hw_tasmin1
        ssp_hw_tasmax0[j]   =  ssp_hw_tasmax1
        ntcf_hw_tasmin0[j]  =  ntcf_hw_tasmin1
        ntcf_hw_tasmax0[j]  =  ntcf_hw_tasmax1

        j+=1

    hist_hw_tasmin_multimodel = xr.DataArray(data=hist_hw_tasmin0, dims=["models", "info", "time_hist", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time_hist=(["time_hist"], time0),
                                        info=(["info"], f_realization['info'].data)
                                    ),
                                    attrs=dict(
                                        description="heatwave",
                                    ),
                                    )
    hist_hw_tasmax_multimodel = xr.DataArray(data=hist_hw_tasmax0, dims=["models", "info", "time_hist", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time_hist=(["time_hist"], time0),
                                        info=(["info"], f_realization['info'].data)
                                    ),
                                    attrs=dict(
                                        description="heatwave",
                                    ),
                                    )
    ssp_hw_tasmin_multimodel  = xr.DataArray(data=ssp_hw_tasmin0, dims=["models", "info", "time_furture", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time_furture=(["time_furture"], time1),
                                        info=(["info"], f_realization['info'].data)
                                    ),
                                    attrs=dict(
                                        description="heatwave",
                                    ),
                                    )
    ssp_hw_tasmax_multimodel  = xr.DataArray(data=ssp_hw_tasmax0, dims=["models", "info", "time_furture", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time_furture=(["time_furture"], time1),
                                        info=(["info"], f_realization['info'].data)
                                    ),
                                    attrs=dict(
                                        description="heatwave",
                                    ),
                                    )
    ntcf_hw_tasmin_multimodel  = xr.DataArray(data=ntcf_hw_tasmin0, dims=["models", "info", "time_furture", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time_furture=(["time_furture"], time1),
                                        info=(["info"], f_realization['info'].data)
                                    ),
                                    attrs=dict(
                                        description="heatwave",
                                    ),
                                    )
    ntcf_hw_tasmax_multimodel  = xr.DataArray(data=ntcf_hw_tasmax0, dims=["models", "info", "time_furture", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time_furture=(["time_furture"], time1),
                                        info=(["info"], f_realization['info'].data)
                                    ),
                                    attrs=dict(
                                        description="heatwave",
                                    ),
                                    )
    
    model_set.update({"hist_hw_tasmin_multimodel":hist_hw_tasmin_multimodel, "hist_hw_tasmax_multimodel":hist_hw_tasmax_multimodel, "ssp_hw_tasmin_multimodel":ssp_hw_tasmin_multimodel, "ssp_hw_tasmax_multimodel":ssp_hw_tasmax_multimodel, "ntcf_hw_tasmin_multimodel":ntcf_hw_tasmin_multimodel, "ntcf_hw_tasmax_multimodel":ntcf_hw_tasmax_multimodel})

            
    return model_set



def plot_change_hw_day(hist, ssp, sspntcf, left_string, figname, lon, lat, ct_level=np.linspace(-10., 10., 21)):
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
    right_title= ['Hist', 'SSP370', 'SSPlowNTCF']

    pet        = [(hist), (ssp), (sspntcf)]
    # Mask the value over ocean
    pet[0][mask_file['lsm'].data[0] < 0.05] = np.nan
    pet[1][mask_file['lsm'].data[0] < 0.05] = np.nan
    pet[2][mask_file['lsm'].data[0] < 0.05] = np.nan

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

    plt.savefig("/home/sun/paint/AerMIP/AerChemMIP_modelgroup_spatial_JJAS_hist_ssp370_ntcf_{}.png".format(figname))

def plot_change_hw_attribute(hist, ssp, sspntcf, left_string, figname, lon, lat, ct_level=np.linspace(-10., 10., 21)):
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
    right_title= ['Hist', 'SSP370', 'SSP370lowNTCF']

    pet        = [(hist), (ssp), (sspntcf)]
    # Mask the value over ocean
    pet[0][mask_file['lsm'].data[0] < 0.05] = np.nan
    pet[1][mask_file['lsm'].data[0] < 0.05] = np.nan
    pet[2][mask_file['lsm'].data[0] < 0.05] = np.nan


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

    plt.savefig("/home/sun/paint/AerMIP/AerChemMIP_modelgroup_spatial_JJAS_hist_ssp370_ntcf_meanstate_{}.png".format(figname))

if __name__ == '__main__':
    file_all = os.listdir(path_in)

    model_set = cal_multiple_model_avg(file_all)

    lat = np.linspace(-90, 90, 121)
    lon = np.linspace(0, 360, 241)

    plot_change_hw_day(np.nanmean(np.nanmean(model_set['hist_hw_tasmin_multimodel'].data[:, 0, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ssp_hw_tasmin_multimodel'].data[:, 0, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ntcf_hw_tasmin_multimodel'].data[:, 0, -20:], axis=0), axis=0), 'Heat Wave events (tasmin)', 'Heat Wave events (tasmin)', lon, lat, np.linspace(-3., 3., 13))
    plot_change_hw_day(np.nanmean(np.nanmean(model_set['hist_hw_tasmax_multimodel'].data[:, 0, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ssp_hw_tasmax_multimodel'].data[:, 0, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ntcf_hw_tasmax_multimodel'].data[:, 0, -20:], axis=0), axis=0), 'Heat Wave events (tasmax)', 'Heat Wave events (tasmax)', lon, lat, np.linspace(-3., 3., 13))

    plot_change_hw_day(np.nanmean(np.nanmean(model_set['hist_hw_tasmin_multimodel'].data[:, 1, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ssp_hw_tasmin_multimodel'].data[:, 1, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ntcf_hw_tasmin_multimodel'].data[:, 1, -20:], axis=0), axis=0), 'Heat Wave duration (tasmin)', 'Heat Wave duration (tasmin)', lon, lat, np.linspace(-20., 20., 11))
    plot_change_hw_day(np.nanmean(np.nanmean(model_set['hist_hw_tasmax_multimodel'].data[:, 1, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ssp_hw_tasmax_multimodel'].data[:, 1, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ntcf_hw_tasmax_multimodel'].data[:, 1, -20:], axis=0), axis=0), 'Heat Wave duration (tasmax)', 'Heat Wave duration (tasmax)', lon, lat, np.linspace(-20., 20., 11))

    plot_change_hw_attribute(np.nanmean(np.nanmean(model_set['hist_hw_tasmin_multimodel'].data[:, 2, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ssp_hw_tasmin_multimodel'].data[:, 2, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ntcf_hw_tasmin_multimodel'].data[:, 2, -20:], axis=0), axis=0), 'Heat Wave intensity (tasmin)', 'Heat Wave intensity (tasmin)', lon, lat, np.linspace(-10., 10., 11))
    plot_change_hw_attribute(np.nanmean(np.nanmean(model_set['hist_hw_tasmax_multimodel'].data[:, 2, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ssp_hw_tasmax_multimodel'].data[:, 2, -20:], axis=0), axis=0), np.nanmean(np.nanmean(model_set['ntcf_hw_tasmax_multimodel'].data[:, 2, -20:], axis=0), axis=0), 'Heat Wave intensity (tasmax)', 'Heat Wave intensity (tasmax)', lon, lat, np.linspace(-10., 10., 11))
