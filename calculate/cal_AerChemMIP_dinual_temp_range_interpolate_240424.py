'''
2024-4-24
This script is to deal with the tropical nights (minimum larger than 20), intepolating them to the same grids

'''
import os
import xarray as xr
import numpy as np

#type0         = ['wet_day', 'pr10', 'pr10-25', 'pr1-10', 'pr20', 'pr25', 'pr10-20']


data_path    = '/home/sun/data/process/model/aerchemmip-postprocess/dtr/'

interp_path  = '/home/sun/data/process/model/aerchemmip-postprocess/dtr_regrid/'

#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'CESM2-WACCM', 'BCC-ESM1', 'NorESM2-LM', 'MPI-ESM-1-2-HAM', 'MIROC6', 'CNRM-ESM']
models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'MPI-ESM-1-2-HAM', 'MIROC6', ]

#variable_list  =  ['tas', 'sfcWind', 'hurs', 'hfss', 'hfls']
variable_list  =  ['wet_day',] # All of the above is wet_day

year_range = np.linspace(1985, 2014, 2014 - 1985 + 1)

def group_files_by_model(list_all, keyword):
    same_group = []

    for i in list_all:
        if keyword in i:
            same_group.append(i)
        else:
            continue
    
    same_group.sort()
    return same_group

def check_latitude(f0):
    print(f0.lat.data)

def check_longitude(f0):
    print(f0.lon.data)

def check_varname(f0):
    print(f0)

def unify_lat_lon(f0, new_lat, new_lon, filename, pathend):
    '''
        This function is to unify the lat/lon information for each inputed f0
    '''
    old_lat   = f0['lat'].data
    old_lon   = f0['lon'].data


    f0_interp = f0.interp(lat = new_lat, lon=new_lon,)

    f0_interp.to_netcdf(pathend + filename)
    #return f0_interp


def main():



    # 1. Get all files:
    files_all = os.listdir(data_path)

        # 2. return the information about latitude and longitude
        # === Result: all of them -90 to 90 for lat, and 0 to 365 for lon. Varname is pr ===
    #    for mm in models_label:
    #        model_group = group_files_by_model(files_all, mm)
    #
    #        f_lat = xr.open_dataset(data_path + model_group[0])
    #
    #        print(f'The model {mm} latitude is : \n')
    #        check_latitude(f_lat)

    #    for mm in models_label:
    #        model_group = group_files_by_model(files_all, mm)
    #
    #        f_lon = xr.open_dataset(data_path + model_group[0])
    #
    #        print(f'The model {mm} longitude is : \n')
    #        check_longitude(f_lon)

    #    for mm in models_label:
    #        model_group = group_files_by_model(files_all, mm)
    #
    #        ff = xr.open_dataset(data_path + model_group[0])
    #
    #        print(f'The model {mm} longitude is : \n')
    #        check_varname(ff)

    # 3. Interpolate
    # 1.5 x 1.5 resolution
    new_lat = np.linspace(-90, 90, 121)
    new_lon = np.linspace(0, 360, 241)

    for fff in files_all:
        if fff[0] == '.':
            continue
        elif fff[-2:] == 'nc':
            ff0 = xr.open_dataset(data_path + fff)
            if 'historical' in fff:
                ff0 = ff0.sel(time=ff0.time.dt.year.isin(year_range))
            else:
                ff0 = ff0.sel(time=ff0.time.dt.year.isin(np.linspace(2015, 2050, 36)))

            unify_lat_lon(ff0, new_lat, new_lon, fff, interp_path)

            print(f'Successfully interpolate the file {fff}')



if __name__ == '__main__':
    main()