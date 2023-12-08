'''
2023-11-22
This script is to plot ensemble trend among the simulation of the CESM output
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys

sys.path.append("/Users/sunweihao/local-code/module/")
from module_sun import *

# ==================== Data location =======================

data_path   = '/Volumes/samssd/data/precipitation/CESM/ensemble_original/'
# Here need to add sum of PRECC and PRECL
data_name_c = 'BTAL_PRECC_1850_150years_member_'
data_name_l = 'BTAL_PRECL_1850_150years_member_'

shp_path = '/Volumes/samssd/data/shape/indian/'
shp_name = 'IND_adm0.shp'

# ===================== other settings =======================

# Set the start and end for the period
start_year = 1900
end_year   = 2000

# ==========================================================

# ============================ Function of calculation ======================================

# Function to mask Indian area
def calculate_anomaly(ncfile):
    '''
        This function calculate regional average rainfall time-series and calculate anomoly for each year
    '''

    # =============== 1. Mask the other region ===================

    clipped = mask_use_shapefile(ncfile, "lat", "lon", shp_path + shp_name)

    # =============== 2. calculate the area_average for each year =====================

    Indian_rainfall_ensemble = np.zeros((8, 157))
    for num in range(8):
        for yyyy in range(157):
            Indian_rainfall_ensemble[num, yyyy] = np.nanmean(clipped["JJAS_prect_{}".format(num+1)].data[yyyy])

    da = xr.DataArray(
            data=Indian_rainfall_ensemble,
            dims=["member", "time"],
            coords=dict(
                member=np.linspace(1, 8, 8),
                time=np.linspace(1850, 2006, 157),
            ),
        )
    
    return da

    


# Function to calculate JJAS mean for each year and save into ncfile
def calculate_seasonal_single_var_mean_for_each_year(ncfile_c, ncfile_l, ncfile_varname_c, ncfile_varname_l, ncfile_latname, ncfile_lonname, ensemble_num):
    '''
        This function calculate JJAS mean for the CESM ensemble data
    '''

    start_year = 1850
    end_year   = 2006

    # ================= 1. Claim the base array ====================

    JJAS_mean    = np.zeros(((end_year - start_year + 1), ncfile_l[ncfile_varname_l].data.shape[1], ncfile_l[ncfile_varname_l].data.shape[2]))

    # ================= 2. Calculation =============================

    for yyyy in range((end_year - start_year + 1)):
        JJAS_mean[yyyy] = np.average(ncfile_c[ncfile_varname_c].data[yyyy * 4 : yyyy * 4 + 4], axis=0) + np.average(ncfile_l[ncfile_varname_l].data[yyyy * 4 : yyyy * 4 + 4], axis=0)

    # ================= 3. Save to ncfile ==========================

    ncfile  =  xr.Dataset(
        {
            "JJAS_prect_{}".format(ensemble_num): (["time", "lat", "lon"], JJAS_mean * 86400 * 1000),
        },
        coords={
            "time": (["time"], np.linspace(start_year, end_year, (end_year - start_year + 1))),
            "lat":  (["lat"],  ncfile_c[ncfile_latname].data),
            "lon":  (["lon"],  ncfile_c[ncfile_lonname].data),
        },
        )

    ncfile["JJAS_prect_{}".format(ensemble_num)].attrs = ncfile_c[ncfile_varname_c].attrs

    return ncfile


# ====================== Main functions =========================
def calculation():

    # ===================== 1. Calculate JJAS precipitation for CESM ======================

#    ncfile_list = []
#    ncfile_sets  = xr.Dataset()
#    for e_num in range(8):
#        f0_c = xr.open_dataset(data_path + data_name_c + str(e_num + 1) + ".nc")
#        f0_l = xr.open_dataset(data_path + data_name_l + str(e_num + 1) + ".nc")
#
#        f0_c = f0_c.sel(time=f0_c.time.dt.month.isin([6, 7, 8, 9]))
#        f0_l = f0_l.sel(time=f0_l.time.dt.month.isin([6, 7, 8, 9]))
#
#        ncfile_list.append(calculate_seasonal_single_var_mean_for_each_year(ncfile_c=f0_c, ncfile_l=f0_l, ncfile_varname_c='PRECC', ncfile_varname_l='PRECL', ncfile_latname='lat', ncfile_lonname='lon', ensemble_num=(e_num + 1)))
#
#        print("{} member success".format(e_num + 1))
#        ncfile_sets["JJAS_prect_{}".format(e_num + 1)] = ncfile_list[e_num]["JJAS_prect_{}".format(e_num + 1)]
    
    #print(ncfile_list[3])
    #print(ncfile_sets)
    out_path = '/Volumes/samssd/data/precipitation/CESM/ensemble_JJAS/'
#    ncfile_sets.to_netcdf(out_path + 'CESM_BTAL_esemble_JJAS_precipitation.nc')

    # =======================================================================================

    # ====================== 2. Calculate Indian rainfall ===================================
    ncfile0 = xr.open_dataset(out_path + 'CESM_BTAL_esemble_JJAS_precipitation.nc')

    series = calculate_anomaly(ncfile=ncfile0)
    series = series.sel(time=slice(1900, 2000))
    # ===================== 4. Paint ===============================
    fig, ax = plt.subplots()

    for i in range(8):
        ax.plot(np.linspace(1900, 2000, 101), np.average(series, axis=0) - np.average(series), color='grey', linewidth=1.5)

    plt.savefig("series.png")

    

if __name__ == "__main__":
    calculation()