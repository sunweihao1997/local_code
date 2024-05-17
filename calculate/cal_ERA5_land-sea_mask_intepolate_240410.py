'''
2024-4-10
this script is to intepolate the ERA5 land-sea mask data to be consistent with the model data
'''
import xarray as xr

f0 = xr.open_dataset('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid.nc')
f1 = xr.open_dataset('/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid_linear1.5/MIROC6_SSP370_r2i1p1f1.nc')

f0 = f0.interp(latitude=f1.lat.data, longitude=f1.lon.data)
f0.to_netcdf('/home/sun/data/process/analysis/other/ERA5_land_sea_mask_model-grid1.5x1.5.nc')