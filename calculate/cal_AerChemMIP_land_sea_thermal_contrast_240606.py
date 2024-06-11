'''
2024-6-6
This script is to calculate the land-sea thermal contrast based on SSP370 and SSP370lowNTCF experiments
'''
import xarray as xr
import numpy as np

# =============== Read file =============

f0 = xr.open_dataset("/data/AerChemMIP/process/multiple_model_climate_ts_month_MJJAS_36years.nc").sel(lat=slice(-80, 80))

mask_file = xr.open_dataset("/data/AerChemMIP/process/ERA5_land_sea_mask_model-grid.nc")
# Need to interpolate
mask_file = mask_file.interp(latitude=f0.lat.data, longitude=f0.lon.data)

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'MPI-ESM-1-2-HAM', 'MIROC6']


# =======================================

def cal_land_sea_thermal_contrast(ncfile, model_tag):
    # 1. Read the data
    single_ssp  = ncfile[model_tag + '_ssp']
    single_ntcf = ncfile[model_tag + '_sspntcf']

    # 2. Mask the data for both land and sea
    single_ssp_land  = single_ssp.copy()
    single_ssp_ocean = single_ssp.copy()


    single_ssp_land.data[:,  mask_file['lsm'].data[0]<0.05]  = np.nan
    single_ssp_ocean.data[:, mask_file['lsm'].data[0]>0.05] = np.nan

    single_ntcf_land  = single_ntcf.copy()
    single_ntcf_ocean = single_ntcf.copy()

    single_ntcf_land.data[:, mask_file['lsm'].data[0]<0.05]  = np.nan
    single_ntcf_ocean.data[:,mask_file['lsm'].data[0]<0.05] = np.nan

    # 3. Calculate area-weighted average
    lat = ncfile.lat ; lon = ncfile.lon.data ; time = ncfile.time.data

    lat_rad = np.deg2rad(lat.data)
    weights = np.cos(lat_rad)

#    print(weights)

#    single_ntcf_ocean_weighted = single_ntcf_ocean.weighted(weights)
#
#    a = single_ntcf_ocean_weighted.mean("lat", "lon")
#    print(a)

    weights_2d = np.tile(weights, (1, len(lon)))

    print(weights_2d.shape)
    #print(np.sum(weights_2d))
#    weights_land  = np.where(mask_file['lsm'].data[0]>0.05, weights_2d, 0)
#    #print(np.sum(weights_land))
#    weights_ocean = np.where(mask_file['lsm'].data[0]<0.05, weights_2d, 0)
#
#    #print(weights)
#    #print(weights[:, np.newaxis].shape)
#    # 4. Claim the array for saving the single year average
#    land_sea_contrast_ssp  = np.zeros((len(time)))
#    land_sea_contrast_ntcf = np.zeros((len(time)))
#
#    start_point_land       = np.nansum(single_ssp_land.data[0] * weights_land) / np.nansum(weights_land)
#    start_point_ocean      = np.nansum(single_ssp_ocean.data[0]* weights_ocean) / np.nansum(weights_ocean)
#
#    print(np.nanmean(single_ssp_ocean.data[0]))
#    print(start_point_ocean)
#    print(np.nanmean(single_ssp.data[0]))

#    for tt in range(1, len(time)):
#        weighted_ssp_land    = single_ssp_land[tt]  * weights_2d
#        weighted_ssp_ocean   = single_ssp_ocean[tt] * weights_2d
#        weighted_ntcf_land   = single_ntcf_land[tt] * weights_2d
#        weighted_ntcf_ocean  = single_ntcf_ocean[tt]* weights_2d
#
#        land_sea_contrast_ssp[tt] = (np.nanmean(weighted_ssp_land) - start_point_land)  / (np.nanmean(weighted_ssp_ocean) - start_point_land)
#        land_sea_contrast_ntcf[tt]= (np.nanmean(weighted_ntcf_land) - start_point_land) / (np.nanmean(weighted_ntcf_ocean) - start_point_land)

        

    #print(land_sea_contrast_ssp)





if __name__ == '__main__':
    cal_land_sea_thermal_contrast(f0, models_label[1])