'''
2024-5-22
This script is to calculate the divergent wind and divergence for non-interpolated ua/va for files
'''
import xarray as xr
import numpy as np
from scipy import stats
from windspharm.xarray import VectorWind
import os

ua_list = os.listdir("/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/")
va_list = os.listdir("/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/")

for ff in ua_list:
    print(f"Now it is dealing with {ff}")
    fua = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/" + ff)
    fva = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/" + ff.replace("ua_", "va_"))

    w      =  VectorWind(fua.sel(plev=20000)['ua'],  fva.sel(plev=20000)['va'])

    u, v   =  w.irrotationalcomponent()
    div    =  w.divergence()

    # Write to ncfile
    ncfile  =  xr.Dataset(
            {
                "div":        (["time", "lat", "lon"], div.data),  
                "u":          (["time", "lat", "lon"], u.data),  
                "v":          (["time", "lat", "lon"], v.data),  
            },
            coords={
                "lat":  (["lat"],  fua.lat.data),
                "lon":  (["lon"],  fua.lon.data),
                "time": (["time"], fua.time.data),
            },
        )

    ncfile.to_netcdf("/home/sun/data/AerChemMIP/process/200_div/" + ff.replace("ua_", "div_"))

    del ncfile