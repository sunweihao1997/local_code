'''
2024-4-28
This script is to plot the changes in the summer ISV intensity under SSP370 and SSP370lowNTCF experiment

The shape is 91 for lat and 181 for lon
'''
import xarray as xr
import numpy as np
import os
import matplotlib.patches as patches

# =============== File Information =================
path_in = '/home/sun/data/process/analysis/AerChem/ISV1/'

file_list = os.listdir(path_in) ; file_list.sort()

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ] # GISS provide no daily data

mask_file    = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid2x2.nc')

# ==================================================

# Calculate the average among the models

def cal_multiple_model_avg(list0,):
    '''
     This function calculate the model-average and single model average
     list0 is all the files under the path
    '''
    # 1. Claim an empty Dataset
    model_set = xr.Dataset()

    # 1.1 Claim the array to save all the model result
    hist_isv = np.zeros((len(models_label), 91, 181))
    ssp3_isv = np.zeros((len(models_label), 91, 181))
    ntcf_isv = np.zeros((len(models_label), 91, 181))


    # 2. for each model, calculate its average among the realization
    # 2.1 Select out the single realization subset
    j = 0 # number for model
    for model0 in models_label:
        model_subset  =  [element for element in list0 if model0 in element]

        # 2.2 ref file provides lat/lon information
        ref_file      =  xr.open_dataset(path_in + model_subset[0])
        lat           =  ref_file.lat.data ; lon      = ref_file.lon.data

        realization_number = len(model_subset) / 3

        print(f'Now it is calculating the single-model average for {model0}, which includes {realization_number}')

        # 3 Claim the averaged array
        hist_isv1 = np.zeros((len(lat), len(lon)))
        ssp3_isv1 = np.zeros((len(lat), len(lon)))
        ntcf_isv1 = np.zeros((len(lat), len(lon)))

        for i in range(int(len(model_subset))):
            #print(model_subset[i])
            f_realization = xr.open_dataset(path_in + model_subset[i])

            if 'historical' in model_subset[i]:
                #print('it is historical')
                hist_isv1 += (f_realization['MJJAS_isv'].data / realization_number)

            elif 'SSP370' in model_subset[i] and 'SSP370NTCF' not in model_subset[i]:
                ssp3_isv1 += (f_realization['MJJAS_isv'].data / realization_number)

            else:
                ntcf_isv1 += (f_realization['MJJAS_isv'].data / realization_number)

        
        # Now the single model realization-average is completed
        hist_isv[j] = hist_isv1
        ssp3_isv[j] = ssp3_isv1
        ntcf_isv[j] = ntcf_isv1

        j+=1

    hist_multimodel = xr.DataArray(data=hist_isv, dims=["models", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                    ),
                                    attrs=dict(
                                        description="historical ISV intensity for 1985-2014",
                                    ),
                                    )
    ssp_multimodel = xr.DataArray(data=ssp3_isv, dims=["models", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                    ),
                                    attrs=dict(
                                        description="SSP370 ISV intensity for 2031-2050",
                                    ),
                                    )
    ntcf_multimodel  = xr.DataArray(data=ntcf_isv, dims=["models", "lat", "lon"],
                                    coords=dict(
                                        models=(["models"], models_label),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                    ),
                                    attrs=dict(
                                        description="SSP370lowNTCF ISV intensity for 2031-2050",
                                    ),
                                    )

    print(np.nanmean(ssp3_isv))
    model_set.update({"hist_multimodel":hist_multimodel, "ssp_multimodel":ssp_multimodel, "ntcf_multimodel":ntcf_multimodel,})

            
    return model_set

# Plot the pictures
def plot_change_hw_day(hist, ssp, sspntcf, left_string, figname, lon, lat, ct_level=np.linspace(0., 10., 21)):
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

    left_title = '{} '.format(left_string)
    right_title= ['SSP370 - Hist', 'SSP370lowNTCF - Hist', 'SSP370 - SSP370lowNTCF']
    #right_title= ['Hist', 'SSP370', 'SSP370lowNTCF']

    pet        = [(ssp - hist), (sspntcf - hist), (ssp - sspntcf)]
#    pet        = [(ssp - hist), (sspntcf - hist), (ssp - sspntcf)]
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

    # --------- Add rectangle for three regions --------------
    points_indian = (70, 15)
    points_indo   = (95, 10)
    points_ea     = (105, 22.5)

#    rect_indian = patches.Rectangle(points_indian, 15, 10, linewidth=3.5, edgecolor='r', facecolor='none')
#    ax.add_patch(rect_indian)
#
#    rect_indo    = patches.Rectangle(points_indo, 15, 10, linewidth=3.5, edgecolor='purple', facecolor='none')
#    ax.add_patch(rect_indo)
#
#    rect_ea      = patches.Rectangle(points_ea, 15, 10, linewidth=3.5, edgecolor='yellow', facecolor='none')
#    ax.add_patch(rect_ea)


    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/home/sun/paint/AerMIP/AerChemMIP_modelgroup_spatial_JJAS_hist_ssp370_ntcf_{}.png".format(figname))

if __name__ == '__main__':
    # Calculation
    model_set = cal_multiple_model_avg(file_list)

    # Plot
    plot_change_hw_day(np.nanmean(model_set['hist_multimodel'].data, axis=0), np.nanmean(model_set['ssp_multimodel'].data, axis=0), np.nanmean(model_set['ntcf_multimodel'].data, axis=0), '8-20 ISV intensity (MJJAS)', '8-20 ISV intensity (MJJAS) meanstate', model_set.lon.data, model_set.lat.data, np.linspace(-1., 1., 21))
