'''
2023-12-18
This script is to deal with the data from GPCC, to show the influence of the aerosol on the long-term change in precipitation over Indian continent
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# ========================= File Location =================================

path_src = '/home/sun/download-data/GPCC_Precipitation/'

file_src = 'precip.mon.total.v2020.nc'

f0       = xr.open_dataset(path_src + file_src)
#print(f0)
#print(np.isnan(f0['precip']).any())
#print(f0)
time     = f0.time.data
lat      = f0.lat.data # 90 to -90
lon      = f0.lon.data

years    = 129
year     = np.linspace(1891, 1891 + years - 1, years)

# =========================================================================

# ======================== Calculation fot JJAS mean ======================

def cal_JJAS_mean(f0, mon_list, varname):
    f0_JJAS = f0.sel(time=f0.time.dt.month.isin(mon_list))

    #print(f0_JJAS)
    shape0 = f0_JJAS[varname].data.shape

    # Year number
    years = int(shape0[0]/len(mon_list))

    # 1. Claim the JJAS-mean array
    JJAS_PRECT = np.zeros((years, len(lat), len(lon)))

    # 2. Calculation
    #print(years)
    for i in range(years):
        JJAS_PRECT[i] = np.average(f0_JJAS[varname].data[i * len(mon_list): i * len(mon_list) + len(mon_list)], axis=0)

    # 3. aggregate into ncfile
    ncfile  =  xr.Dataset(
        {
            "JJAS_PRECT": (["time", "lat", "lon"], JJAS_PRECT / 31),
        },
        coords={
            "time": (["time"], np.linspace(1891, 1891+(years - 1), years)),
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
        },
        )
    ncfile['JJAS_PRECT'].attrs = f0[varname].attrs
    ncfile['JJAS_PRECT'].attrs['units'] = 'mm/day'

    return ncfile

# =========================================================================

# ======================== Function for smoothing =========================

def cal_moving_average(x, w):
        return np.convolve(x, np.ones(w), "valid") / w

# =========================================================================


# ======================== Paint for area-averaged mean evolution ================

def plot_area_average_evolution(f0, varname, extent):
    '''
        extent: latmin, latmax, lonmin, linmax
    '''
    # 1. Extract data from original file using extent

    f0_area = f0.sel(lat=slice(extent[0], extent[1]), lon=slice(extent[2], extent[3]))
    #print(f0_area)

    # 2. Claim the array for saving the 165-year data

    area_mean = np.zeros((years))

    # 3. Calculate for each year

    for yy in range(years):
        area_mean[yy] = np.nanmean(f0_area[varname].data[yy])

    # 4. Smoothing
    w = 13
    area_mean_smooth  =  cal_moving_average(area_mean - np.average(area_mean), w) # Notice that the lenth after smoothing is (original - (window - 1))

    # 5. Paint
    fig, ax = plt.subplots()

    ax.plot(year, area_mean - np.average(area_mean), color='grey', linewidth=1.5)

    time_process = np.linspace(1891 + (w-1)/2, 1891 + 129 - 1 - (w-1)/2, years - (w-1))

    ax.plot(time_process, area_mean_smooth, color='orange', linewidth=2.5)

    ax.set_ylim((-0.8 * 2, 0.8 * 2))
    
    ax.set_ylabel("Observation-Based Data", fontsize=11)

    ax.set_title("(a)", loc='left', fontsize=15)
    ax.set_title("74-86°E, 18-28°N", loc='right', fontsize=15)

    # Plot zero line
    ax.plot([1891, 2020], [0, 0], 'k--')

    # Set the limit for the x-axis
    ax.set_xlim((1895, 2005))

    plt.savefig("/home/sun/paint/aerosol_research/Aerosol_research_GPCC_PRECT_evolution_area_average_Indian_key_region.pdf", dpi=700)





def main():
    JJAS_mean = cal_JJAS_mean(f0, [6, 7, 8, 9], 'precip')
    plot_area_average_evolution(JJAS_mean, 'JJAS_PRECT', [28, 18, 74, 86])
    #print(JJAS_mean)


if __name__ == '__main__':
    main()