'''
2024-4-11
This script is to plot the water deficit under SSP370 and SSP370lowNTCF experiment
The water deficit is represented by the diff between Precipitation and Potential evaportranspiration
'''
import xarray as xr
import numpy as np

# =============== File information ================
data_path = '/data/AerChemMIP/process/'

pr_name   = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_precipitation_2015-2050_new.nc'
pet_name  = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_PET_2015-2050.nc'

pr_file   = xr.open_dataset(data_path + pr_name)
pet_file  = xr.open_dataset(data_path + pet_name)
mask_file = xr.open_dataset(data_path + 'ERA5_land_sea_mask_model-grid.nc')

lat       = pr_file.lat.data
lon       = pr_file.lon.data

year_list = np.linspace(2031, 2050, 2050 - 2031 + 1)
month_list= [6, 7, 8, 9]
# ==================================================

# --------------- Function1: calculate the JJAS mean ---------------------
def cal_seasonal_mean(ncfile0, varname, month_list, year_list,):
    # 1. Claim the averaged-array
    avg0  = np.zeros((len(lat), len(lon)))

    # 2. Select out the one year data
    year_num  =  len(year_list)

    for yy in year_list:
        ncfile0_1year = ncfile0.sel(time=ncfile0.time.dt.year.isin([yy]))

        # 3. Select out the months in the given list
        ncfile0_1year_month = ncfile0_1year.sel(time=ncfile0_1year.time.dt.month.isin(month_list))

        # 4. Calculate the seasonal mean and add it to the avg0
        avg0                += (np.average(ncfile0_1year_month[varname].data, axis=0) / year_num)

    avg0[mask_file['lsm'][0] < 0.1] = np.nan

    return avg0

# ---------------- The end of the Function1 -------------------------------

# --------------- Function2: Plot the water deficit ---------------------------------
def plot_wd_meanstate(wd_ssp, wd_ntcf,):
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    import sys
    sys.path.append("/root/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,-10,60
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(20,30))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=1)

    left_title = 'JJAS Water Deficit'
    right_title= ['SSP370', 'SSP370lowNTCF',]
    pet        = [wd_ssp, wd_ntcf, wd_ssp - wd_ntcf]
    ct_level   = np.linspace(-1000, 1000, 11)

    # ------      paint    -----------
    for row in range(2):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,60,8,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, pet[row] * 120, ct_level, cmap='coolwarm', alpha=1, extend='both')

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/modelgroup_spatial_JJAS_ssp370_ntcf_mean_state_water-deficit_Pr-PET.png")
    # ------------- End of the function2 -------------------------------------------------------

# ------------------ Function3: diff between SSP370 and SSP370lowNTCF ---------------------
def plot_wd_diff(wd_ssp, wd_ntcf,):
    #  ----- import  ----------
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    import sys
    sys.path.append("/root/local_code/module/")
    from module_sun import set_cartopy_tick

    # -------   cartopy extent  -----
    lonmin,lonmax,latmin,latmax  =  45,150,-10,60
    extent     =  [lonmin,lonmax,latmin,latmax]

    # -------     figure    -----------
    proj  =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(20,30))
    spec1   =  fig1.add_gridspec(nrows=2,ncols=1)

    left_title = 'JJAS Water Deficit'
    right_title= ['SSP370 - SSP370lowNTCF',]
    pet        = [wd_ssp - wd_ntcf]
    ct_level   = np.linspace(-70, 70, 15)

    # ------      paint    -----------
    for row in range(1):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,60,8,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, pet[row] * 120, ct_level, cmap='coolwarm', alpha=1, extend='both')

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/modelgroup_spatial_JJAS_ssp370_ntcf_diff_water-deficit_Pr-PET.png")
    # ------------- End of the function2 -------------------------------------------------------

if __name__ == '__main__':
    # ------------ Calculation -------------
    pr_ssp_jjas  = cal_seasonal_mean(pr_file,  'pr_ssp',  month_list, year_list)
    pet_ssp_jjas = cal_seasonal_mean(pet_file, 'pet_ssp', month_list, year_list)

    pr_ntcf_jjas  = cal_seasonal_mean(pr_file,  'pr_ntcf',  month_list, year_list)
    pet_ntcf_jjas = cal_seasonal_mean(pet_file, 'pet_ntcf', month_list, year_list)

    wd_ssp        = pr_ssp_jjas - pet_ssp_jjas
    wd_ntcf       = pr_ntcf_jjas - pet_ntcf_jjas

    # ------------ Paint -------------------
    plot_wd_meanstate(wd_ssp, wd_ntcf)
    plot_wd_diff(wd_ssp, wd_ntcf)