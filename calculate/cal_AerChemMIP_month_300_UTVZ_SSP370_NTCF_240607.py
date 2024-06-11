'''
2024-5-20
This script is to plot the changes in MJJAS ts between SSP370 and SSP370lowNTCF, the simulation of historical is ignored
'''
import xarray as xr
import numpy as np
from scipy import stats

path_in   =  '/home/sun/data/process/analysis/AerChem/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data
#models_label = ['EC-Earth3-AerChem'] # GISS provide no daily data
#models_label = ['UKESM1-0-LL'] # GISS provide no daily data

varname      = 'div'

gen_f     = xr.open_dataset('/home/sun/data/topography/geo_1279l4_0.1x0.1.grib2_v4_unpack.nc')

z         = gen_f['z'].data[0] / 9.8

def cal_multiple_model_avg(f0, exp_tag, timeaxis,):
    '''
    Because the input data is single model, so this function is to calculate the model-averaged data

    timeaxis is 65 for historical and 36 for furture simulation
    '''
    # 1. Generate the averaged array
    lat = f0.lat.data ; lon = f0.lon.data ; time = f0[timeaxis].data ; lev = f0.plev.data

    multiple_model_avg = np.zeros((len(time), len(lev), len(lat), len(lon)))

    # 2. Calculation
    models_num = len(models_label)

    for mm in models_label:
        varname1 = mm + '_' + exp_tag

        multiple_model_avg += (f0[varname1].data / models_num)

    #
    return multiple_model_avg


def cal_student_ttest(array1, array2):
    '''
        This function is to calculate the student ttest among the array1 and array2
    '''
    p_value = np.zeros((array1.shape[1], array2.shape[2]))

    for i in range(array1.shape[1]):
        for j in range(array2.shape[2]):
            #print(i)
            p_value[i, j] = stats.ttest_rel(array1[:, i, j], array2[:, i, j])[1]

    return p_value

if __name__ == '__main__':
    #--------- U -------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_ua_month_MJJAS_all.nc')

    ua_ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ua_ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    del f0

    # -------- V --------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_va_month_MJJAS_all.nc')

    va_ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    va_ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    del f0

    # -------- T ---------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_ta_month_MJJAS_all.nc')

    ta_ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    ta_ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    del f0

    # -------- Z ---------------
    f0  =  xr.open_dataset('/home/sun/data/AerChemMIP/process/multiple_model_climate_zg_month_MJJAS_all.nc')

    zg_ssp0      =  cal_multiple_model_avg(f0, 'ssp',  'time_ssp')
    zg_ntcf0     =  cal_multiple_model_avg(f0, 'sspntcf', 'time_ssp')

    
    

    # Write ncfile 

    ncfile  =  xr.Dataset(
        {
            "u_ssp":     (["lev", "lat", "lon"], np.nanmean(ua_ssp0,   axis=0)),     
            "v_ssp":     (["lev", "lat", "lon"], np.nanmean(va_ssp0,   axis=0)),    
            "t_ssp":     (["lev", "lat", "lon"], np.nanmean(ta_ssp0,   axis=0)),
            "z_ssp":     (["lev", "lat", "lon"], np.nanmean(zg_ssp0,   axis=0)),  
            "u_ntcf":    (["lev", "lat", "lon"], np.nanmean(ua_ntcf0,  axis=0)),     
            "v_ntcf":    (["lev", "lat", "lon"], np.nanmean(va_ntcf0,  axis=0)),    
            "t_ntcf":    (["lev", "lat", "lon"], np.nanmean(ta_ntcf0,  axis=0)),
            "z_ntcf":    (["lev", "lat", "lon"], np.nanmean(zg_ntcf0,  axis=0)),      
            "z_diff":    (["lev", "lat", "lon"], np.nanmean(zg_ssp0[-20:], axis=0) - np.nanmean(zg_ntcf0[-20:],  axis=0)),                   
        },
        coords={
            "lat":  (["lat"],  f0.lat.data),
            "lon":  (["lon"],  f0.lon.data),
            "lev":  (["lev"],  f0.plev.data),
            "time": (["time"], f0.time.data)
        },
        )

    ncfile.attrs['description'] = 'Created on 2024-6-7. This file save the modelmean climatological UTVZ at 300 hPa, which for the calculation of the wave activity flux'


    ncfile.to_netcdf("/home/sun/data/AerChemMIP/process/multiple_modelmean_climate_utvz_month_MJJAS.nc")
