'''
2023-12-14
This script is to deal with the download of the CESM2 LE SF data
'''
import os

path0 = '/home/sun/CMIP6/LE_SF_CESM2/'
list1 = os.listdir(path0)

#var_list = []
#for ff in list1:
#    var_list.append(ff[12:])
#
#for f2 in var_list:
#    path1 = path0
#print(var_list)
#var_list = ''

for ff in list1:
    list2 = os.listdir(path0 + ff)

    # Delete the irrevelant file
    file_list = []
    py_list   = []
    for f2 in list2:
        if "b.e21.B1850cmip6" in f2:
            file_list.append(f2)
        elif ".py" in f2:
            py_list.append(f2)
    
    # Sort the file list and delete the last three files
    file_list.sort()

    # The following I have run so I mask them
#    os.system('rm -rf ' + path0 + ff + '/' + file_list[-1])
#    os.system('rm -rf ' + path0 + ff + '/' + file_list[-2])
#    os.system('rm -rf ' + path0 + ff + '/' + file_list[-3])
    os.chdir(path0 + ff + '/')
    os.system('nohup python ' + path0 + ff + '/' + py_list[0] + ' &')

#print(file_list)
#print(py_list)