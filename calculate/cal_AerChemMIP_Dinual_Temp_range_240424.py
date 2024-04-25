'''
2024-4-24
This script is to calculate the Dinual Temperature Range

The method of calculation can be found in https://journals.ametsoc.org/view/journals/clim/35/22/JCLI-D-21-0928.1.xml : The DTR is defined as the difference between daily maximum and daily minimum temperatures 
'''
import xarray as xr
import numpy as np
import os

# ================ Path Information ===================

path_min = '/home/sun/data/process/model/aerchemmip-postprocess/tasmin/'
path_max = '/home/sun/data/process/model/aerchemmip-postprocess/tasmax/' # Note the file name under these two paths are same
end_path = '/home/sun/data/process/model/aerchemmip-postprocess/dtr/'

file_min = os.listdir(path_min)
file_max = os.listdir(path_max)

# =====================================================

# =============== Calculation Part ====================
for ff in file_min:
    fmin = xr.open_dataset(path_min + ff)
    fmax = xr.open_dataset(path_max + ff)

    dtr  = fmax['tasmax'].data - fmin['tasmin'].data

    # Write to ncfile
    ncfile  =  xr.Dataset(
            {
                "dtr":     (["time", "lat", "lon"], dtr),          
            },
            coords={
                "time": (["time"], fmin.time.data),
                "lat":  (["lat"],  fmin.lat.data),
                "lon":  (["lon"],  fmin.lon.data),
            },
            )
    ncfile.attrs['description'] = 'Created on 24-Apr-2024 by cal_AerChemMIP_Dinual_Temp_range_240424.py.'

    ncfile.to_netcdf(end_path + ff)

    print(f'Successfully calculated the file {ff}')

    del ncfile