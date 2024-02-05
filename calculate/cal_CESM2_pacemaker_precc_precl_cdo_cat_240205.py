'''
2024-2-5
This script is to post-process the output from the CESM2 pacemaker experiment
'''

## ==== Deal with the pacemaker experiment ====
from cdo import *
import os

cdo = Cdo()

path_model = '/mnt/win/CESM_pacemaker/precc/mon/'
#
sst_list   = os.listdir(path_model) ; sst_list.sort()
#
## ---- 1. Filter out irrevelant files ----

sst_list_1 = []
for ffff in sst_list:
    if ".py" in ffff or "BSSP" in ffff:
        continue
    else:
        sst_list_1.append(ffff)

# ---- 2. cdo cat each year ----

for year in range(10): # 10 ensemble members
    member_num = str(year + 1)

    if (year + 1) < 10:
        str1 = "00" + str(year + 1)
    else:
        str1 = "0"  + str(year + 1)

    #print(str1)
    str2     = ".pacemaker_pacific." + str1 + ".cam."
    #print(str2)
    # 2.1 filter out files for this year
    sst_list_2 = []
    for ffff in sst_list_1:
        #print(ffff)
        if str2 in ffff:
            sst_list_2.append(ffff)
    
    sst_list_2.sort()
    #print(sst_list_2)

    # 2.2 Cdo cat
    out_path = '/home/sun/data/download_data/CESM2_pacemaker/precc/mon/'
    cdo.cat(input=[(path_model + x) for x in sst_list_2], output=out_path + "CESM2" + str2 + "188001-201412.nc")

# ===== Deal with precl =====
path_model = '/mnt/win/CESM_pacemaker/precl/mon/'
#
sst_list   = os.listdir(path_model) ; sst_list.sort()
#
## ---- 1. Filter out irrevelant files ----

sst_list_1 = []
for ffff in sst_list:
    if ".py" in ffff or "BSSP" in ffff:
        continue
    else:
        sst_list_1.append(ffff)

# ---- 2. cdo cat each year ----

for year in range(10): # 10 ensemble members
    member_num = str(year + 1)

    if (year + 1) < 10:
        str1 = "00" + str(year + 1)
    else:
        str1 = "0"  + str(year + 1)

    #print(str1)
    str2     = ".pacemaker_pacific." + str1 + ".cam."
    #print(str2)
    # 2.1 filter out files for this year
    sst_list_2 = []
    for ffff in sst_list_1:
        #print(ffff)
        if str2 in ffff:
            sst_list_2.append(ffff)
    
    sst_list_2.sort()
    #print(sst_list_2)

    # 2.2 Cdo cat
    out_path = '/home/sun/data/download_data/CESM2_pacemaker/precl/mon/'
    cdo.cat(input=[(path_model + x) for x in sst_list_2], output=out_path + "CESM2" + str2 + "188001-201412.nc")