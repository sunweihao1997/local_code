'''
2023-11-23
This script is to calculate Indian rainfall time series for the given period (1900 - 2000)
'''
import xarray as xr
import numpy as np
import sys
import scipy

module_path = '/home/sun/local_code/module'
sys.path.append(module_path)
from module_sun import mask_use_shapefile

# ==================== Files information ==========================
class c1:
    '''
        This class save information about file in the disk
    '''

    # ================ GPCC =====================
    gpcc_path = '/mnt/e/data/precipitation/GPCC/'
    gpcc_name = 'JJAS_GPCC_mean_update.nc'

    # ================ CESM =====================
    cesm_path = '/mnt/e/data/precipitation/CESM/ensemble_JJAS/'
    cesm_name = 'CESM_BTAL_esemble_JJAS_precipitation.nc'  # Need to be averaged

    # ================ CESM2 ====================
    cesm2_path = '/mnt/e/data/precipitation/processed/CESM2/'
    cesm2_name = 'CESM2_CMIP6_precipitation_ensemble_mean_JJAS.nc'

    # ================ shape file ==============
    shp_path = '/mnt/e/data/shape/indian/'
    shp_name = 'IND_adm0.shp'

# ==================================================================

# ------- 1. Read the file --------

gpcc = xr.open_dataset(c1.gpcc_path + c1.gpcc_name)


# ------- 2. Send to clipped using shape file -----------

#gpcc_indian = mask_use_shapefile(gpcc, "lat", "lon", c1.shp_path + c1.shp_name)
gpcc_indian = gpcc.sel(lat=slice(34, 5), lon=slice(65, 100))


#print(gpcc_indian)
#print(cesm_indian)
# ------- 3. Select period ----------

#gpcc_indian = gpcc_indian.sel(time=slice(1900, 2000))


#print(gpcc_indian)
#print(cesm_indian)

# ------- 4. Calculate time-series of whole precipitation ------
gpcc_indian_p  = np.zeros((129,))


for yyyy in range(129):
    gpcc_indian_p[yyyy] = np.nanmean(gpcc_indian['JJAS_prect'].data[yyyy])


# ------- 5. filter ---------------------------------------------
N = 5
period = 20
Wn = 2 * (1 / period) / 1


# 5.1 butter construction
b, a = scipy.signal.butter(N, Wn, 'lowpass')

# 5.2 filter
gpcc_indian_p_filter = scipy.signal.filtfilt(b, a, gpcc_indian_p, axis=0)


# ------ 6. plot -----
#import matplotlib.pyplot as plt
#
#plt.plot(gpcc_indian_p_filter)
#
#plt.savefig('test.png')

# ------ 7. Save to the ncfile ----
ncfile  =  xr.Dataset(
{
    "gpcc": (gpcc_indian_p_filter),

},
)

out_path = '/mnt/e/data/precipitation/processed/'

ncfile.to_netcdf(out_path + "EUI_GPCC_CESM_CESM2_Indian_JJAS_rainfall_time_series_1900_2000_with_filtered.nc")