'''
2024-3-22
This script is to calculate the climatological annual evolution of the precipitation in the NCEP data
'''
import numpy as np
import os
import xarray as xr
import cftime

data_path = '/home/sun/data/download_data/NCEP2/precipitation/'

data_list = os.listdir(data_path) ; data_list.sort()

ref_file  = xr.open_dataset(data_path + data_list[1])
lat       = ref_file.lat.data ; lon      = ref_file.lon.data

# Claim the climate array
pre_avg   = np.zeros((365, len(lat), len(lon)))

years_num = len(ref_file)

for i in range(years_num):
    f1    = xr.open_dataset(data_path + data_list[i])

    pre_avg += (f1.prate.data[:365] * 86400 / years_num) # convert to mm/day

# The time-axis
time0 = cftime.num2date(range(0, 365), units='days since 2000-01-01', calendar='365_day')

ncfile  =  xr.Dataset(
    {
        "precip":     (["time", "lat", "lon"], pre_avg[:, ::-1, :]),
       
    },
    coords={
        "lat":   (["lat"],  lat[::-1]),
        "lon":   (["lon"],  lon),
        "time":  (["time"], time0),
    },
    )


ncfile.attrs['description'] = 'Created on 2024-3-22. This file save the climatological annual evolution of the precipitation using NCEP data, the period is 1980-2014'
ncfile.attrs['Mother'] = 'local-code (server Huaibei): cal_NCEP_precipitation_climatological_annual_evolution_240322.py'

ncfile['precip'].attrs = ref_file['prate'].attrs
ncfile['precip'].attrs['units'] = 'mm/day'

out_path = '/home/sun/data/process/analysis/AerChem/observation/'

new_lat = np.linspace(-90, 90, 91)
new_lon = np.linspace(0, 360, 181)

f0_interp = ncfile.interp(lat = new_lat, lon=new_lon,)

#print(f0_interp['precip'].data[5, :, 5])
f0_interp.to_netcdf(out_path + 'NCEP2_precipitation_climate_annual_evolution_1980_2014.nc')