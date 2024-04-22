'''
2024-3-29
This script is to calculate the change of the area of the global monsoon

In another script I used the monthly data and set 2.5 mm/day as criterion but the result is not very good
This trying is to see whether it will be better to use the daily data
'''
import xarray as xr
import numpy as np

data_path = '/home/sun/data/process/analysis/AerChem/'
data_name = 'multiple_model_climate_prect_daily_new.nc'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6',]

precip_f     = xr.open_dataset(data_path + data_name)

lat          = precip_f.lat.data ; lon        = precip_f.lon.data
time         = precip_f.time.data


def cal_modelmean(exp_tag):
    model_mean = np.zeros((len(time), len(lat), len(lon)))

    for mm in models_label:
        model_mean += (precip_f[mm + exp_tag].data / len(models_label))

    return model_mean * 86400 # mm/day

# Calculate the modelmean for hist, ssp370 and ssp370lowntcf
p_hist  =  cal_modelmean('_hist')
p_ssp3  =  cal_modelmean('_ssp')
p_ntcf  =  cal_modelmean('_sspntcf')

nh_summer_start = 120 ; nh_summer_end = 270 ; nh_winter_start = 300 ; nh_winter_end = 90
sh_summer_start = 300 ; sh_summer_end = 90  ; sh_winter_start = 120 ; sh_winter_end = 270

# ============= Calculate the summer, winter and percentum ==============
def calculate_summer_winter_annual(data, hemi):
    if hemi == 'nh':
        data_summer   = np.sum(data[nh_summer_start:nh_summer_end], axis=0)
        data_winter   = np.sum(data[nh_winter_start:], axis=0) + np.sum(data[:nh_winter_end], axis=0)
        data_annual   = np.sum(data, axis=0)

        percentum     = data_summer / data_annual
    if hemi == 'sh':
        data_winter   = np.sum(data[sh_winter_start:sh_winter_end], axis=0)
        data_summer   = np.sum(data[sh_summer_start:], axis=0) + np.sum(data[:sh_summer_end], axis=0)
        data_annual   = np.sum(data, axis=0)

        percentum     = data_summer / data_annual

    return data_summer, (data_summer - data_winter), percentum

# ============ calculate the whole field ====================
def calculate_summer_winter_annual_twohemi(data):
    diff_array      = np.zeros((len(lat), len(lon)))
    percentum_array = np.zeros((len(lat), len(lon)))
    summer_data     = np.zeros((len(lat), len(lon)))

    summer_data[45:], diff_array[45:], percentum_array[45:] = calculate_summer_winter_annual(data[:, 45:], 'nh')
    summer_data[:45], diff_array[:45], percentum_array[:45] = calculate_summer_winter_annual(data[:, :45], 'sh')

    return summer_data, diff_array, percentum_array

p_hist_summer, p_hist_diff, p_hist_percent = calculate_summer_winter_annual_twohemi(p_hist)
p_ssp_summer,  p_ssp_diff,  p_ssp_percent  = calculate_summer_winter_annual_twohemi(p_ssp3)
p_ntcf_summer, p_ntcf_diff, p_ntcf_percent = calculate_summer_winter_annual_twohemi(p_ntcf)

print(np.nanmin(p_hist_diff))
# ============ Judge the monsoon area ====================
area_hist = np.zeros((len(lat), len(lon)))
area_ssp  = np.zeros((len(lat), len(lon)))
area_ntcf = np.zeros((len(lat), len(lon)))
arid_hist = np.zeros((len(lat), len(lon)))
arid_ssp  = np.zeros((len(lat), len(lon)))
arid_ntcf = np.zeros((len(lat), len(lon)))

def judge_monsoon_area(diff_value, percentile):
    if diff_value > 300 and percentile > 0.55:
        return 1
    else:
        return 0

def judge_arid_area(summer_value,):
    if summer_value < 150:
        return 1
    else:
        return 0

for i in range(len(lat)):
    for j in range(len(lon)):
        area_hist[i, j] = judge_monsoon_area(p_hist_diff[i, j], p_hist_percent[i, j])
        area_ssp[i, j]  = judge_monsoon_area(p_ssp_diff[i, j],  p_ssp_percent[i, j])
        area_ntcf[i, j] = judge_monsoon_area(p_ntcf_diff[i, j], p_ntcf_percent[i, j])
        arid_hist[i, j] = judge_arid_area(p_hist_summer[i, j], )
        arid_ssp[i, j]  = judge_arid_area(p_ssp_summer[i, j], )
        arid_ntcf[i, j] = judge_arid_area(p_ntcf_summer[i, j], )

# ==== Write to ncfile ====

ncfile  =  xr.Dataset(
        {
            "hist_area":     (["lat", "lon"], area_hist),     
            "ssp_area":      (["lat", "lon"], area_ssp),     
            "ntcf_area":     (["lat", "lon"], area_ntcf),   
            "arid_hist":     (["lat", "lon"], arid_hist),     
            "arid_ssp":      (["lat", "lon"], arid_ssp),     
            "arid_ntcf":     (["lat", "lon"], arid_ntcf),       
        },
        coords={
            "lat":  (["lat"],  lat),
            "lon":  (["lon"],  lon),
        },
        )

ncfile.attrs['description'] = 'Created on 2024-3-29. This file save the area definition of the global monsoon, while 1 indicates it fullfil the criterion. The script is cal_AerChemMIP_global_monsoon_area_daily_240329.py.'
ncfile.attrs['reference']   = 'https://www.sciencedirect.com/science/article/pii/S0012825216302070'


ncfile.to_netcdf(data_path + 'globalmonsoon_area_modelmean_hist_ssp370_ssp370ntcf_300mm_dry_150.nc')