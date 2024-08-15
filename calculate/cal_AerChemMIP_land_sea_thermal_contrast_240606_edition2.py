'''
2024-6-6
This script is to calculate the land-sea thermal contrast based on SSP370 and SSP370lowNTCF experiments
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


# =============== Read file =============

f0 = xr.open_dataset("/data/AerChemMIP/process/multiple_model_climate_ts_month_MJJAS_36years.nc").sel(lat=slice(-80, 80))

mask_file = xr.open_dataset("/data/AerChemMIP/process/ERA5_land_sea_mask_model-grid.nc")
# Need to interpolate
mask_file = mask_file.interp(latitude=f0.lat.data, longitude=f0.lon.data)

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G']


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
    single_ntcf_ocean.data[:,mask_file['lsm'].data[0]>0.05] = np.nan

    # 3. Calculate area-weighted average
    lat = ncfile.lat ; lon = ncfile.lon.data ; time = ncfile.time.data

    lat_rad = np.deg2rad(lat.data)
    weights = np.cos(lat_rad)

    weights_2d = np.tile(weights[:, np.newaxis], (1, len(lon)))
    
    weights_land  = np.where(mask_file['lsm'].data[0]>0.05, weights_2d, 0)
    weights_ocean = np.where(mask_file['lsm'].data[0]<0.05, weights_2d, 0)

    # 4. Claim the array for saving the single year average
    land_sea_contrast_ssp  = np.zeros((len(time)))
    land_sea_contrast_ntcf = np.zeros((len(time)))

    start_point_land       = np.nansum(single_ssp_land.data[0] * weights_land)  / np.nansum(weights_land)
    start_point_ocean      = np.nansum(single_ssp_ocean.data[0]* weights_ocean) / np.nansum(weights_ocean)


    for tt in range(1, len(time)):
        weighted_ssp_land    = np.nansum(single_ssp_land.data[tt] * weights_land)    / np.nansum(weights_land)
        weighted_ssp_ocean   = np.nansum(single_ssp_ocean.data[tt]* weights_ocean)   / np.nansum(weights_ocean)
        weighted_ntcf_land   = np.nansum(single_ntcf_land.data[tt] * weights_land)    / np.nansum(weights_land)
        weighted_ntcf_ocean  = np.nansum(single_ntcf_ocean.data[tt]* weights_ocean)  / np.nansum(weights_ocean)


        land_sea_contrast_ssp[tt] = (weighted_ssp_land - start_point_land)  - (weighted_ssp_ocean - start_point_ocean)
        land_sea_contrast_ntcf[tt]= (weighted_ntcf_land - start_point_land) - (weighted_ntcf_ocean - start_point_ocean)

    return land_sea_contrast_ssp, land_sea_contrast_ntcf

def paint_evolution_landsea_contrast(ssp, sspntcf, ssp_std, ntcf_std, left_string, right_string,):
    fig, ax = plt.subplots(figsize=(25, 10))

    # Paint the member average
    ax.plot(np.linspace(2015, 2050, 36), ssp,     color='royalblue',      linewidth=3.25, alpha=1, label='SSP370')
    ax.plot(np.linspace(2015, 2050, 36), sspntcf, color='red',            linewidth=3.25, alpha=1, label='SSP370lowNTCF')

    # Paint the model deviation
    ax.fill_between(np.linspace(2015, 2050, 36), ssp   + ssp_std,     ssp  - ssp_std, facecolor='royalblue', alpha=0.2)
    ax.fill_between(np.linspace(2015, 2050, 36), sspntcf  + ntcf_std, sspntcf - ntcf_std, facecolor='red', alpha=0.2)

    plt.legend(loc='lower right', fontsize=25)

    ax.set_title(left_string,  loc='left',  fontsize=25)
    ax.set_title(right_string, loc='right', fontsize=25)

    plt.savefig(f"/data/paint/SSP370_SSP370lowNTCF_landsea_thermal_contrast.png", dpi=500)

    plt.close()


if __name__ == '__main__':
    # 1. Claim the all-models array
    land_sea_contrast_ssp_all  = np.zeros((7, 36))
    land_sea_contrast_ntcf_all = np.zeros((7, 36))

    j = 0
    for mm in models_label:
        land_sea_contrast_ssp_all[j], land_sea_contrast_ntcf_all[j] = cal_land_sea_thermal_contrast(f0, mm)

        j += 1

        print(f'Finish calculating model {mm}')
    
    land_sea_contrast_ssp_std  = np.std(land_sea_contrast_ssp_all, axis=0)
    land_sea_contrast_ntcf_std = np.std(land_sea_contrast_ntcf_all, axis=0)

#    print(land_sea_contrast_ntcf_std)

    # 2. Send to plot
    paint_evolution_landsea_contrast(np.average(land_sea_contrast_ssp_all, axis=0), np.average(land_sea_contrast_ntcf_all, axis=0), land_sea_contrast_ssp_std, land_sea_contrast_ntcf_std, 'Land-Sea thermal contrast', 'Boreal Summer')