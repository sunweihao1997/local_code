'''
2023-12-16
This script is to cdo cat the whole period of the ncfile for each member from the CESM2_LE_SF experiments
'''
import os
from multiprocessing import Pool

path0 = '/home/sun/CMIP6/LE_SF_CESM2/CESM2_LE_SF_PRECT/'

file_all = os.listdir(path0)
#print(file_all)
file_sel = []

from cdo import *
cdo = Cdo()

# defind method
def cdocat(lists, member):
    path_in  = '/home/sun/CMIP6/LE_SF_CESM2/CESM2_LE_SF_PRECT/'
    path_out = '/home/sun/CMIP6/LE_SF_CESM2/CESM2_LE_SF_PRECT/Aggregated/'

    cdo.cat(input = [(path_in + x) for x in lists],output = path_out + "PRECT_CESM2_SF_LE_" + member + ".nc")


for ff in file_all:
    if 'b.e21.B1850cmip6' in ff:
        file_sel.append(ff)

path_out = '/home/sun/CMIP6/LE_SF_CESM2/temporary/'

pool = Pool(20)

for mm in range(20):
    file_member = []
    for ff in file_sel:
        if "0" + str(mm + 1) + '.cam.' in ff:
            file_member.append(ff)
    #print(len(file_member))
    file_member.sort()
    
    pool.apply_async(cdocat, (file_member, str(mm + 1)))
    
pool.close()
pool.join()