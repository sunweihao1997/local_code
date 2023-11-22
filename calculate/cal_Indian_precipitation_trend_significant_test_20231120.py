'''
This script is to calculate the spatial distribution in the trend of precipitation over Indian continent in the 1900 ~ 1960
'''
import xarray as xr
import numpy as np
import geopandas
import rioxarray
from shapely.geometry import mapping
import pymannkendall as mk

# ================== File location information ========================
# gpcc data

gpcc_path = '/mnt/d/samssd/precipitation/GPCC/'
gpcc_name = 'JJAS_GPCC_mean.nc'

gpcc      = xr.open_dataset(gpcc_path + gpcc_name)

#print(gpcc)

# CESM data

CESM_path = '/mnt/d/samssd/precipitation/CESM/'
CESM_name = 'BTAL_precipitation_jjas_mean_231113.nc'

cesm      = xr.open_dataset(CESM_path + CESM_name)
#print(cesm)

# CESM2 data

CESM2_path = '/mnt/d/samssd/precipitation/processed/CESM2/'
CESM2_name = 'CESM2_CMIP6_precipitation_ensemble_mean_JJAS.nc'

cesm2      = xr.open_dataset(CESM2_path + CESM2_name)

# shape file
shape_path= '/mnt/d/samssd/shape/indian/'
shape_name= 'IND_adm0.shp'

# =====================================================================

# =================== Calculation =====================================
# -------------- 1. Unite the time axis --------------------------

start_year = 1900
end_year   = 1960

gpcc       = gpcc.sel(time = slice(start_year, end_year))
cesm       = cesm.sel(time = slice(start_year, end_year))
cesm2      = cesm2.sel(time = slice(start_year, end_year))

# -------------- 2. Claim the array to save significance ---------
#print(cesm) 
#print(gpcc['JJAS_prect'].data[5, :, 50])
p_gpcc     = np.zeros((gpcc['JJAS_prect'].data.shape[1], gpcc['JJAS_prect'].data.shape[2]))
p_cesm     = np.zeros((cesm['PRECT_JJAS'].data.shape[1], cesm['PRECT_JJAS'].data.shape[2]))
p_cesm2    = np.zeros((cesm2['prect_JJAS'].data.shape[1], cesm2['prect_JJAS'].data.shape[2]))

# -------------- 3. Claim the array to save the trend ------------

trend_gpcc = np.zeros((gpcc['JJAS_prect'].data.shape[1], gpcc['JJAS_prect'].data.shape[2]))
trend_cesm = np.zeros((cesm['PRECT_JJAS'].data.shape[1], cesm['PRECT_JJAS'].data.shape[2]))
trend_cesm2= np.zeros((cesm2['prect_JJAS'].data.shape[1], cesm2['prect_JJAS'].data.shape[2]))

# -------------- 4. Calculation trend and MK trend test ----------
# 4-1 CESM

for latt in range(cesm['PRECT_JJAS'].data.shape[1]):
    for lonn in range(cesm['PRECT_JJAS'].data.shape[2]):
        # least squares
        a = np.polyfit(cesm['time'].data, cesm['PRECT_JJAS'].data[:, latt, lonn], 1)

        trend_cesm[latt, lonn] = a[0] * 10 # units: mm per day per decade

        # MK test
        b = mk.original_test(cesm['PRECT_JJAS'].data[:, latt, lonn], alpha=0.1)

        if b[0] == 'no trend':
            continue
        else:
            p_cesm[latt, lonn] = 1

# 4-2 GPCC

for latt in range(gpcc['JJAS_prect'].data.shape[1]):
    for lonn in range(gpcc['JJAS_prect'].data.shape[2]):
        # least squares
        a = np.polyfit(gpcc['time'].data, gpcc['JJAS_prect'].data[:, latt, lonn], 1)

        trend_gpcc[latt, lonn] = a[0] * 10 # units: mm per day per decade

        # MK test
        if np.isnan(trend_gpcc[latt, lonn]):
            continue
        else:
            b = mk.original_test(gpcc['JJAS_prect'].data[:, latt, lonn], alpha=0.1)

            if b[0] == 'no trend':
                continue
            else:
                p_gpcc[latt, lonn] = 1

#print(trend_cesm)
# 4-3 CESM2

for latt in range(cesm2['prect_JJAS'].data.shape[1]):
    for lonn in range(cesm2['prect_JJAS'].data.shape[2]):
        # least squares
        a = np.polyfit(cesm2['time'].data, cesm2['prect_JJAS'].data[:, latt, lonn], 1)

        trend_cesm2[latt, lonn] = a[0] * 10 # units: mm per day per decade

        # MK test
        b = mk.original_test(cesm2['prect_JJAS'].data[:, latt, lonn], alpha=0.1)

        if b[0] == 'no trend':
            continue
        else:
            p_cesm2[latt, lonn] = 1

# -------------- 5. Save to the netcdf file -----------------------

ncfile  =  xr.Dataset(
{
    "trend_cesm": (["lat1", "lon1"], trend_cesm),
    "trend_gpcc": (["lat2", "lon2"], trend_gpcc),
    "trend_cesm2":(["lat3", "lon3"], trend_cesm2),
    "p_cesm":     (["lat1", "lon1"], p_cesm),
    "p_gpcc":     (["lat2", "lon2"], p_gpcc),
    "p_cesm2":    (["lat3", "lon3"], p_cesm2),
},
coords={
    "lat1":  (["lat1"],  cesm['lat'].data),
    "lon1":  (["lon1"],  cesm['lon'].data),
    "lat3":  (["lat3"],  cesm2['lat'].data),
    "lon3":  (["lon3"],  cesm2['lon'].data),
    "lat2":  (["lat2"],  gpcc['lat'].data),
    "lon2":  (["lon2"],  gpcc['lon'].data),
},
)

ncfile['trend_cesm'].attrs['units'] = 'mm day**-1 decade**-1'
ncfile['trend_gpcc'].attrs['units'] = 'mm day**-1 decade**-1'
ncfile['trend_cesm2'].attrs['units'] = 'mm day**-1 decade**-1'

ncfile.to_netcdf('/mnt/d/samssd/precipitation/processed/CESM_GPCC_JJAS_trend_1900_1960_significant_level.nc')