'''
2024-5-9
This script is to plot the MJJAS mean's uas vas and rlut
The purpose is to check the NTCF experiment's data
'''
import xarray as xr
import numpy as np
import os
from scipy.signal import butter, filtfilt
import xarray as xr
import numpy as np
import os
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

def band_pass_calculation(data, fs, low_frq, high_frq, order,):
    '''
        fs: sample freq
    '''
    lowcut  = 1/low_frq
    highcut = 1/high_frq

    b, a    = butter(N=order, Wn=[lowcut, highcut], btype='band', fs=fs)

    filtered_data = filtfilt(b, a, data)

    return filtered_data

def band_pass_array(data):
    # claim the array
    array0 = np.zeros(data.shape)

    # Loop for band_pass
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            array0[:, i, j] = band_pass_calculation(data[:, i, j], 1, 20, 8, 5)

    return array0

# =============== File Information =================
uas_file = xr.open_dataset('/home/sun/data/process/analysis/AerChem/uas_MJJAS_multiple_model_result.nc')
vas_file = xr.open_dataset('/home/sun/data/process/analysis/AerChem/vas_MJJAS_multiple_model_result.nc')
psl_file = xr.open_dataset('/home/sun/data/process/analysis/AerChem/psl_MJJAS_multiple_model_result.nc')
olr_file = xr.open_dataset('/home/sun/data/process/analysis/AerChem/rlut_MJJAS_multiple_model_result.nc')

uas      = [np.nanmean((np.nanmean(uas_file['hist_model'], axis=0)), axis=0), np.nanmean((np.nanmean(uas_file['ssp3_model'], axis=0)), axis=0), np.nanmean((np.nanmean(uas_file['ntcf_model'], axis=0)), axis=0)]
vas      = [np.nanmean((np.nanmean(vas_file['hist_model'], axis=0)), axis=0), np.nanmean((np.nanmean(vas_file['ssp3_model'], axis=0)), axis=0), np.nanmean((np.nanmean(vas_file['ntcf_model'], axis=0)), axis=0)]
psl      = [np.nanmean((np.nanmean(psl_file['hist_model'], axis=0)), axis=0), np.nanmean((np.nanmean(psl_file['ssp3_model'], axis=0)), axis=0), np.nanmean((np.nanmean(psl_file['ntcf_model'], axis=0)), axis=0)]
olr      = [np.nanmean((np.nanmean(olr_file['hist_model'], axis=0)), axis=0), np.nanmean((np.nanmean(olr_file['ssp3_model'], axis=0)), axis=0), np.nanmean((np.nanmean(olr_file['ntcf_model'], axis=0)), axis=0)]

# Save to ncfile
ncfile  =  xr.Dataset(
            {
                "uas_hist":     (["lat", "lon"], uas[0]),        
                "vas_hist":     (["lat", "lon"], vas[0]),        
                "psl_hist":     (["lat", "lon"], psl[0]),        
                "olr_hist":     (["lat", "lon"], olr[0]),

                "uas_ssp3":     (["lat", "lon"], uas[1]),        
                "vas_ssp3":     (["lat", "lon"], vas[1]),        
                "psl_ssp3":     (["lat", "lon"], psl[1]),        
                "olr_ssp3":     (["lat", "lon"], olr[1]),      

                "uas_ntcf":     (["lat", "lon"], uas[2]),        
                "vas_ntcf":     (["lat", "lon"], vas[2]),        
                "psl_ntcf":     (["lat", "lon"], psl[2]),        
                "olr_ntcf":     (["lat", "lon"], olr[2]),                
            },
            coords={
                "lat":  (["lat"],  uas_file.lat.data),
                "lon":  (["lon"],  uas_file.lon.data),
            },
            )
ncfile.attrs['description'] = 'Created on 9-May-2024 by paint_AerChemMIP_8to20_bandpass_circulation_MJJAS_240509.py. This is the 8-20 filtered data'

ncfile.to_netcdf('/home/sun/data/process/analysis/AerChem/AerChemMIP_MJJAS_mean_uas_vas_psl_olr.nc')

f0 = xr.open_dataset('/home/sun/data/process/analysis/AerChem/AerChemMIP_MJJAS_mean_uas_vas_psl_olr.nc')
lon = f0.lon.data
lat = f0.lat.data

