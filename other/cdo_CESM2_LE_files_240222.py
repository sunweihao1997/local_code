'''
2024-2-22
This script is to cdo cat the CESM2 Large Ensemble output

Please note the strategy of the CESM LENS2 project includes two contents:
1. 10 members: initiated from 1001, 1021, 1041...
2. 40 members: 1231 10 members, 1251 10, 1281, 10, 1301 10
'''

import os
from multiprocessing import Pool

from cdo import *
cdo = Cdo()

src_path = '/home/sun/data/download_data/CESM2_LE/day_PRECT/raw/'
end_path = '/home/sun/data/download_data/CESM2_LE/day_PRECT/cdo/'

def get_allfiles(path0, keyword):
    pure_nc  = []

    file_all = os.listdir(path0)
    for ffff in file_all:
        if keyword in ffff:
            continue
        elif ffff[-2:] == 'nc':
            pure_nc.append(ffff)

    return pure_nc

def cdocat(lists, groupname):
    path_in  = src_path
    path_out = end_path

    # Notice the CESM LE is initiated from different conditions, here I should cdo by each group

    cdo.cat(input = [(path_in + x) for x in lists],output = path_out + groupname + "nc")

def group_id_division(list0):
    '''
        This function deal with all files included input and return the group name list
    '''
    group_id = []
    for ffff in list0:
        groupid = ffff[:50]

        if groupid in group_id:
            continue
        else:
            group_id.append(groupid)

    return group_id

def output_same_groupid(list0, groupname):
    same_group = []

    for ff in list0:
        if groupname in ff:
            same_group.append(ff)

    print(f'This group include {len(same_group)} files')

    same_group.sort()

    return same_group

def main():
    # 1. First, get all the files

    file_list = get_allfiles(src_path, 'python') ; file_list.sort()

    # 2. Verify the location of the ideal character
    #print(file_list[1][:34]) #b.e21.BHISTcmip6.f09_g17.LE2-1001.

    # 3. Get all the group name

    group_name = group_id_division(file_list)
    #print(len(group_name)) # 50 members

    # --- test ---
#    list_test = output_same_groupid(file_list, group_name[5])
#
#    cdocat(list_test, group_name[5])

    pool = Pool(50)
    for i in range(50):
        list_samegroup = output_same_groupid(file_list, group_name[i])

        pool.apply_async(cdocat, (list_samegroup, group_name[i]))

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()