'''
2023-11-18
This script calculate Indian average rainfall simulated by the CESM2
'''
import xarray as xr
import numpy as np
import sys
import matplotlib.pyplot as plt

module_path = '/Users/sunweihao/local-code/module'
sys.path.append(module_path)
from module_sun import mask_use_shapefile

# ===================== 1. Process the data =========================
data_file  =  xr.open_dataset('/Volumes/samssd/data/precipitation/processed/CESM2/CESM2_CMIP6_precipitation_ensemble_mean_JJAS.nc')

shp_path = '/Volumes/samssd/data/shape/indian/'
shp_name = 'IND_adm0.shp'

prect    = mask_use_shapefile(data_file, "lat", "lon", shp_path + shp_name)
#print(prect)

# ===================== 2. Save to the ncfile ======================

ncfile  =  xr.Dataset(
{
    "prect": (["time", "lat", "lon"], prect['prect_JJAS'].data),
},
coords={
    "time": (["time"], data_file['time'].data),
    "lat":  (["lat"],  data_file['lat'].data),
    "lon":  (["lon"],  data_file['lon'].data),
},
)

# ===================== 3. Calculate whole Indian mean ===========

ncfile1 = ncfile.sel(time=slice(1891, 2006))
whole_precip  =  np.zeros((116))

for yyyy in range(116):
    whole_precip[yyyy] = np.nanmean(ncfile1['prect'].data[yyyy])

def cal_moving_average(x, w):
        return np.convolve(x, np.ones(w), "valid") / w

w = 13
whole_precip_move_con = cal_moving_average(whole_precip, w)

# ===================== 4. Paint ===============================
fig, ax = plt.subplots()
ax.plot(ncfile1['time'].data, whole_precip, color='grey', linewidth=1.5)

time_process = np.linspace(1891 + (w-1)/2, 2006 - (w-1)/2, 116 - (w-1))

ax.plot(time_process, whole_precip_move_con, color='black', linewidth=2.5)



plt.savefig("/Volumes/samssd/paint/EUI_CESM2_whole_Indian_rainfall_trend_JJAS_moving13.png", dpi=700)

# ==================== 5. Plot the whole period ===================

whole_precip  =  np.zeros((165))

for yyyy in range(165):
    whole_precip[yyyy] = np.nanmean(ncfile['prect'].data[yyyy])

def cal_moving_average(x, w):
        return np.convolve(x, np.ones(w), "valid") / w

w = 13
whole_precip_move_con = cal_moving_average(whole_precip, w)

# ===================== 4. Paint ===============================
fig, ax = plt.subplots()
ax.plot(ncfile['time'].data, whole_precip, color='grey', linewidth=1.5)

time_process = np.linspace(1850 + (w-1)/2, 2014 - (w-1)/2, 165 - (w-1))

ax.plot(time_process, whole_precip_move_con, color='black', linewidth=2.5)



plt.savefig("/Volumes/samssd/paint/EUI_CESM2_whole_Indian_rainfall_trend_JJAS_moving13_whole_period.png", dpi=700)