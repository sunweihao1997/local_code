'''
2023-11-23
This script is to plot the time-series of the Indian rainfall for the 1900 to 2000 period
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# ============== File location information =======================

file_path = '/mnt/e/data/precipitation/processed/'
file_name = 'EUI_GPCC_CESM_CESM2_Indian_JJAS_rainfall_time_series_1900_2000_with_filtered.nc'

f0        = xr.open_dataset(file_path + file_name)

# ============== calculation =====================================

# 1. Anomaly

gpcc      = f0['gpcc'].data - np.average(f0['gpcc'].data)

# ============== paint ==========================================

fig, ax = plt.subplots(figsize=(12,18))

ax.plot(np.linspace(1891, 1891+128, 129), gpcc, color='black')

#ax.plot([1900, 2000], [0, 0], 'k--')
#
#ax.set_ylim((-0.5, 0.5))
#ax.set_xlim((1905, 1990))
#
#ax.set_xticks(np.linspace(1905, 2000, 20))
#ax.set_yticks(np.linspace(-0.5, 0.5, 11))
#
ax.grid(True)

plt.savefig('test.png')
