'''
2023-12-11
This script is to calculate and paint the changes in wind at 850 level between 1900-1920 and 1940-1960, using CR20 data
'''
import xarray as xr
import numpy as np
import sys
import matplotlib.pyplot as plt

#module_path = '/Users/sunweihao/local_code/module'
module_path = '/home/sun/local_code/module'
sys.path.append(module_path)

from module_sun import set_cartopy_tick

periodA_1 = 1900 ; periodA_2 = 1910
periodB_1 = 1940 ; periodB_2 = 1950

#file_path = '/Volumes/samssd/'
file_path = '/mnt/e/download_data/CR20/CR20_UV/'
file_name1 = 'uwnd.mon.mean.nc'
file_name2 = 'vwnd.mon.mean.nc'

fu = xr.open_dataset(file_path + file_name1).sel(level=850)
fv = xr.open_dataset(file_path + file_name2).sel(level=850)
#print(f0)

# ======================================== Part of calculation =========================================
def cal_JJAS_average_each_year(ncfile, varname):
    '''
        This function calculate JJAS-average and save to ncfile format
    '''
    # 1. Slice out JJAS data
    #ncfile_JJAS = ncfile.sel(time=ncfile.time.dt.month.isin([6, 7, 8, 9])) # The name of the time dimension in ERA20C is initial_time0_hours
    ncfile_JJAS = ncfile.sel(time=ncfile.time.dt.month.isin([6, 7, 8, 9]))
    ncfile_JJAS = ncfile.sel(time=ncfile.time.dt.month.isin([6, 7, 8,]))
    
    lat = ncfile.lat.data ; lon = ncfile.lon.data ; time = ncfile.time.data

    #2. Claim the array for average

    JJAS_var = np.zeros((len(time), len(lat), len(lon))) # Totally 111 years from 1900 to 2010

    # 3. Calculating
    for i in range(len(time)):
        JJAS_var[i] = np.average(ncfile_JJAS[varname].data[i * 3 : i * 3 + 3], axis=0)

        #JJAS_var[i] = np.average(ncfile[varname].data[i * 12 + 5 : i * 12 + 9], axis=0)


    ncfile_return  =  xr.Dataset(
        {
            "JJAS_PSL": (["time", "lat", "lon"], JJAS_var),
        },
        coords={
            "time": (["time"], np.linspace(1806, 1806+len(time)-1, len(time))),
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
def plot_uv_changes_two_period(data_u, data_v, ref_file,):
    '''This function is to plot difference among two periods'''
    import cartopy.crs as ccrs
    from cartopy.util import add_cyclic_point

    proj       =  ccrs.PlateCarree()
    ax         =  plt.subplot(projection=proj)

    # Tick settings
    cyclic_data_u, cyclic_lon = add_cyclic_point(data_u, coord=ref_file['lon'].data)
    cyclic_data_v, cyclic_lon = add_cyclic_point(data_v, coord=ref_file['lon'].data)
    #set_cartopy_tick(ax=ax,extent=paint_class.extent,xticks=np.linspace(0,140,8,dtype=int),yticks=np.linspace(-10,70,9,dtype=int),nx=1,ny=1,labelsize=10.5)

    set_cartopy_tick(ax=ax,extent=[0, 150, 0, 80],xticks=np.linspace(0,150,6,dtype=int),yticks=np.linspace(0,80,9,dtype=int),nx=1,ny=1,labelsize=10)

    # Vector Map
    q  =  ax.quiver(ref_file['lon'].data, ref_file['lat'].data, data_u, data_v, 
        regrid_shape=20, angles='uv',        # regrid_shape这个参数越小，是两门就越稀疏
        scale_units='xy', scale=0.5,        # scale是参考矢量，所以取得越大画出来的箭头就越短
        units='xy', width=0.5,              # width控制粗细
        transform=proj,
        color='k', headlength = 5, headaxislength = 4, headwidth = 4, alpha=0.8)

    ax.coastlines(resolution='110m', lw=1.25)

    ax.set_title('1901-1920 to 1941-1960',fontsize=15)
    ax.set_title('20CR',loc='right', fontsize=15)
    ax.set_title('850 UV',loc='left', fontsize=15)

    #add_vector_legend(ax=ax, q=q, speed=0.25)
    
    plt.savefig('/mnt/e/paint/EUI_CR20_UV_850_1900_1960_diff_JJA.pdf', dpi=500)
    #plt.savefig('test1.png')

# ============================= Part3. Main ==============================================
def main():
    #print(f0)
    JJAS_U = cal_JJAS_average_each_year(ncfile=fu, varname='uwnd')
    JJAS_V = cal_JJAS_average_each_year(ncfile=fv, varname='vwnd')

    # Please notice: here the varname is still using JJAS_PSL because I am not willing to modify the function
    JJAS_U_DIFF = cal_JJAS_PSL_diff_between_periods(ncfile=JJAS_U, varname='JJAS_PSL', periodA_1=periodA_1, periodA_2=periodA_2, periodB_1=periodB_1, periodB_2=periodB_2)
    JJAS_V_DIFF = cal_JJAS_PSL_diff_between_periods(ncfile=JJAS_V, varname='JJAS_PSL', periodA_1=periodA_1, periodA_2=periodA_2, periodB_1=periodB_1, periodB_2=periodB_2)

    plot_uv_changes_two_period(data_u=JJAS_U_DIFF, data_v=JJAS_V_DIFF, ref_file=JJAS_U)

if __name__ == '__main__':
    main()