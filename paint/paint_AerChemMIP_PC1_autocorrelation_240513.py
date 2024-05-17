'''
2024-5-13
This script is to calculate and plot the autocorrelation for the PC1
'''
import xarray as xr
import numpy as np
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt

# =========== File Information ===============
# 1. Read the PC1 file 
data_path   =  '/home/sun/data/process/analysis/AerChem/'
high_EOF    =  xr.open_dataset(data_path + 'AerchemMIP_Asia_EOF_land_summertime_8-20_precipitation_hist_SSP370_NTCF.nc')
low_EOF     =  xr.open_dataset(data_path + 'AerchemMIP_Asia_EOF_land_summertime_20-70_precipitation_hist_SSP370_NTCF.nc')

high_pc_hist     =  high_EOF['pc_hist'].data[:, 0]
low_pc_hist      =  low_EOF['pc_hist'].data[:, 0]

high_pc_ssp      =  high_EOF['pc_ssp3'].data[:, 0]
low_pc_ssp       =  low_EOF['pc_ssp3'].data[:, 0]

high_pc_ntcf     =  high_EOF['pc_ntcf'].data[:, 0]
low_pc_ntcf      =  low_EOF['pc_ntcf'].data[:, 0]

# ==============================================

# ========== calculate =========
lag = 60
auto_correlations = acf(high_pc_hist, nlags=lag, fft=True)

print(auto_correlations.shape)
#print("Auto-correlations:", auto_correlations)
plot_acf(high_pc_hist, lags=lag)
plt.savefig('/home/sun/paint/AerMIP/high_PC1_autocorrelation.pdf')