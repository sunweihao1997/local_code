'''
2024-5-31
This script is to test the vertical integral in python, for the cdnc variable
'''
import xarray as xr
import numpy as np

cdnc_file = xr.open_dataset("/home/sun/data/other_data/cdnc_AERmon_MRI-ESM2-0_ssp370_r1i1p1f1.nc")

#lev       = cdnc_file.plev.data

print(cdnc_file)