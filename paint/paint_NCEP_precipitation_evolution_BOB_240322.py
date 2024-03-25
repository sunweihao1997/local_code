'''
2024-3-22
This script is to see the annual evolution of the precipitation over BOB in NCEP
'''
import xarray as xr
import numpy as np

data_obs = xr.open_dataset('/home/sun/data/process/analysis/AerChem/observation/NCEP_precipitation_climate_annual_evolution_1980_2014.nc').sel(lat=slice(5, 15), lon=slice(90, 100))

year_value = np.average(np.average(data_obs.precip.data, axis=1), axis=1)

import matplotlib.pyplot as plt

plt.plot(year_value)

plt.savefig('NCEP_BOB.png')