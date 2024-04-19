'''
2024-4-16
This script is to show the trend of the wet days under different scenarios

reference:
1. region devision:
https://www.researchgate.net/publication/357688312_Fractional_contribution_of_global_warming_and_regional_urbanization_to_intensifying_regional_heatwaves_across_Eurasia

2. panel reference:
https://doi.org/10.1073/pnas.2219825120

2024-4-18:The new edition is that I realize the wide range among model could be due to the std calculation. I should first calculate the spatial average and then calculate the std.
'''
import numpy as np
import xarray as xr

# ============================ File Information =====================================
models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ] # GISS provide no daily data
type0        = ['wet_day', 'pr10', 'pr10-25', 'pr1-10', 'pr20', 'pr25',]

path_src = '/home/sun/data/process/analysis/AerChem/'

region_division = {
    'CAS':[30, 50, 60, 75], 'EAS':[20, 50, 100, 145], 'NAS':[50, 70, 40, 180], 'SEA':[-10, 20, 95, 155], 'SAS':[5, 30, 60, 100], 'TIB':[30, 50, 75, 100], 'WAS':[15, 50, 40, 60], 'Asia':[0, 60, 70, 150],
}
# ===================================================================================

def cal_multiple_model_avg(f0, exp_tag, timeaxis, varname='wet_day'):

    '''
    Because the input data is single model, so this function is to calculate the model-averaged data

    timeaxis is 65 for historical and 36 for furture simulation
    '''
    # 1. Generate the averaged array
    lat = f0.lat.data ; lon = f0.lon.data ; time = f0[timeaxis].data

    multiple_model_avg   = np.zeros((len(time), len(lat), len(lon)))

    # 2. Calculation
    models_num = len(models_label) # model and realization (3)
    multiple_model_value = np.zeros((models_num, len(time), len(lat), len(lon))) # This array is to calculate the uncertainity

    j = 0
    for mm in models_label:
        varname1 = varname + '_' + mm + '_' + exp_tag

        multiple_model_avg += (f0[varname1].data / models_num)

        multiple_model_value[j] = f0[varname1].data

        j  += 1


    # add the geography information
    multiple_model_avg_nc  =  xr.Dataset(
        {
            "multiple_model_avg":     (["time", "lat", "lon"], multiple_model_avg), 
            "multiple_model_value":   (["modellabel", "time", "lat", "lon"], multiple_model_value), 
        },
        coords={
            "time": (["time"], time),
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
            "modellabel": (["modellabel"], models_label),
        },
        )
    
    return multiple_model_avg_nc


def plot_trend_uncertainity(fhist, fssp, fntcf, region_slice, type1):
    '''
        This function is to calculate the regional precipitation index evolution and uncertainity
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import matplotlib.patches as patches
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    import sys
    sys.path.append("/home/sun/local_code/module/")
    from module_sun import set_cartopy_tick

    # 1. Select the region
    scale_region = region_division[region_slice]
    fhist_region = fhist.sel(lat=slice(scale_region[0], scale_region[1]), lon=slice(scale_region[2], scale_region[3]))
    fssp_region  = fssp.sel(lat=slice(scale_region[0], scale_region[1]), lon=slice(scale_region[2], scale_region[3]))
    fntcf_region = fntcf.sel(lat=slice(scale_region[0], scale_region[1]), lon=slice(scale_region[2], scale_region[3]))

    # 2. calculate the area average
    # varname is multiple_model_avg and multiple_model_std
    # 2.1 Claim the preliminary array
    fhist_avg    = np.average(np.average(fhist_region['multiple_model_avg'].data, axis=1), axis=1) - np.average(fhist_region['multiple_model_avg'].data)
    fssp_avg     = np.average(np.average(fssp_region['multiple_model_avg'].data, axis=1), axis=1)  - np.average(fhist_region['multiple_model_avg'].data)
    fntcf_avg    = np.average(np.average(fntcf_region['multiple_model_avg'].data, axis=1), axis=1) - np.average(fhist_region['multiple_model_avg'].data)
    #print(fhist_avg)

    fhist_std    = np.std(np.average(np.average(fhist_region['multiple_model_value'].data, axis=2), axis=2) - np.average(fhist_region['multiple_model_avg'].data), axis=0)
    fssp_std     = np.std(np.average(np.average(fssp_region['multiple_model_value'].data,  axis=2), axis=2) - np.average(fhist_region['multiple_model_avg'].data), axis=0)
    fntcf_std    = np.std(np.average(np.average(fntcf_region['multiple_model_value'].data, axis=2), axis=2) - np.average(fhist_region['multiple_model_avg'].data), axis=0)
#    print(fssp_std.shape)

    avg_ssp  = np.concatenate((fhist_avg, fssp_avg))
    avg_ntcf = np.concatenate((fhist_avg, fntcf_avg))
    std_ssp  = np.concatenate((fhist_std, fssp_std))
    std_ntcf = np.concatenate((fhist_std, fntcf_std))

    # Plot the picture
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(np.linspace(2015, 2050, 36), avg_ssp[65:],     color='royalblue',      linewidth=3.25, alpha=1, label='SSP370')
    ax.plot(np.linspace(2015, 2050, 36), avg_ntcf[65:],    color='red',            linewidth=3.25, alpha=1, label='SSP370NTCF')

    # Paint the model deviation
    ax.fill_between(np.linspace(2015, 2050, 36), avg_ssp[65:]  + std_ssp[65:],  avg_ssp[65:]  - std_ssp[65:],  facecolor='royalblue', alpha=0.2)
    ax.fill_between(np.linspace(2015, 2050, 36), avg_ntcf[65:] + std_ntcf[65:], avg_ntcf[65:] - std_ntcf[65:], facecolor='red', alpha=0.2)

    plt.legend(loc='upper left', fontsize=25.5)

    ax.set_title(type1       ,  loc='left',  fontsize=35)
    ax.set_title(region_slice, loc='right', fontsize=35)

    plt.savefig(f"/home/sun/paint/AerMIP/regional_precip_index/{region_slice}_{type1}_trend_2000-2050_realization_include_for_std_new.png", dpi=700)

    plt.close()





def main1():
    '''
        This function intends to visualize the trend and uncertainity for different area
    '''
    # 1. calculate the model-average for the different scanarios
    for type1 in type0:
        filename1 = 'multiple_model_climate_' + type1 + '.nc'

        f1        = xr.open_dataset(path_src + filename1)

        hist_nc   = cal_multiple_model_avg(f1, 'hist', 'time_hist', type1)
        ssp_nc    = cal_multiple_model_avg(f1, 'ssp',  'time_ssp',  type1)
        ntcf_nc   = cal_multiple_model_avg(f1, 'sspntcf', 'time_ssp',  type1)

        # 2. Send to plot picture
        for key, value in region_division.items():
            plot_trend_uncertainity(hist_nc, ssp_nc, ntcf_nc, key, type1)

if __name__ == '__main__':
    main1()
