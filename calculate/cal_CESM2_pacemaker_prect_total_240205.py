'''
2024-2-5
This script is to calculate the total precipitation which is combination of the precc and precl
'''

import numpy as np
import xarray as xr
import os

path_ss = '/home/sun/data/download_data/CESM2_pacemaker/precc/mon/'

list_precc = os.listdir(path_precc) ; list_precc.sort()
list_precl = os.listdir(path_precl) ; list_precl.sort()

vars_name  = ['PRECC', 'PRECL']

## ==== 1. Save the files to an array ====  Completed and save to ncfile
#
#precc_all  = np.zeros((10, 1620, 192, 288))
#precl_all  = np.zeros((10, 1620, 192, 288))
#
#if len(list_precc) != 10 or len(list_precl) != 10:
#    print(f"Something wrong with the files")
#
#for i in range(len(list_precc)):
#    f1_precc = xr.open_dataset(path_precc + list_precc[i])
#    f1_precl = xr.open_dataset(path_precl + list_precl[i])
#
#    precc_all[i] = f1_precc['PRECC'].data
#    precl_all[i] = f1_precl['PRECL'].data
#
## ---- 1.1 Save the all members array to the ncfile ----
#
#ncfile  =  xr.Dataset(
#    {
#        "PRECC": (["member", "time", "lat", "lon"], precc_all),
#        "PRECL": (["member", "time", "lat", "lon"], precl_all),
#    },
#    coords={
#        "member": (["member"], np.linspace(1, 10, 10)),
#        "lat":    (["lat"],    f1_precc['lat'].data),
#        "lon":    (["lon"],    f1_precc['lon'].data),
#        "time":   (["time"],   f1_precc['time'].data),
#    },
#        )
#
## ---- 1.1.1 Add attributes ----
#
#ncfile['PRECC'].attrs = f1_precc['PRECC'].attrs
#ncfile['PRECL'].attrs = f1_precl['PRECL'].attrs
#
#ncfile.attrs['description'] = 'Create on 2024-2-5 on the Huaibei Server. This netcdf file saves the 10-members PRECC and PRECL data from the CESM2 pacemaker experiments.'
#
#ncfile.to_netcdf('/home/sun/data/process/model/CESM2_pacemaker_PRECC_PRECL_10members_1880-2014.nc')