'''
2023-11-27
This script is to plot the difference between two period using the data from the CESM output
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys
from scipy import stats

module_path = "/home/sun/local_code/module"
sys.path.append(module_path)
from module_sun import *

f0 = xr.open_dataset("/mnt/d/samssd/precipitation/processed/EUI_CESM_fixEU_precipitation_difference_period_1901_1960_JJAS.nc")
f1 = xr.open_dataset("/mnt/d/samssd/precipitation/processed/EUI_CESM_BTAL_precipitation_difference_period_1901_1960_JJAS.nc")

#print(f0)

lat = f0.lat.data
lon = f0.lon.data


def calculate_student_t_test(period1, period2):
    '''This function loop every grid, calculate this year anomaly and do student-t test'''
#    BTAL_JJAS_precipitation = xr.open_dataset('/mnt/d/samssd/precipitation/CESM/ensemble_JJAS/CESM_BTAL_esemble_JJAS_precipitation.nc')
#    noEU_JJAS_precipitation = xr.open_dataset('/mnt/d/samssd/precipitation/CESM/ensemble_JJAS/CESM_noEU_esemble_JJAS_precipitation.nc')
#
#    time = BTAL_JJAS_precipitation.time.data
#
#    # Claim array to save the anomaly for each year
#    # Notice: Here I only calculate ensemble-mean!
#    anomaly_BTAL = np.zeros((len(time), len(lat), len(lon)))
#    anomaly_noEU = np.zeros((len(time), len(lat), len(lon)))
#
#    for i in range(len(lat)):
#        print(i)
#        for j in range(len(lon)):
#            # This point climatology precipitation
#            climatology_BTAL = (np.average(BTAL_JJAS_precipitation['JJAS_prect_1'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_2'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_3'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_4'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_5'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_6'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_7'].data[:, i, j], axis=0) + np.average(BTAL_JJAS_precipitation['JJAS_prect_8'].data[:, i, j], axis=0)) / 8
#            climatology_noEU = (np.average(noEU_JJAS_precipitation['JJAS_prect_1'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_2'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_3'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_4'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_5'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_6'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_7'].data[:, i, j], axis=0) + np.average(noEU_JJAS_precipitation['JJAS_prect_8'].data[:, i, j], axis=0)) / 8
#            for tt in range(157):
#                #print(tt)
#                anomaly_BTAL[tt, i, j] = ((BTAL_JJAS_precipitation['JJAS_prect_1'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_2'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_3'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_4'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_5'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_6'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_7'].data[tt, i, j] + BTAL_JJAS_precipitation['JJAS_prect_8'].data[tt, i, j]) / 8) - climatology_BTAL
#                anomaly_noEU[tt, i, j] = ((noEU_JJAS_precipitation['JJAS_prect_1'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_2'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_3'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_4'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_5'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_6'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_7'].data[tt, i, j] + noEU_JJAS_precipitation['JJAS_prect_8'].data[tt, i, j]) / 8) - climatology_noEU
#
#    print('Climatology and anomaly calculate successfully!')
#    # save to the ncfile
#    ncfile  =  xr.Dataset(
#        {
#            #"climatology_BTAL": (["lat", "lon"], climatology_BTAL),
#            #"climatology_noEU": (["lat", "lon"], climatology_noEU),
#            "anomaly_BTAL":     (["time", "lat", "lon"], anomaly_BTAL),
#            "anomaly_noEU":     (["time", "lat", "lon"], anomaly_noEU),
#        },
#        coords={
#            "time":  (["time"],  time),
#            "lon":   (["lon"],   lon),
#            "lat":   (["lat"],   lat),
#        },
#        )
#    
#    ncfile.to_netcdf("/mnt/d/samssd/precipitation/processed/EUI_CESM_BTAL_fixEU_JJAS_precipitation_anomaly_150years")
    ncfile = xr.open_dataset("/mnt/d/samssd/precipitation/processed/EUI_CESM_BTAL_fixEU_JJAS_precipitation_anomaly_150years")
    # calculate t-test for the given period
    ncfile_select = ncfile.sel(time=slice(period1, period2))
    p_value       = np.zeros((len(lat), len(lon)))
    for ii in range(len(lat)):
        for jj in range(len(lon)):
            a,b  = stats.ttest_ind(ncfile_select['anomaly_BTAL'].data[:, ii, jj], ncfile_select['anomaly_noEU'].data[:, ii, jj], equal_var=False)
            p_value[ii, jj] = b

    ncfile['p_value'] = xr.DataArray(
                            data=p_value,
                            dims=["lat", "lon"],
                            coords=dict(
                                lon=(["lon"], lon),
                                lat=(["lat"], lat),
                            ),
                        )

    # Save to the ncfile
    ncfile.to_netcdf("/mnt/d/samssd/precipitation/processed/EUI_CESM_BTAL_fixEU_JJAS_precipitation_anomaly_150years_and_ttest_1940_to_1960.nc")


def plot_diff_rainfall(extent, pvalue):
    '''This function plot the difference in precipitation'''
    # ------------ 2. Paint the Pic --------------------------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    # 2.2 Set the figure
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(15,12))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    #levels  =  np.linspace(-1.2, 1.2, 25)
    levels = np.array([-1.8, -1.5, -1.2, -0.9, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.2, 1.5, 1.8])


    # ------------ First. Paint the All forcing picture ------------
    ax1 = fig1.add_subplot(spec1[0, 0], projection=proj)

    # Tick setting
    set_cartopy_tick(ax=ax1,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,40,6,dtype=int),nx=1,ny=1,labelsize=25)

    # Equator line
    ax1.plot([40,120],[0,0],'k--')

    # Set ylabel name
    ax1.set_ylabel('ALL_Forcing - Fix_EU', fontsize=25)

    # Set title
    ax1.set_title('1941to1960 - 1901to1920', fontsize=25)

    # Shading for precipitation
    im1  =  ax1.contourf(f0['lon'].data, f0['lat'].data, np.average(f1['JJAS_prect_diff'], axis=0) - np.average(f0['JJAS_prect_diff'], axis=0), levels=levels, cmap='bwr_r', alpha=1, extend='both')

    dot  =  ax1.contourf(f0['lon'].data, f0['lat'].data, pvalue, levels=[0., 0.1], colors='none', hatches=['//'])

    # Coast Line
    ax1.coastlines(resolution='110m', lw=1.75)

    # ========= add colorbar =================
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im1, cax=cbar_ax, shrink=0.5, pad=0.01, orientation='horizontal')
    cb.ax.set_xticks([-1.8, -1.5, -1.2, -0.9, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.2, 1.5, 1.8])
    cb.ax.tick_params(labelsize=15, rotation=45)

    plt.savefig('/mnt/d/samssd/paint/EUI_CESM_All_Forcing_subtract_fixEU_precipitation_difference_1900_1960_stippling.png', dpi=500)
    #plt.savefig('test.png', dpi=500)

lonmin,lonmax,latmin,latmax  =  40,115,-10,40
extent     =  [lonmin,lonmax,latmin,latmax]


calculate_student_t_test(period1=1945, period2=1960)
p_file = xr.open_dataset("/mnt/d/samssd/precipitation/processed/EUI_CESM_BTAL_fixEU_JJAS_precipitation_anomaly_150years_and_ttest_1940_to_1960.nc")
plot_diff_rainfall(extent, pvalue=p_file['p_value'].data)