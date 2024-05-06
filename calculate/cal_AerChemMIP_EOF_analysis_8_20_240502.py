'''
2024-5-2
This script is to calculate the EOF for the 8-20 band-pass land precipitation
'''
import xarray as xr
import numpy as np
from eofs.standard import Eof

# ========= File Information ===========
f0  =  xr.open_dataset('/home/sun/data/process/analysis/AerChem/8-20_pr_MJJAS_multiple_model_result.nc')

f0_asia = f0.sel(lat=slice(0, 60), lon=slice(60, 140))

# =====================================

# ========= Calculation Part ==========
coslat  = np.cos(np.deg2rad(f0_asia.lat.data))
wgts    = np.sqrt(coslat)[:, np.newaxis]

modelmean_hist = f0_asia['hist_model'].mean(dim='model')
modelmean_ssp3 = f0_asia['ssp3_model'].mean(dim='model')
modelmean_ntcf = f0_asia['ntcf_model'].mean(dim='model')

solver_hist  = Eof(modelmean_hist.data, weights=wgts)
solver_ssp3  = Eof(modelmean_ssp3.data, weights=wgts)
solver_ntcf  = Eof(modelmean_ntcf.data, weights=wgts)

eof1_hist    = solver_hist.eofsAsCorrelation(neofs=1)
eof1_ssp3    = solver_ssp3.eofsAsCorrelation(neofs=1)
eof1_ntcf    = solver_ntcf.eofsAsCorrelation(neofs=1)

pc_hist      = solver_hist.pcs(npcs=1, pcscaling=1)
pc_ssp3      = solver_ssp3.pcs(npcs=1, pcscaling=1)
pc_ntcf      = solver_ntcf.pcs(npcs=1, pcscaling=1)

var_frac_hist= solver_hist.varianceFraction(neigs=1)
var_frac_ssp3= solver_ssp3.varianceFraction(neigs=1)
var_frac_ntcf= solver_ntcf.varianceFraction(neigs=1)



ncfile  =  xr.Dataset(
    {
        "eof1_hist":     (["time0", "lat", "lon"], eof1_hist),
        "eof1_ssp3":     (["time0", "lat", "lon"], eof1_ssp3),
        "eof1_ntcf":     (["time0", "lat", "lon"], eof1_ntcf),
        "pc_hist":       (["time_hist", "time0"], pc_hist),
        "pc_ssp3":       (["time_furt", "time0"], pc_ssp3),
        "pc_ntcf":       (["time_furt", "time0"], pc_ntcf),
        "var_frac_hist":     (["time0",], var_frac_hist),
        "var_frac_ssp3":     (["time0",], var_frac_ssp3),
        "var_frac_ntcf":     (["time0",], var_frac_ntcf),
    },
    coords={
        "model":        (["time0"],[0]),
        "lat":          (["lat"],  f0_asia.lat.data),
        "lon":          (["lon"],  f0_asia.lon.data),
    },
    )

out_path  = '/home/sun/data/process/analysis/AerChem/'

ncfile.attrs['description'] = 'Created on 2024-5-2 by cal_AerChemMIP_EOF_analysis_8_20_240502.py. This file save the 8-20 bandpass precipitation EOF1 result for all the three experiments.'
ncfile.to_netcdf(out_path + 'AerchemMIP_Asia_EOF_land_summertime_8-20_precipitation_hist_SSP370_NTCF.nc')  