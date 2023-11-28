'''
2023-11-20
This script is to calculate the JJAS mean for the GPCP data

2023-11-23 update
Use the dt month to select range of time
'''
import xarray as xr
import numpy as np

# GPCP data

GPCP_path = '/mnt/e/data/precipitation/GPCC/'
GPCP_name = 'precip.mon.total.1x1.v2020.nc'

gpcp      = xr.open_dataset(GPCP_path + GPCP_name)
print(gpcp)
gpcp      = gpcp.sel(time=(gpcp.time.dt.month.isin([6, 7, 8, 9])))
print(gpcp)
#print(gpcp)
# Claim the average array

JJAS_prect = np.zeros((129, 180, 360))

for yyyy in range(129):
    JJAS_prect[yyyy] = np.average(gpcp['precip'].data[yyyy*4 :yyyy*4 + 4], axis=0)

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

ncfile.attrs['description']  =  'Created on 2023-11-20. This file saves JJAS mean for each year calculated from GPCC. The difference is that it use new time slice method.'
ncfile.to_netcdf("/mnt/e/data/precipitation/GPCC/JJAS_GPCP_mean_update.nc", format='NETCDF4')