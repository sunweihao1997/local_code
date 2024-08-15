'''
2024-5-8
This script is to calculate and plot the track of the ISV for 8-20 and 20-70 band-pass result
'''
import xarray as xr
import numpy as np
import os
import re
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

# ============ File Information =============

data_path = '/home/sun/data/process/analysis/AerChem/'
file_list = os.listdir(data_path)

ref_file  = xr.open_dataset('/home/sun/data/process/analysis/AerChem/psl_MJJAS_multiple_model_result.nc')
lat       = ref_file.lat.data
lon       = ref_file.lon.data

correlation_file = xr.open_dataset(data_path + 'AerChemMIP_correlation_pvalue_PC_variable_uas_vas_psl_rlut_autocaliberate.nc')

# ===========================================

def sort_func(text):
    # 1. Split the string

    lagtext = text.split("_")[5]
    number  = re.findall(r'\d+', lagtext)


    return int(number[0])

def get_file_list_singlevar(varname, char0, char1):
    '''
        Because the raw data is messy, this function is to aggregate them 
    '''
    singlevar_list = []
    for ffff in file_list:
        if varname in ffff and char0 in ffff and char1 in ffff:
            singlevar_list.append(ffff)

    singlevar_list.sort()

    # Check the number
    #print(varname + ' ' + char0 + ' is ' + str(len(singlevar_list)))

    return singlevar_list

def aggregate_time_for_var(list0, time_length, varname,):
    '''
        This function is to aggregate the time axis for a single variable
    '''
    # 1. Claim the array to save the data
    new_var = np.zeros((time_length, len(lat), len(lon)))

    # 2. Sort list by day ( because the default sort method would generate wrong result )
    list0 = sorted(list0, key=sort_func)

    #print(f'The new list is {list0}')

    for i in range(time_length):
        f_i = xr.open_dataset(data_path + list0[i])

        new_var[i] = f_i[varname]

    # 3. Add it to dataarray
    var_array = xr.DataArray(data=new_var, dims=["day", "lat", "lon"],
                                    coords=dict(
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        day=(["day"], np.linspace(-12,12, 13)),
                                    ),
                                    )

    return var_array
                                    
# ================ Plot part ====================
def paint_ISV_track(uas, vas, rlut, psl, p, figname, levels, windscale, Day0 = np.linspace(-18,18, 13)):
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
    fig1    =  plt.figure(figsize=(60,90))
    spec1   =  fig1.add_gridspec(nrows=13,ncols=3)

    j = 0
    # -------   Start painting -------
    # -------   Hist -----------------
    for row in range(13):


        # add subplot
        ax  =  fig1.add_subplot(spec1[row, 0], projection = proj)

        # set ticks
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30, 135, 8,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=20)

        ax.coastlines(resolution='50m',lw=1.65)

        # OLR
        im1  =  ax.contourf(lon, lat, rlut[0][row], levels, cmap='coolwarm', alpha=1, extend='both')

        # psl
        #im2  =  ax.contour(lon, lat, psl[0][row], np.linspace(-20, 20, 11), colors='grey', alpha=1,)
        sp  =  ax.contourf(lon, lat, p[0, row], levels=[0., 0.05], colors='none', hatches=['..'])

        # wind
        q  =  ax.quiver(lon, lat, uas[0][row], vas[0][row], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=windscale,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

        ax.set_title(int(Day0[row]), fontsize=20, loc='left')
        ax.set_title('historical', fontsize=20, loc='right')

    # --------- SSP370 ------------------
    for row in range(13):

        # add subplot
        ax  =  fig1.add_subplot(spec1[row, 1], projection = proj)

        # set ticks
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30, 135, 8,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=20)

        ax.coastlines(resolution='50m',lw=1.65)

        # OLR
        im1  =  ax.contourf(lon, lat, rlut[1][row], levels, cmap='coolwarm', alpha=1, extend='both')

        # psl
        #im2  =  ax.contour(lon, lat, psl[1][row], np.linspace(-20, 20, 11), colors='grey', alpha=1,)
        sp  =  ax.contourf(lon, lat, p[1, row], levels=[0., 0.05], colors='none', hatches=['..'])

        # wind
        q  =  ax.quiver(lon, lat, uas[1][row], vas[1][row], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=windscale,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

        ax.set_title(int(Day0[row]), fontsize=20, loc='left')
        ax.set_title('SSP370', fontsize=20, loc='right')

    # --------- SSP370NTCF ------------------
    for row in range(13):

        # add subplot
        ax  =  fig1.add_subplot(spec1[row, 2], projection = proj)

        # set ticks
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30, 135, 8,dtype=int),yticks=np.linspace(0,60,7,dtype=int),nx=1,ny=1,labelsize=20)

        ax.coastlines(resolution='50m',lw=1.65)

        # OLR
        im1  =  ax.contourf(lon, lat, rlut[2][row], levels, cmap='coolwarm', alpha=1, extend='both')

        # psl
        #im2  =  ax.contour(lon, lat, psl[2][row], np.linspace(-20, 20, 11), colors='grey', alpha=1,)
        sp  =  ax.contourf(lon, lat, p[2, row], levels=[0., 0.05], colors='none', hatches=['.'])

        # wind
        q  =  ax.quiver(lon, lat, uas[2][row], vas[2][row], 
                regrid_shape=15, angles='uv',   # regrid_shape这个参数越小，是两门就越稀疏
                scale_units='xy', scale=windscale,        # scale是参考矢量，所以取得越大画出来的箭头就越短
                units='xy', width=0.25,
                transform=proj,
                color='k',linewidth=1.2,headlength = 5, headaxislength = 4, headwidth = 5,alpha=1)

        ax.set_title(int(Day0[row]), fontsize=20, loc='left')
        ax.set_title('SSP370lowNTCF', fontsize=20, loc='right')

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im1, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig('/home/sun/paint/AerMIP/' + figname)


