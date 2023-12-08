#!/usr/bin/env python
# coding: utf-8

# **2023-11-13**<p>
# **This script serves for the EUI research**<p>
# **This script purpose is the same as <cal_Indian_rainfall_mask_other_region_GPCC_231113.ipynb>, except this rainfall is from CESM simulation**

# In[ ]:


from matplotlib import projections
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys
import cartopy
import geopandas
import rioxarray
from shapely.geometry import mapping

module_path = '/Users/sunweihao/local-code/module'
sys.path.append(module_path)
from module_sun import mask_use_shapefile


# <font color=red>1. Process the data</font>

# In[ ]:


data_path = '/Volumes/samssd/data/precipitation/CESM/'
data_name = ['BTAL_precipitation_jjas_mean_231113.nc', 'noEU_precipitation_jjas_mean_231113.nc']

shp_path = '/Volumes/samssd/data/shape/indian/'
shp_name = 'IND_adm0.shp'

# Mask the data out of the bound
f0       = xr.open_dataset(data_path + data_name[0])
f1       = xr.open_dataset(data_path + data_name[1])

prect_con = mask_use_shapefile(f0, "lat", "lon", shp_path + shp_name)
prect_neu = mask_use_shapefile(f1, "lat", "lon", shp_path + shp_name)
#prect_con = f0.sel(lat=slice(0,35), lon=slice(70, 90))
#prect_neu = f1.sel(lat=slice(0,35), lon=slice(70, 90))

#for yyyy in range(157):
#    print(np.nanmean(prect_con['PRECT_JJAS'].data[yyyy])) # (150, 96, 144)
# 4. Give the axis information to the output
ncfile  =  xr.Dataset(
{
    "JJAS_precip_con": (["time", "lat", "lon"], prect_con['PRECT_JJAS'].data),
    "JJAS_precip_neu": (["time", "lat", "lon"], prect_neu['PRECT_JJAS'].data),
},
coords={
    "time": (["time"], np.linspace(1850, 1850 + 156, 157)),
    "lat":  (["lat"],  prect_con['lat'].data),
    "lon":  (["lon"],  prect_con['lon'].data),
},
)


# <font color=red>2. Whole Indian mean and trend</font>

# In[ ]:


ncfile_select = ncfile.sel(time=slice(1891, 2006))
whole_precip_con  =  np.zeros((116))
whole_precip_neu  =  np.zeros((116))
for yyyy in range(116):
    whole_precip_con[yyyy] = np.nanmean(ncfile_select['JJAS_precip_con'].data[yyyy])
    whole_precip_neu[yyyy] = np.nanmean(ncfile_select['JJAS_precip_neu'].data[yyyy])
#print(ncfile_select)


# <font color=red>3. Paint the trend of the whole Indian precipitation</font>

# In[ ]:


def cal_moving_average(x, w):
        return np.convolve(x, np.ones(w), "valid") / w

w = 13
whole_precip_move_con = cal_moving_average(whole_precip_con, w)
whole_precip_move_neu = cal_moving_average(whole_precip_neu, w)
#print(whole_precip_move.shape) # 117 points

fig, ax = plt.subplots()
ax.plot(ncfile_select['time'].data, whole_precip_con , color='grey', linewidth=1.5)
ax.plot(ncfile_select['time'].data, whole_precip_neu, color='grey', linestyle='--', linewidth=1.5)
time_process = np.linspace(1891 + (w-1)/2, 2006 - (w-1)/2, 116 - (w-1))
ax.plot(time_process, whole_precip_move_con, color='black', linewidth=2.5)
ax.plot(time_process, whole_precip_move_neu, color='red', linewidth=2.5)


plt.savefig("/Volumes/samssd/paint/EUI_CESM_whole_Indian_rainfall_trend_JJAS_moving13.png", dpi=700)


# In[ ]:


def cal_moving_average(x, w):
        return np.convolve(x, np.ones(w), "valid") / w

w = 11
whole_precip_move_con = cal_moving_average(whole_precip_con, w)
whole_precip_move_neu = cal_moving_average(whole_precip_neu, w)
#print(whole_precip_move.shape) # 117 points

fig, ax = plt.subplots()
ax.plot(ncfile_select['time'].data, whole_precip_con, color='grey', linewidth=1.5)
ax.plot(ncfile_select['time'].data, whole_precip_neu, color='grey', linestyle='--', linewidth=1.5)
time_process = np.linspace(1891 + (w-1)/2, 2006 - (w-1)/2, 116 - (w-1))
ax.plot(time_process, whole_precip_move_con, color='black', linewidth=2.5)
ax.plot(time_process, whole_precip_move_neu, color='red', linewidth=2.5)


plt.savefig("/Volumes/samssd/paint/EUI_CESM_whole_Indian_rainfall_trend_JJAS_moving11.png", dpi=700)


# In[ ]:




