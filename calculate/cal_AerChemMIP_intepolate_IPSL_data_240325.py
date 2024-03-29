'''
2024-3-24
This script is dealing with the IPSL data, because I add them later
'''
import xarray as xr
import numpy as np

source_path = '/data/AerChemMIP/LLNL_download/'

f1          = xr.open_dataset(source_path + 'IPSL-CM5A2_historical_r1i1p1f1.nc')
f2          = xr.open_dataset(source_path + 'IPSL-CM5A2_SSP370_r1i1p1f1.nc')
f3          = xr.open_dataset(source_path + 'IPSL-CM5A2_SSP370NTCF_r1i1p1f1.nc')


new_lat = np.linspace(-90, 90, 121)
new_lon = np.linspace(0, 360, 241)

f1_interp   = f1.interp(lat = new_lat, lon=new_lon,)
f2_interp   = f2.interp(lat = new_lat, lon=new_lon,)
f3_interp   = f3.interp(lat = new_lat, lon=new_lon,)

f1_interp.to_netcdf('/data/AerChemMIP/LLNL_download/postprocess_samegrids/IPSL-CM5A2_historical_r1i1p1f1.nc')
f2_interp.to_netcdf('/data/AerChemMIP/LLNL_download/postprocess_samegrids/IPSL-CM5A2_SSP370_r1i1p1f1.nc')
f3_interp.to_netcdf('/data/AerChemMIP/LLNL_download/postprocess_samegrids/IPSL-CM5A2_SSP370NTCF_r1i1p1f1.nc')