if __name__ == '__main__':
    # 1. Get the file list for variables
    uas_list_high  = get_file_list_singlevar('uas', '8to20_pc1_lag', 'v2')
    uas_list_low   = get_file_list_singlevar('uas', '20to70_pc1_lag', 'v2')
    vas_list_high  = get_file_list_singlevar('vas', '8to20_pc1_lag', 'v2')
    vas_list_low   = get_file_list_singlevar('vas', '20to70_pc1_lag', 'v2')
    psl_list_high  = get_file_list_singlevar('psl', '8to20_pc1_lag', 'v2')
    psl_list_low   = get_file_list_singlevar('psl', '20to70_pc1_lag', 'v2')
    rlut_list_high = get_file_list_singlevar('rlut', '8to20_pc1_lag', 'v2')
    rlut_list_low  = get_file_list_singlevar('rlut', '20to70_pc1_lag', 'v2')



    # 2. Put them into one ncfile !! Finished, skip to Step 3 !!
#    ncfile0        = xr.Dataset()
#    # ------------------------- High Freq ----------------------------------
#    ncfile0["uas_high_hist"]  = aggregate_time_for_var(uas_list_high,  len(uas_list_high),  'rc_uas_hist')
#    ncfile0["vas_high_hist"]  = aggregate_time_for_var(vas_list_high,  len(vas_list_high),  'rc_uas_hist')
#    ncfile0["psl_high_hist"]  = aggregate_time_for_var(psl_list_high,  len(psl_list_high),  'rc_uas_hist')
#    ncfile0["rlut_high_hist"] = aggregate_time_for_var(rlut_list_high, len(rlut_list_high), 'rc_uas_hist')
#
#    ncfile0["uas_high_ssp"]  = aggregate_time_for_var(uas_list_high,  len(uas_list_high),  'rc_uas_ssp3')
#    ncfile0["vas_high_ssp"]  = aggregate_time_for_var(vas_list_high,  len(vas_list_high),  'rc_uas_ssp3')
#    ncfile0["psl_high_ssp"]  = aggregate_time_for_var(psl_list_high,  len(psl_list_high),  'rc_uas_ssp3')
#    ncfile0["rlut_high_ssp"] = aggregate_time_for_var(rlut_list_high, len(rlut_list_high), 'rc_uas_ssp3')
#
#    ncfile0["uas_high_ntcf"]  = aggregate_time_for_var(uas_list_high,  len(uas_list_high),  'rc_uas_ntcf')
#    ncfile0["vas_high_ntcf"]  = aggregate_time_for_var(vas_list_high,  len(vas_list_high),  'rc_uas_ntcf')
#    ncfile0["psl_high_ntcf"]  = aggregate_time_for_var(psl_list_high,  len(psl_list_high),  'rc_uas_ntcf')
#    ncfile0["rlut_high_ntcf"] = aggregate_time_for_var(rlut_list_high, len(rlut_list_high), 'rc_uas_ntcf')
#
#    # ----------------------- Low Freq ---------------------------------------
#    ncfile0["uas_low_hist"]  = aggregate_time_for_var(uas_list_low,  len(uas_list_low),  'rc_uas_hist')
#    ncfile0["vas_low_hist"]  = aggregate_time_for_var(vas_list_low,  len(vas_list_low),  'rc_uas_hist')
#    ncfile0["psl_low_hist"]  = aggregate_time_for_var(psl_list_low,  len(psl_list_low),  'rc_uas_hist')
#    ncfile0["rlut_low_hist"] = aggregate_time_for_var(rlut_list_low, len(rlut_list_low), 'rc_uas_hist')
#
#    ncfile0["uas_low_ssp"]  = aggregate_time_for_var(uas_list_low,  len(uas_list_low),  'rc_uas_ssp3')
#    ncfile0["vas_low_ssp"]  = aggregate_time_for_var(vas_list_low,  len(vas_list_low),  'rc_uas_ssp3')
#    ncfile0["psl_low_ssp"]  = aggregate_time_for_var(psl_list_low,  len(psl_list_low),  'rc_uas_ssp3')
#    ncfile0["rlut_low_ssp"] = aggregate_time_for_var(rlut_list_low, len(rlut_list_low), 'rc_uas_ssp3')
#
#    ncfile0["uas_low_ntcf"]  = aggregate_time_for_var(uas_list_low,  len(uas_list_low),  'rc_uas_ntcf')
#    ncfile0["vas_low_ntcf"]  = aggregate_time_for_var(vas_list_low,  len(vas_list_low),  'rc_uas_ntcf')
#    ncfile0["psl_low_ntcf"]  = aggregate_time_for_var(psl_list_low,  len(psl_list_low),  'rc_uas_ntcf')
#    ncfile0["rlut_low_ntcf"] = aggregate_time_for_var(rlut_list_low, len(rlut_list_low), 'rc_uas_ntcf')
#   #print(np.sum(np.isnan(ncfile0['vas_low_ntcf'].data[0, :, 0])))
#   #print(ncfile0["uas_low_hist"].shape)
#   #print(ncfile0['uas_low_hist'].data[0, :, 0])
#    ncfile0.to_netcdf(data_path + 'AerChemMIP_regression_uas_vas_psl_rlut_hist_ssp_ntcf.nc')

    # 3. Plot the result
    f1 = xr.open_dataset(data_path + 'AerChemMIP_regression_uas_vas_psl_rlut_hist_ssp_ntcf.nc')


    # 3.1 Investigate the unit
    # psl: Pa ; rlut: W m-2

    # 3.2 Painting
    paint_ISV_track([-1*f1['uas_low_hist'].data,  -1*f1['uas_low_ssp'].data,  -1*f1['uas_low_ntcf'].data], 
                    [-1*f1['vas_low_hist'].data,  -1*f1['vas_low_ssp'].data,  -1*f1['vas_low_ntcf'].data], 
                    [-1*f1['rlut_low_hist'].data, -1*f1['rlut_low_ssp'].data, -1*f1['rlut_low_ntcf'].data], 
                    [-1*f1['psl_low_hist'].data,  -1*f1['psl_low_ssp'].data,  -1*f1['psl_low_ntcf'].data], 
                    correlation_file['rlutp_fi'][:, 1, ::-1],
                    figname='low-frq-1day.pdf',
                    levels=np.linspace(-3, 3, 13),
                    windscale=0.03,
                    Day0 = np.linspace(-6,6,13)
                    )

    paint_ISV_track([f1['uas_high_hist'].data,   -1*f1['uas_high_ssp'].data, f1['uas_high_ntcf'].data], 
                    [f1['vas_high_hist'].data,   -1*f1['vas_high_ssp'].data, f1['vas_high_ntcf'].data], 
                    [f1['rlut_high_hist'].data,  -1*f1['rlut_high_ssp'].data, f1['rlut_high_ntcf'].data], 
                    [f1['psl_high_hist'].data,   -1*f1['psl_high_ssp'].data,  f1['psl_high_ntcf'].data], 
                    correlation_file['rlutp_bh'][:, 0, ::-1],
                    figname='high-frq-1day.pdf',
                    levels=np.linspace(-1.5, 1.5, 13),
                    windscale=0.02,
                    Day0=np.linspace(-6,6,13)
                    )
#print(np.nanmin(correlation_file['rlutp_bh']))