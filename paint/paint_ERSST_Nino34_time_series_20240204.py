'''
2024-2-4
This script is to calculate the Nino34 index using ERSST data
'''
import xarray as xr
import numpy as np
import os

ersst = xr.open_dataset('/home/sun/data/download_data/ERSST/sst.mnmean.nc')

# time selection is 1980-2014
ersst_time = ersst.sel(time=ersst.time.dt.year.isin(np.linspace(1980, 2014, 35)))

ersst_time_nino34 = ersst_time.sel(lat=slice(5, -5), lon=slice(190, 240))

#print(ersst_time_nino34)

Nino34 = np.array([])

for yy in range(420):
    Nino34 = np.append(Nino34, np.nanmean(ersst_time_nino34['sst'].data[yy]))

## ==== Deal with the pacemaker experiment ====
#from cdo import *
#import os
#
#cdo = Cdo()
#
path_model = '/home/sun/data/download_data/CESM2_pacemaker/sst/mon/'
#
sst_list   = os.listdir(path_model) ; sst_list.sort()
#
## ---- 1. Filter out irrevelant files ----
#
#sst_list_1 = []
#for ffff in sst_list:
#    if ".py" in ffff or "BSSP" in ffff:
#        continue
#    else:
#        sst_list_1.append(ffff)
#
## ---- 2. cdo cat each year ----
#
#for year in range(10): # 10 ensemble members
#    member_num = str(year + 1)
#
#    if (year + 1) < 10:
#        str1 = "00" + str(year + 1)
#    else:
#        str1 = "0"  + str(year + 1)
#
#    #print(str1)
#    str2     = ".pacemaker_pacific." + str1 + ".cam."
#    #print(str2)
#    # 2.1 filter out files for this year
#    sst_list_2 = []
#    for ffff in sst_list_1:
#        #print(ffff)
#        if str2 in ffff:
#            sst_list_2.append(ffff)
#    
#    sst_list_2.sort()
#    #print(sst_list_2)
#
#    # 2.2 Cdo cat
#    out_path = '/home/sun/data/download_data/CESM2_pacemaker/sst/temporary/'
#    cdo.cat(input=[(path_model + x) for x in sst_list_2], output=out_path + "CESM2" + str2 + "188001-201412.nc")

#print(sst_list)

# ==== Verify whether the Nino34 index is consistent in the model ====

ersst = xr.open_dataset(path_model + sst_list[3])

ersst_time = ersst.sel(time=ersst.time.dt.year.isin(np.linspace(1980, 2014, 35)))

ersst_time_nino34 = ersst_time.sel(lat=slice(-5, 5), lon=slice(190, 240))

Nino34_model = np.array([])

for yy in range(420):
    Nino34_model = np.append(Nino34_model, np.nanmean(ersst_time_nino34['SST'].data[yy]))

Nino34_model = Nino34_model - 273.15
Nino34_model_anomaly = Nino34_model - np.average(Nino34_model)
Nino34_anomaly       = Nino34 - np.average(Nino34)


print(Nino34_anomaly - Nino34_model_anomaly)