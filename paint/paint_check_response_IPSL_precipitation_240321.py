'''
2024-3-21
This script is to plot the precipitation over tropical Asia in May and June
Because the response to the aerosol reduction in NorESM is different with others, so this script is to check it
'''
import xarray as xr
import numpy as np

data_path = '/Users/sunweihao/Downloads/IPSL/'

ref_file  = xr.open_dataset(data_path + 'pr_Amon_IPSL-CM5A2-INCA_ssp370-lowNTCF_r1i1p1f1_gr_201501-205512.nc')

# Select the range of the year
year_range = np.linspace(2015, 2050, 2050 - 2015 + 1)
mon_range  = [5]
lat        = ref_file.lat.data 
lon        = ref_file.lon.data
lat_range  = slice(5,  20)
lon_range  = slice(90, 120)

# Put the data into the array
ref_file_select = ref_file.sel(lat=slice(5, 20), lon=slice(90, 120)).sel(time=ref_file.time.dt.year.isin(year_range))

#print(len(ref_file_select.time.data))

ssp370  = np.zeros((len(year_range)))
lowNTCF = np.zeros((len(year_range)))

file_ssp370 = ['pr_Amon_IPSL-CM5A2-INCA_ssp370_r1i1p1f1_gr_201501-205512.nc',]
file_NTCF   = ['pr_Amon_IPSL-CM5A2-INCA_ssp370-lowNTCF_r1i1p1f1_gr_201501-205512.nc',]

member=0
f0_ssp370 = xr.open_dataset(data_path + file_ssp370[member]).sel(lat=lat_range, lon=lon_range)
f0_NTCF   = xr.open_dataset(data_path + file_NTCF[member]).sel(lat=lat_range, lon=lon_range)

f1_ssp370 = f0_ssp370.sel(time=f0_ssp370.time.dt.month.isin(mon_range))
f1_NTCF   = f0_NTCF.sel(time=f0_NTCF.time.dt.month.isin(mon_range))

for yyyy in range(len(year_range)):
    ssp370[yyyy] = np.average(f1_ssp370['pr'].data[yyyy])
    lowNTCF[yyyy]= np.average(f1_NTCF['pr'].data[yyyy])


import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10)

plt.plot(year_range, 86400 * ssp370, color='k', linewidth=3)
plt.plot(year_range, 86400 * lowNTCF,  color='r', linewidth=3)


plt.savefig('IPSL.png')