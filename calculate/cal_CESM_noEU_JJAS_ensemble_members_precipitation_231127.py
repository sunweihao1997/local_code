'''
2023-11-27
This script is calculate JJAS precipitation for each year and each member from original ensemble members
'''
import xarray as xr
import numpy as np
import os

# ===================== Files location ========================

file_path  = '/mnt/d/samssd/precipitation/CESM/ensemble_original/'
file_name0 = 'noEU_PRECC_1850_150years_member_'
file_name1 = 'noEU_PRECL_1850_150years_member_'

# =============================================================

# ------------ 1. Get the file list ----------------

list_all = os.listdir(file_path)
list_precc = []
list_precl = []

for ffff in list_all:
    if 'noEU' in ffff and 'PRECC' in ffff:
        list_precc.append(ffff)
    elif 'noEU' in ffff and 'PRECL' in ffff:
        list_precl.append(ffff)
    else:
        continue

#print(len(list_precc)) ; print(len(list_precl))
list_precl.sort() ; list_precc.sort()

# ------------------------------------------------------

# ------------ 2. calculation ----------------------
def cal_season_average(path, name, varname):
    '''
        The input is ncfile
    '''

    data = xr.open_dataset(path + name)

    # 1. Select the JJAS data
    data_JJAS = data.sel(time=data.time.dt.month.isin([6, 7, 8, 9]))

    #print(data_JJAS)
    # 2. Claim the array to save
    year_number = 157 ; shape = data_JJAS[varname].data.shape
    JJAS_prect = np.zeros((year_number, shape[1], shape[2]))

    # 3. Calculation
    for yyyy in range(year_number):
        JJAS_prect[yyyy] = np.average(data_JJAS[varname].data[yyyy*4 : yyyy*4+4], axis=0)

    return JJAS_prect

# ------------ 3. calculation and save to file --------------
ref_file = xr.open_dataset(file_path + list_precc[0])
ncfile  =  xr.Dataset(
    {
        "JJAS_prect_{}".format(0 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[0], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[0], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(1 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[1], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[1], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(2 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[2], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[2], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(3 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[3], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[3], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(4 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[4], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[4], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(5 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[5], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[5], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(6 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[6], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[6], varname='PRECC')) * 86400 * 1000),
        "JJAS_prect_{}".format(7 + 1): (["time", "lat", "lon"], (cal_season_average(path=file_path, name=list_precl[7], varname='PRECL') + cal_season_average(path=file_path, name=list_precc[7], varname='PRECC')) * 86400 * 1000),
                                        
    },
    coords={
        "time": (["time"], np.linspace(1850, 1850+156, 157)),
        "lat":  (["lat"],  ref_file['lat'].data),
        "lon":  (["lon"],  ref_file['lon'].data),
    },
    )

for mm in range(8):
    ncfile["JJAS_prect_{}".format(mm + 1)].attrs['units'] = 'mm day-1'

ncfile.attrs['description'] = 'Created on 2023-11-27. This file save the JJAS precipitation for each year from the fixEU experiment. Please note that the unit has been changed to the mm per day'
ncfile.attrs['Mother'] = 'local-code: cal_CESM_noEU_JJAS_ensemble_members_precipitation_231127.py'
#
out_path = '/mnt/d/samssd/precipitation/CESM/ensemble_JJAS/'
ncfile.to_netcdf(out_path + 'CESM_noEU_esemble_JJAS_precipitation.nc')