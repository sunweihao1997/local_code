'''
2023-12-11
This script is to calculate and paint the changes in Skin Temperature between 1900-1920 and 1940-1960, using CR20 data
'''
import xarray as xr
import numpy as np
import sys
import matplotlib.pyplot as plt

#module_path = '/Users/sunweihao/local_code/module'
module_path = '/home/sun/local_code/module'
sys.path.append(module_path)

from module_sun import set_cartopy_tick

periodA_1 = 1900 ; periodA_2 = 1920
periodB_1 = 1940 ; periodB_2 = 1960

#file_path = '/Volumes/samssd/'
file_path = '/mnt/e/'
file_name = 'skt.mon.mean.nc'

f0 = xr.open_dataset(file_path + file_name)
#print(f0)

# ======================================== Part of calculation =========================================
def cal_JJAS_average_each_year(ncfile, varname):
    '''
        This function calculate JJAS-average and save to ncfile format
    '''
    # 1. Slice out JJAS data
    #ncfile_JJAS = ncfile.sel(time=ncfile.time.dt.month.isin([6, 7, 8, 9])) # The name of the time dimension in ERA20C is initial_time0_hours
    ncfile_JJAS = ncfile.sel(time=ncfile.time.dt.month.isin([6, 7, 8, 9]))
    
    lat = ncfile.lat.data ; lon = ncfile.lon.data ; time = ncfile.time.data

    #2. Claim the array for average

    JJAS_var = np.zeros((len(time), len(lat), len(lon))) # Totally 111 years from 1900 to 2010

    # 3. Calculating
    for i in range(len(time)):
        JJAS_var[i] = np.average(ncfile_JJAS[varname].data[i * 4 : i * 4 + 4], axis=0)

        #JJAS_var[i] = np.average(ncfile[varname].data[i * 12 + 5 : i * 12 + 9], axis=0)


    ncfile_return  =  xr.Dataset(
        {
            "JJAS_TS": (["time", "lat", "lon"], JJAS_var),
        },
        coords={
            "time": (["time"], np.linspace(1806, 1806+len(time)-1, len(time))),
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
        },
        )
    ncfile_return['JJAS_TS'].attrs = ncfile[varname].attrs
    #
    
    return ncfile_return

def cal_JJAS_ts_diff_between_periods(ncfile, varname, periodA_1, periodA_2, periodB_1, periodB_2):
    '''
        This function is to calculate the difference between two periods
    '''
    ncfile_p1 = ncfile.sel(time=slice(periodA_1, periodA_2))
    ncfile_p2 = ncfile.sel(time=slice(periodB_1, periodB_2))

    period_diff = np.average(ncfile_p2[varname].data, axis=0) - np.average(ncfile_p1[varname].data, axis=0)

    return period_diff

# ============================ Part2: painting ==============================================
def plot_skt_changes_two_period(data, ref_file, plot_name):
    '''This function is to plot difference among two periods'''
    import cartopy.crs as ccrs
    from cartopy.util import add_cyclic_point

    proj       =  ccrs.PlateCarree()
    ax         =  plt.subplot(projection=proj)

    # Tick settings
    cyclic_data_slp, cyclic_lon = add_cyclic_point(data, coord=ref_file['lon'].data)
    #set_cartopy_tick(ax=ax,extent=paint_class.extent,xticks=np.linspace(0,140,8,dtype=int),yticks=np.linspace(-10,70,9,dtype=int),nx=1,ny=1,labelsize=10.5)

    set_cartopy_tick(ax=ax,extent=[0, 150, 0, 80],xticks=np.linspace(0,150,6,dtype=int),yticks=np.linspace(0,80,9,dtype=int),nx=1,ny=1,labelsize=10)

    im  =  ax.contourf(cyclic_lon, ref_file['lat'].data, cyclic_data_slp, np.linspace(-1,1,11), cmap='coolwarm', alpha=1, extend='both')

    ax.coastlines(resolution='110m', lw=1.25)

    ax.set_title('1901-1920 to 1941-1960',fontsize=15)
    ax.set_title('20CR',loc='right', fontsize=15)
    ax.set_title('TS',loc='left', fontsize=15)

    #add_vector_legend(ax=ax, q=q, speed=0.25)
    plt.colorbar(im, orientation='horizontal')
    
    plt.savefig('/mnt/e/paint/EUI_CR20_TS_1900_1960_diff.pdf', dpi=500)
    #plt.savefig('test.png')

# ============================= Part3. Main ==============================================
def main():
    #print(f0)
    JJAS_TS = cal_JJAS_average_each_year(ncfile=f0, varname='skt')

    JJAS_TS_DIFF = cal_JJAS_ts_diff_between_periods(ncfile=JJAS_TS, varname='JJAS_TS', periodA_1=periodA_1, periodA_2=periodA_2, periodB_1=periodB_1, periodB_2=periodB_2)

    plot_skt_changes_two_period(data=JJAS_TS_DIFF, ref_file=JJAS_TS, plot_name='a')

if __name__ == '__main__':
    main()