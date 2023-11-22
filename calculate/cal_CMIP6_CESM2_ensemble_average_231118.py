'''
2023-11-18
This script calculate the ensemble of the CESM2 ensemble precipitation
'''
import numpy as np
import xarray as xr
import os

path_src  =  '/Volumes/samssd/data/precipitation/CESM2/'
lists     =  os.listdir(path_src) ; lists.sort()

#print(lists[0])
ref_file  =  xr.open_dataset(path_src + lists[0])

#print(ref_file) # varname = pr (1980, 192, 288)
# ================= 1. Claim the base array ======================
avg_pr    =  np.zeros((1980, 192, 288))

# ================= 2. Calculation ===============================

#file_number = 8
#for i in range(file_number):
#    f0  =  xr.open_dataset(path_src + lists[i])
#
#    avg_pr += f0['pr'].data / file_number

# ================= 3. Write to ncfile ===========================
# 3.1 unit of model output is kg m-2 s-1, here convert it to mm/dat
# method : 1 kg m-2 s-1 = 86400 mm day-1.

#ncfile  =  xr.Dataset(
#{
#    "prect": (["time", "lat", "lon"], avg_pr * 86400),
#},
#coords={
#    "time": (["time"], ref_file['time'].data),
#    "lat":  (["lat"],  ref_file['lat'].data),
#    "lon":  (["lon"],  ref_file['lon'].data),
#},
#)
#ncfile['prect'].attrs = ref_file['pr'].attrs
#ncfile['prect'].attrs['units'] = 'mm/day'
#
#out_path = '/Volumes/samssd/data/precipitation/processed/CESM2/'
#ncfile.to_netcdf(out_path + 'CESM2_CMIP6_precipitation_ensemble_mean.nc')

# ================= 4. Use the result to calculate JJAS mean =================
avg_file  =  xr.open_dataset('/Volumes/samssd/data/precipitation/processed/CESM2/CESM2_CMIP6_precipitation_ensemble_mean.nc')

# ================= 5. Claim the base array ==================================
JJAS_prect  =  np.zeros((165, 192, 288))

month0    =  5
month1    =  9

# ================= 6. Calculation ===========================================

for yyyy in range(165):
    JJAS_prect[yyyy] = np.average(avg_file['prect'].data[yyyy*12 + month0:yyyy*12 + month1], axis=0)

# ================= 7. Write to ncfile =======================================

ncfile  =  xr.Dataset(
{
    "prect_JJAS": (["time", "lat", "lon"], JJAS_prect),
},
coords={
    "time": (["time"], np.linspace(1850, 1850+164, 165)),
    "lat":  (["lat"],  ref_file['lat'].data),
    "lon":  (["lon"],  ref_file['lon'].data),
},
)
ncfile['prect_JJAS'].attrs = ref_file['pr'].attrs
ncfile['prect_JJAS'].attrs['units'] = 'mm/day'
#
out_path = '/Volumes/samssd/data/precipitation/processed/CESM2/'
ncfile.to_netcdf(out_path + 'CESM2_CMIP6_precipitation_ensemble_mean_JJAS.nc')