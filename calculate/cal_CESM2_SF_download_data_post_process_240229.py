'''
2024-2-29
This script is to deal with the downloaded CESM2 SF experiment to show the long-term trend in May precipitation under different forcing
'''
import xarray as xr
import numpy as np
import os
from cdo import *
cdo = Cdo()

data_path = '/home/sun/data/download_data/CESM2_SF/mon_PRECT/'
out_path  = '/home/sun/data/download_data/CESM2_SF/mon_PRECT/cdo/'

files_all = os.listdir(data_path)
#print(len(files_all))
for ff in files_all:
    if ff[-2:] != 'nc':
        files_all.remove(ff) # Only keep the netcdf file
#print(len(files_all))

exp_names  = ['CESM2-SF-AAER', 'CESM2-SF-BMB', 'CESM2-SF-EE', 'CESM2-SF-GHG']

def return_special_group(list0, keywords):
    '''
        This function is to return a group for the files name which includes the keyword
    '''
    group_list = []

    for ff in list0:
        if keywords in ff and 'SSP370' not in ff:
            group_list.append(ff)

    group_list.sort()

    return group_list

def calculate_members_mean(filelist, varname):
    '''
        This function calculate and return the members mean for each group
    '''
    # Get the number of the members
    num_member = len(filelist)

    # Claim the array
    ref_file   = xr.open_dataset(data_path + filelist[1])
    mem_mean   = np.zeros(ref_file[varname].shape)

    for i in range(num_member):
        print(f'Now it is deal with file {filelist[i]}')
        f1 = xr.open_dataset(data_path + filelist[i])

        mem_mean += f1[varname].data / num_member

    return mem_mean

def cdo_files(lists):
    # Try to filter out each mini-group
    while len(lists) != 0:
        f0 = lists[0]
        f0_split = f0.split(".")
        name_exp = f0_split[4] ; name_mem = f0_split[5]

        mini_group = []
        for file0 in lists:
            f1_split = file0.split(".")
            if f1_split[4] == name_exp and f1_split[5] == name_mem:
                mini_group.append(file0)
            else:
                continue

        if len(mini_group) == 1:
            print(f'Single file list {mini_group}')
            lists.remove(mini_group[0])
            continue
        else:
            #print(mini_group)
            mini_group.sort()
            cdo.cat(input = [(data_path + x) for x in mini_group], output = out_path + mini_group[0][:-16] + 'nc')

            print('Successfully cat the {}'.format(mini_group[0][:-16]))
            for file1 in mini_group:
                #print('Now it is removing the {}'.format(file1))
                lists.remove(file1)


def main():
    # Deal with AAER experiment
    list_aaer = return_special_group(files_all, exp_names[0])

    #aaer_mean = calculate_members_mean(list_aaer, 'PRECT')
    #print(list_aaer[0].split('.'))
    #print(list_aaer[0][:-16])

    cdo_files(files_all)

if __name__ == '__main__':
    main()