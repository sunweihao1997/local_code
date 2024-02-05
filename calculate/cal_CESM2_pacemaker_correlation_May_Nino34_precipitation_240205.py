'''
2024-2-5
This script is to calculate the correlation between the May precipitation and Nino34 index in the CESM2 pacemaker experiment

Temporal range is 1980-2014, 35 years
'''

import xarray as xr
import numpy as np
import scipy.stats

src_datapath = '/home/sun/data/process/model/'

f0_precip    = xr.open_dataset(src_datapath + 'CESM2_pacemaker_PRECC_PRECL_10members_1880-2014.nc')
f0_sst       = xr.open_dataset(src_datapath + 'CESM2_pacemaker_SST_10members_1880-2014.nc')

# ==== Time selection for 1980-2014, May
f0_precip_sely = f0_precip.sel(time=f0_precip.time.dt.year.isin(np.linspace(1980, 2014, 35)))
f0_precip_selm = f0_precip_sely.sel(time=f0_precip_sely.time.dt.month.isin([5]))

f0_sst_sely    = f0_sst.sel(time=f0_sst.time.dt.year.isin(np.linspace(1980, 2014, 35)))
f0_sst_selm    = f0_sst_sely.sel(time=f0_sst_sely.time.dt.month.isin([5]), lat=slice(-5, 5), lon=slice(190, 240))

# ==== Calculate the members-mean ====

May_precip     = np.average(f0_precip_selm['PRECC'].data, axis=0) + np.average(f0_precip_selm['PRECL'].data, axis=0)
May_sst        = np.average(f0_sst_selm['SST'].data, axis=0)

May_Nino34     = np.average(np.average(May_sst, axis=1), axis=1)
May_Nino34     = May_Nino34 - np.average(May_Nino34)

#print(May_precip.shape) # (35, 192, 288)

# ==== Calculate the correlation ====

corre   = np.zeros((192, 288))
p_value = np.zeros((192, 288))

for i in range(192):
    for j in range(288):
        pearson_r     = scipy.stats.pearsonr(May_Nino34, (May_precip[:, i, j] - np.average(May_precip[:, i, j])))    
        corre[i, j]   = pearson_r[0]
        p_value[i, j] = pearson_r[1]

# ==== Save to the array ====

ncfile  =  xr.Dataset(
    {
        "corre":   (["lat", "lon"], corre),
        "p_value": (["lat", "lon"], p_value),
    },
    coords={
        "lat":    (["lat"],    f0_precip['lat'].data),
        "lon":    (["lon"],    f0_precip['lon'].data),
    },
        )

# ---- 1.1.1 Add attributes ----

ncfile['corre'].attrs['description'] = 'Pearson correlation between ensemble-averaged Nino34 and precipitation in May.'

ncfile.attrs['description'] = 'Create on 2024-2-5 on the Huaibei Server. This netcdf file saves Pearson correlation between ensemble-averaged Nino34 and precipitation in May.'

ncfile.to_netcdf('/home/sun/data/process/analysis/CESM2_pacemaker_correlation_May_precipitation_Nino34.nc')