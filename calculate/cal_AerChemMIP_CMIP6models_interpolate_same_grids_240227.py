'''
2024-2-27
This script is trying to Unify the resolutions of different climate models using interpolation.
'''
import os
import xarray as xr
import numpy as np

data_path    = '/Volumes/Untitled/AerChemMIP/LLNL_download/postprocess/'

interp_path  = '/Volumes/Untitled/AerChemMIP/LLNL_download/postprocess_samegrids/'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2', 'GISS-E2-1-G', 'CESM2-WACCM', 'BCC-ESM1']

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

def unify_lat_lon(f0, new_lat, new_lon, filename):
    '''
        This function is to unify the lat/lon information for each inputed f0
    '''
    old_lat   = f0['lat'].data
    old_lon   = f0['lon'].data
    time_data = f0['time'].data

    f0_interp = f0.interp(lat = new_lat, lon=new_lon)

    f0_interp.to_netcdf(interp_path + filename)


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
        print(f'Now it is dealing with {fff}')
        if fff[0] == '.':
            continue
        else:
            ff = xr.open_dataset(data_path + fff)
            unify_lat_lon(ff, new_lat, new_lon, fff)

            print(f'Successfully interpolate the file {fff}')

#    print(new_lat)
#    print(new_lon)


if __name__ == '__main__':
    main()