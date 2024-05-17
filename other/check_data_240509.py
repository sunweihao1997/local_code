import xarray as xr
import numpy as np
from scipy import stats

f0 = xr.open_dataset("/home/sun/data/process/analysis/AerChem/rlut_MJJAS_multiple_model_result.nc").sel(lat=slice(0, 60), lon=slice(30, 120))

print(np.std(f0['ssp3_model']))
#f1 = xr.open_dataset('/home/sun/data/process/analysis/AerChem/AerchemMIP_Asia_EOF_land_summertime_8-20_precipitation_hist_SSP370_NTCF.nc')
#print(np.average(f1['pc_hist'].data[:, 0]))
#print(stats.ttest_ind(f1['pc_hist'].data[:, 0], f1['pc_ntcf'].data[:, 0], trim=.2))