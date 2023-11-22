'''
2023-11-20
This script is to calculate the JJAS mean for the GPCP data
'''
import xarray as xr
import numpy as np

# GPCP data

GPCP_path = '/mnt/d/samssd/precipitation/GPCC/'
GPCP_name = 'precip.mon.total.1x1.v2020.nc'

gpcp      = xr.open_dataset(GPCP_path + GPCP_name)

#print(gpcp)
# Claim the average array

JJAS_prect = np.zeros((129, 180, 360))

month0 = 5 ; month_num = 4

for yyyy in range(129):
    JJAS_prect[yyyy] = np.average(gpcp['precip'].data[yyyy*12 + month0:yyyy*12 + month0 + month_num], axis=0)

# ----------- save to the ncfile ------------------
ncfile  =  xr.Dataset(
{
    "JJAS_prect": (["time", "lat", "lon"], JJAS_prect/31),
},
coords={
    "time": (["time"], np.linspace(1891, 1891 + 128, 129)),
    "lat":  (["lat"],  gpcp['lat'].data),
    "lon":  (["lon"],  gpcp['lon'].data),
},
)

ncfile['JJAS_prect'].attrs = gpcp['precip'].attrs
ncfile['JJAS_prect'].attrs['units'] = 'mm/day'

ncfile.attrs['description']  =  'Created on 2023-11-20. This file saves JJAS mean for each year calculated from GPCC'
ncfile.to_netcdf("/mnt/d/samssd/precipitation/GPCC/JJAS_GPCP_mean.nc", format='NETCDF4')