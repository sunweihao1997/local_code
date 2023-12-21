'''
2023-12-16
This script is to cdo cat the whole period of the ncfile for each member from the CESM2_LE_SF experiments
'''
import os

path0 = '/home/sun/CMIP6/LE_SF_CESM2/CESM2_LE_SF_PRECT/'

file_all = os.listdir(path0)
#print(file_all)
file_sel = []

from cdo import *
cdo = Cdo()

for ff in file_all:
    if 'b.e21.B1850cmip6' in ff:
        file_sel.append(ff)

path_out = '/home/sun/CMIP6/LE_SF_CESM2/temporary/'

for mm in range(20):
    file_member = []
    for ff in file_sel:
        if str(mm + 1) + '.cam.' in ff:
            file_member.append(ff)
    
    #print(file_member)
    cdo.cat(input = [(path0 + x) for x in file_member],output = path_out + "test_"+str(mm+1)+".nc")