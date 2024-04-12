'''
2024-4-10
This script is to calculate the JJAS mean Potential evaportranspiration over Asia
'''
import xarray as xr
import numpy as np

# ============== File Information ====================
data_path = '/data/AerChemMIP/process/'
data_name = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_PETADV_2015-2050.nc'
mask_name = 'ERA5_land_sea_mask_model-grid.nc'

pet_file  = xr.open_dataset(data_path + data_name)

# Here use the all PET to be the baseline
pet_file_base = xr.open_dataset(data_path + 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_PET_2015-2050.nc')

mask_file = xr.open_dataset(data_path + mask_name)

lat       = pet_file.lat.data
lon       = pet_file.lon.data
# ====================================================

# -------------- Function1 : calculate the JJAS mean --------------------
def cal_JJAS(nc0, varname, year_list):
    # Define the time range
    mon_list = [6, 7, 8, 9]

    # 1. Select the summer month
    nc_summer = nc0.sel(time=nc0.time.dt.month.isin(mon_list))
#    print(f'The number of summer months is {len(nc_summer.time.data)}')

    # 2. Claim the array for averaged result
    pet_summer = np.zeros((len(lat), len(lon)))

    # 3. Start calculating: 1. extract one-year's data
#    print(f'It includes years {len(year_list)}')
    for yy in year_list:

        nc_summer_1year = nc_summer.sel(time=nc_summer.time.dt.year.isin([yy]))

#        print(np.nanmean(nc_summer_1year[varname],))
        pet_summer      += (np.average(nc_summer_1year[varname], axis=0) / len(year_list))

    # 4. Mask the data over Ocean
    pet_summer[mask_file['lsm'].data[0] < 0.05] = np.nan
#    print(np.nanmean(pet_summer))
    return pet_summer

def cal_JJAS_hist(nc0, varname, year_list):
    # Define the time range
    mon_list = [6, 7, 8, 9]

    # 1. Select the summer month
    nc_summer = nc0.sel(time_hist=nc0.time_hist.dt.month.isin(mon_list))
#    print(f'The number of summer months is {len(nc_summer.time.data)}')

    # 2. Claim the array for averaged result
    pet_summer = np.zeros((len(lat), len(lon)))

    # 3. Start calculating: 1. extract one-year's data
#    print(f'It includes years {len(year_list)}')
    for yy in year_list:

        nc_summer_1year = nc_summer.sel(time_hist=nc_summer.time_hist.dt.year.isin([yy]))

        print(np.nanmean(nc_summer_1year[varname],))
        pet_summer      += (np.average(nc_summer_1year[varname], axis=0) / len(year_list))

    # 4. Mask the data over Ocean
    pet_summer[mask_file['lsm'].data[0] < 0.05] = np.nan
#    print(np.nanmean(pet_summer))
    return pet_summer

# --------------- End of the Function1 ------------------------------------

# --------------- Function2: Plot the PET ---------------------------------
def plot_pet(pet_hist, pet_ssp, pet_ntcf,):
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
    spec1   =  fig1.add_gridspec(nrows=3,ncols=1)

    left_title = 'JJAS (advection)'
    right_title= ['SSP370 - Hist', 'SSP370lowNTCF - SSP370', 'SSP370 - SSP370lowNTCF']
    pet        = [(pet_ssp - pet_hist) / pet_hist, (pet_ntcf - pet_hist) / pet_hist, (pet_ssp - pet_ntcf) /  pet_hist]
    ct_level   = np.linspace(-10, 10, 11)

    # ------      paint    -----------
    for row in range(3):
        col = 0
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,60,8,dtype=int),nx=1,ny=1,labelsize=25)

        # 添加赤道线
        ax.plot([40,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, pet[row] * 100, ct_level, cmap='coolwarm', alpha=1, extend='both')

        # 海岸线
        ax.coastlines(resolution='50m',lw=1.65)

        ax.set_title(left_title, loc='left', fontsize=16.5)
        ax.set_title(right_title[row], loc='right', fontsize=16.5)

    # 加colorbar
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)

    plt.savefig("/data/paint/modelgroup_spatial_JJAS_hist_ssp370_ntcf_diff_PETADV.pdf")


def main():
    # Get the 2031-2050 period-averaged data for SSP370 and SSp370lowNTCF and 1980-2015 for historical
    pet_ssp   =  cal_JJAS(pet_file, 'pet_adv_ssp',  np.linspace(2031, 2050, 2050 - 2031 + 1))
    pet_ntcf  =  cal_JJAS(pet_file, 'pet_adv_ntcf', np.linspace(2031, 2050, 2050 - 2031 + 1))
    pet_hist  =  cal_JJAS_hist(pet_file_base, 'pet_hist', np.linspace(1980, 2014, 2014 - 1980 + 1)) 

#    print(np.nanmean(pet_hist))
#    print(np.nanmean(pet_ssp))
    plot_pet(pet_hist, pet_ssp, pet_ntcf)

if __name__ == '__main__':
    main()

# ------------ Test area ----------------
#print(np.nanmean(pet_file['pet_hist'][-30:].data))
#print(np.nanmean(pet_file['pet_ssp'][-30:].data))