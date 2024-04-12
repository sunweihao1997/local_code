'''
2024-4-10
this script is to intepolate the ERA5 land-sea mask data to be consistent with the model data
'''
import xarray as xr

f0 = xr.open_dataset('/data/AerChemMIP/process/ERA5_land_sea_mask_1x1.nc')
f1 = xr.open_dataset('/data/AerChemMIP/process/CMIP6_model_historical_SSP370_SSP370NTCF_monthly_PETADV_2015-2050.nc')

f0 = f0.interp(latitude=f1.lat.data, longitude=f1.lon.data)
f0.to_netcdf('/data/AerChemMIP/process/ERA5_land_sea_mask_model-grid.nc')