'''
2024-4-9
This script is to deal with the CMIP6 PET relevant variables, intepolating them to the same grids

'''
import os
import xarray as xr
import numpy as np

data_path0    = '/data/AerChemMIP/LLNL_PET/postprocess/'

interp_path0  = '/data/AerChemMIP/LLNL_PET/postprocess-samegrid/'

#models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'CESM2-WACCM', 'BCC-ESM1', 'NorESM2-LM', 'MPI-ESM-1-2-HAM', 'MIROC6', 'CNRM-ESM']
models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'MPI-ESM-1-2-HAM', 'MIROC6', ]

#variable_list  =  ['tas', 'sfcWind', 'hurs', 'hfss', 'hfls']
variable_list  =  ['ps']

year_range = np.linspace(1950, 2014, 2014 - 1950 + 1)

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
    time_data = f0['time'].data

    f0_interp = f0.interp(lat = new_lat, lon=new_lon,)

    f0_interp.to_netcdf(pathend + filename)


def main():

    for vv in variable_list:
        data_path = data_path0 + vv + '/'
        interp_path=interp_path0 + vv + '/'

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
            else:
                ff0 = xr.open_dataset(data_path + fff)
                if 'historical' in fff:
                    ff  = ff0.sel(time=ff0.time.dt.year.isin(year_range))
                else:
                    ff  = ff0

                del ff0

                print(f'Now it is dealing with {fff}')

                unify_lat_lon(ff, new_lat, new_lon, fff, interp_path)

                print(f'Successfully interpolate the file {fff}')

    #    print(new_lat)
    #    print(new_lon)


if __name__ == '__main__':
    main()