'''
2024-2-5
This script is to calculate the total precipitation which is combination of the precc and precl
'''

import numpy as np
import xarray as xr
import os

path_sst   = '/home/sun/data/download_data/CESM2_pacemaker/sst/mon/'

list_sst   = os.listdir(path_sst) ; list_sst.sort()


# ==== 1. Save the files to an array ====  Completed and save to ncfile

sst_all  = np.zeros((10, 1620, 192, 288))

if len(list_sst) != 10:
    print(f"Something wrong with the files")

for i in range(len(list_sst)):
    f1_sst = xr.open_dataset(path_sst + list_sst[i])

    sst_all[i] = f1_sst['SST'].data

# ---- 1.1 Save the all members array to the ncfile ----

ncfile  =  xr.Dataset(
    {
        "SST":   (["member", "time", "lat", "lon"], sst_all),
    },
    coords={
        "member": (["member"], np.linspace(1, 10, 10)),
        "lat":    (["lat"],    f1_sst['lat'].data),
        "lon":    (["lon"],    f1_sst['lon'].data),
        "time":   (["time"],   f1_sst['time'].data),
    },
        )

# ---- 1.1.1 Add attributes ----

ncfile['SST'].attrs = f1_sst['SST'].attrs

ncfile.attrs['description'] = 'Create on 2024-2-5 on the Huaibei Server. This netcdf file saves the 10-members SST data from the CESM2 pacemaker experiments.'

ncfile.to_netcdf('/home/sun/data/process/model/CESM2_pacemaker_SST_10members_1880-2014.nc')