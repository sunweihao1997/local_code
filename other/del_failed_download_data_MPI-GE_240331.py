'''
2024-3-1
This script is to check the failed data and delete them
'''
import os

path0 = '/home/sun/data/download_data/MPI-GE/CMIP6/u_day/'

fail_list = []
files_all = os.listdir(path0)
files_all_nc = [x for x in files_all if x[-2:] == 'nc']

for nn in files_all_nc:
    file_size = os.path.getsize(path0 + nn)

    limit_size = 1 * 1024 * 1024

    if file_size < limit_size:
        fail_list.append(nn)

fail_list.sort()
#print(fail_list)
for ff in fail_list:
    os.system('rm ' + path0 + ff)