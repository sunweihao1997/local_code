'''
2023-12-8
This script is to calculate and paint the changes in PSL between 1900-1920 and 1940-1960, using ERA20C data
'''
import xarray as xr
import numpy as np
import sys
import matplotlib.pyplot as plt

module_path = '/Users/sunweihao/local_code/module'
sys.path.append(module_path)

from module_sun import set_cartopy_tick

periodA_1 = 1900 ; periodA_2 = 1920
periodB_1 = 1940 ; periodB_2 = 1960

file_path = '/Volumes/samssd/ERA20C/'
file_name = 'ERA20C_PSL_monthly_1900_2010.nc'

f0 = xr.open_dataset(file_path + file_name, engine='netcdf4')
#print(f0)

# ======================================== Part of calculation =========================================
def cal_JJAS_average_each_year(ncfile, varname):
    '''
        This function calculate JJAS-average and save to ncfile format
    '''
    # 1. Slice out JJAS data
    #ncfile_JJAS = ncfile.sel(time=ncfile.initial_time0_hours.dt.month.isin([6, 7, 8, 9])) # The name of the time dimension in ERA20C is initial_time0_hours

    lat = ncfile.g4_lat_1.data ; lon = ncfile.g4_lon_2.data

    #2. Claim the array for average
    JJAS_var = np.zeros((111, len(lat), len(lon))) # Totally 111 years from 1900 to 2010

    # 3. Calculating
    for i in range(111):
        #JJAS_var[i] = np.average(ncfile_JJAS[varname].data[i * 4 : i * 4 + 4], axis=0)

        JJAS_var[i] = np.average(ncfile[varname].data[i * 12 + 5 : i * 12 + 9], axis=0)


    ncfile_return  =  xr.Dataset(
        {
            "JJAS_PSL": (["time", "lat", "lon"], JJAS_var),
        },
        coords={
            "time": (["time"], np.linspace(1900, 1900+110, 111)),
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
        },
        )
    ncfile_return['JJAS_PSL'].attrs = ncfile[varname].attrs
    #
    
    return ncfile_return

def cal_JJAS_PSL_diff_between_periods(ncfile, varname, periodA_1, periodA_2, periodB_1, periodB_2):
    '''
        This function is to calculate the difference between two periods
    '''
    ncfile_p1 = ncfile.sel(time=slice(periodA_1, periodA_2))
    ncfile_p2 = ncfile.sel(time=slice(periodB_1, periodB_2))

    period_diff = np.average(ncfile_p2[varname].data, axis=0) - np.average(ncfile_p1[varname].data, axis=0)

    return period_diff

# ============================ Part2: painting ==============================================
def plot_slp_changes_two_period(data, ref_file, plot_name):
    '''This function is to plot difference among two periods'''
    import cartopy.crs as ccrs
    from cartopy.util import add_cyclic_point

    proj       =  ccrs.PlateCarree()
    ax         =  plt.subplot(projection=proj)

    # Tick settings
    cyclic_data_slp, cyclic_lon = add_cyclic_point(data, coord=ref_file['lon'].data)
    #set_cartopy_tick(ax=ax,extent=paint_class.extent,xticks=np.linspace(0,140,8,dtype=int),yticks=np.linspace(-10,70,9,dtype=int),nx=1,ny=1,labelsize=10.5)

    set_cartopy_tick(ax=ax,extent=[0, 150, 0, 80],xticks=np.linspace(0,150,6,dtype=int),yticks=np.linspace(0,80,9,dtype=int),nx=1,ny=1,labelsize=10)

    im  =  ax.contourf(cyclic_lon, ref_file['lat'].data, cyclic_data_slp, np.linspace(-80,80,9), cmap='coolwarm', alpha=1, extend='both')

    ax.coastlines(resolution='110m', lw=1.25)

    ax.set_title('1901-1920 to 1941-1960',fontsize=15)
    ax.set_title('ERA20C',loc='right', fontsize=15)

    #add_vector_legend(ax=ax, q=q, speed=0.25)
    plt.colorbar(im, orientation='horizontal')
    
    #plt.savefig('/exports/csce/datastore/geos/users/s2618078/paint/analysis_EU_aerosol_climate_effect/slp/{}_period_diff_JJA_Indian_UV.pdf'.format(plot_name), dpi=500)
    plt.savefig('test.png')

# ============================= Part3. Main ==============================================
def main():
    JJAS_PSL = cal_JJAS_average_each_year(ncfile=f0, varname='MSL_GDS4_SFC')

    JJAS_PSL_DIFF = cal_JJAS_PSL_diff_between_periods(ncfile=JJAS_PSL, varname='JJAS_PSL', periodA_1=1900, periodA_2=1920, periodB_1=1940, periodB_2=1960)

    plot_slp_changes_two_period(data=JJAS_PSL_DIFF, ref_file=JJAS_PSL, plot_name='a')

if __name__ == '__main__':
    main()