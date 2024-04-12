'''
2024-4-10
This script is to calculate the PET, calling the cal_AerChemMIP_PET_function_part_240409.py
'''
import xarray as xr
import numpy as np
import os

from cal_AerChemMIP_PET_function_part_240409 import *

path_in0 = '/data/AerChemMIP/LLNL_PET/postprocess-samegrid/'

varslist = ['hfls', 'hfss', 'hurs', 'ps', 'sfcwind', 'tas']

def get_files(varname):
    file_list = os.listdir(path_in0 + varname) ; file_list.sort()

    return file_list

def check_same_file(num0):
    if hfls_list[num0] == hfss_list[num0] == hurs_list[num0] == ps_list[num0] == sfcwind_list[num0] == tas_list[num0]:
        print('True')
    else:
        print(f'False for {num0}')

def Check_same_unit(num0):
    hfls0    = xr.open_dataset(path_in0 + 'hfls' + '/' + hfls_list[num0])
    hfss0    = xr.open_dataset(path_in0 + 'hfss' + '/' + hfss_list[num0])
    hurs0    = xr.open_dataset(path_in0 + 'hurs' + '/' + hurs_list[num0])
    ps0      = xr.open_dataset(path_in0 + 'ps' + '/' + ps_list[num0])
    tas0     = xr.open_dataset(path_in0 + 'tas' + '/' + tas_list[num0])
    sfcwind0 = xr.open_dataset(path_in0 + 'sfcwind' + '/' + sfcwind_list[num0])

    j = 0
    if hfls0['hfls'].attrs['units'] == hfls_ref['hfls'].attrs['units']:
        j += 1
    if hfss0['hfss'].attrs['units'] == hfss_ref['hfss'].attrs['units']:
        j += 1
    if hurs0['hurs'].attrs['units'] == hurs_ref['hurs'].attrs['units']:
        j += 1
    if ps0['ps'].attrs['units']   == ps_ref['ps'].attrs['units']:
        j += 1
    if tas0['tas'].attrs['units']   == tas_ref['tas'].attrs['units']:
        j += 1
    if sfcwind0['sfcWind'].attrs['units'] == sfcwind_ref['sfcWind'].attrs['units']:
        j += 1
    if j == 6:
        print('Yes the units are same')

hfls_list = get_files('hfls')
hfss_list = get_files('hfss')
hurs_list = get_files('hurs')
ps_list   = get_files('ps')
sfcwind_list   = get_files('sfcwind')
tas_list  = get_files('tas')

# ======== Read reference file =======
hfls_ref    = xr.open_dataset(path_in0 + 'hfls' + '/' + hfls_list[0])
hfss_ref    = xr.open_dataset(path_in0 + 'hfss' + '/' + hfss_list[0])
hurs_ref    = xr.open_dataset(path_in0 + 'hurs' + '/' + hurs_list[0])
ps_ref      = xr.open_dataset(path_in0 + 'ps' + '/' + ps_list[0])
tas_ref     = xr.open_dataset(path_in0 + 'tas' + '/' + tas_list[0])
sfcwind_ref = xr.open_dataset(path_in0 + 'sfcwind' + '/' + sfcwind_list[0])


# ======== Start calculate the PET ==========
end_path    = '/data/AerChemMIP/LLNL_PET/postprocess-samegrid/pet/'

filenum     = len(hfls_list) #; print(filenum)
for num in range(filenum):
    print(tas_list[num])
    # 1. Check if it the same among the variable
    #check_same_file(num) # All the same

    # 2. Check if it the same unit
    #Check_same_unit(num) # All the same

    # 3. Start calculate the pet
    temp1   = xr.open_dataset(path_in0 + 'tas' + '/' + tas_list[num])
    sh1     = xr.open_dataset(path_in0 + 'hfss' + '/' + hfss_list[num])
    lh1     = xr.open_dataset(path_in0 + 'hfls' + '/' + hfls_list[num])
    sfcwind1= xr.open_dataset(path_in0 + 'sfcwind' + '/' + sfcwind_list[num])
    ps1     = xr.open_dataset(path_in0 + 'ps' + '/' + ps_list[num])
    rh1     = xr.open_dataset(path_in0 + 'hurs' + '/' + hurs_list[num])

    pet1, pet1_rad, pet1_adv    = PenMon(temp1['tas'].data, sh1['hfss'].data, lh1['hfls'].data, sfcwind1['sfcWind'].data, ps1['ps'].data, rh1['hurs'].data, temp1['tas'].attrs['units'])

    #print(np.nanmean(pet1))
    # Save to the netcdf file
#    ncfile  =  xr.Dataset(
#        {
#            "pet":     (["time", "lat", "lon"], pet1),
#            "pet_rad":     (["time", "lat", "lon"], pet1_rad),     
#            "pet_adv":     (["time", "lat", "lon"], pet1_adv),                   
#        },
#        coords={
#            "time": (["time"], temp1['time'].data),
#            "lat":  (["lat"],  temp1['lat'].data),
#            "lon":  (["lon"],  temp1['lon'].data),
#        },
#        )
#
#    ncfile['pet'].attrs['units'] = 'mm/day'
#
#    ncfile.attrs['description'] = 'Created on 2024-4-10. This file used variables from CMIP6 to calculate the potential evapotranspiration which script is cal_AerChemMIP_PET_runpart_240410.py. The reference is https://www.nature.com/articles/s41597-023-02290-0'
#    #ncfile.attrs['Note']        = 'This pentad averaged precipitation does not includes NorESM'
#
#    ncfile.to_netcdf(end_path + tas_list[num])



# ======== Test part =============
# Read the list of each variable

#print(hfls_list[50])
#print(hfss_list[50])

# The file name under different variable's path is the same
# ======== End of the Test part =========

# ======== Test part =============
# Get information about hurs

#f_test = xr.open_dataset(path_in0 + varslist[2] + '/' + hurs_list[5])
#print(f_test['hurs'].attrs)

# The mean value is about 75, so its unit should be percentile
# ================================