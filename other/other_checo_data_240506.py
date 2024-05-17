import xarray as xr
import numpy as np

fvas = xr.open_dataset("/home/sun/data/process/analysis/AerChem/vas_MJJAS_multiple_model_result.nc")
frlut = xr.open_dataset("/home/sun/data/process/analysis/AerChem/rlut_MJJAS_multiple_model_result.nc")

print(np.sum(np.isnan(frlut['hist_model'].data)))