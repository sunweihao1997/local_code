'''
This script is to see the value of cdnc
'''
import xarray as xr

f0 = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_cdnc/cdnc_AERmon_MRI-ESM2-0_ssp370_r5i1p1f1_gn_209501-210012.nc")

print(f0.cdnc.data[5, :, 30, 50])