def paint_ISV_track(uas, vas, rlut, figname):
    '''
        This function plot the propogation of the ISV
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    import sys
    sys.path.append("/home/sun/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,0,45
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------   Set Figure -----------
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(60,60))
    spec1   =  fig1.add_gridspec(nrows=3,ncols=1)

    j = 0
    # -------   Start painting -------
    # -------   Hist -----------------
    row=0
    # add subplot
    ax  =  fig1.add_subplot(spec1[0, 0], projection = proj)

    # set ticks
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=12)

    ax.coastlines(resolution='50m',lw=1.65)

    # OLR
    im1  =  ax.contourf(lon, lat, rlut[row],  np.linspace(-20, 20, 11), cmap='coolwarm', alpha=1, extend='both')

    # psl
    #im2  =  ax.contour(lon, lat, psl[0][row], np.linspace(-20, 20, 11), colors='grey', alpha=1,)
    #sp  =  ax.contourf(lon, lat, p[0, row], levels=[0., 0.05], colors='none', hatches=['..'])

    # wind
    q  =  ax.quiver(lon, lat, uas[row], vas[row], 
            regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
            scale_units='xy', scale=0.01,        # scale是参考矢量，所以取得越大画出来的箭头就越短
            units='xy', width=0.25,
            transform=proj,
            color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

    ax.set_title('MJJAS', fontsize=20, loc='left')
    ax.set_title('historical', fontsize=20, loc='right')

    # --------- SSP370 ------------------
    row = 1
    # add subplot
    ax  =  fig1.add_subplot(spec1[1, 0], projection = proj)

    # set ticks
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=12)

    ax.coastlines(resolution='50m',lw=1.65)

    # OLR
    im1  =  ax.contourf(lon, lat, rlut[row],  np.linspace(-20, 20, 11), cmap='coolwarm', alpha=1, extend='both')

    # psl
    #im2  =  ax.contour(lon, lat, psl[0][row], np.linspace(-20, 20, 11), colors='grey', alpha=1,)
    #sp  =  ax.contourf(lon, lat, p[0, row], levels=[0., 0.05], colors='none', hatches=['..'])

    # wind
    q  =  ax.quiver(lon, lat, uas[row], vas[row], 
            regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
            scale_units='xy', scale=0.01,        # scale是参考矢量，所以取得越大画出来的箭头就越短
            units='xy', width=0.25,
            transform=proj,
            color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

    ax.set_title('MJJAS', fontsize=20, loc='left')
    ax.set_title('SSP370', fontsize=20, loc='right')

    # --------- SSP370NTCF ------------------
    row = 2
    # add subplot
    ax  =  fig1.add_subplot(spec1[row, 0], projection = proj)

    # set ticks
    set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,120,7,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=12)

    ax.coastlines(resolution='50m',lw=1.65)

    # OLR
    im1  =  ax.contourf(lon, lat, rlut[row],  np.linspace(-20, 20, 11), cmap='coolwarm', alpha=1, extend='both')

    # psl
    #im2  =  ax.contour(lon, lat, psl[0][row], np.linspace(-20, 20, 11), colors='grey', alpha=1,)
    #sp  =  ax.contourf(lon, lat, p[0, row], levels=[0., 0.05], colors='none', hatches=['..'])

    # wind
    q  =  ax.quiver(lon, lat, uas[row], vas[row], 
            regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
            scale_units='xy', scale=0.01,        # scale是参考矢量，所以取得越大画出来的箭头就越短
            units='xy', width=0.25,
            transform=proj,
            color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

    ax.set_title('MJJAS', fontsize=20, loc='left')
    ax.set_title('SSP370', fontsize=20, loc='right')

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im1, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig('/home/sun/paint/AerMIP/' + figname)

uas = [f0['uas_ssp3'] - f0['uas_hist'], f0['uas_ntcf'] - f0['uas_hist'], f0['uas_ssp3'] - f0['uas_ntcf']]
vas = [f0['vas_ssp3'] - f0['vas_hist'], f0['vas_ntcf'] - f0['vas_hist'], f0['vas_ssp3'] - f0['vas_ntcf']]
psl = [f0['psl_ssp3'] - f0['psl_hist'], f0['psl_ntcf'] - f0['psl_hist'], f0['psl_ssp3'] - f0['psl_ntcf']]
olr = [f0['olr_ssp3'] - f0['olr_hist'], f0['olr_ntcf'] - f0['olr_hist'], f0['olr_ssp3'] - f0['olr_ntcf']]

#print(np.std(f0['uas_hist']))
paint_ISV_track(uas, vas, olr, 'check_data_diff.png')