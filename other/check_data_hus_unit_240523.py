import xarray as xr
import numpy as np

f0 = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_hus_cat/hus_Amon_MRI-ESM2-0_ssp370-lowNTCF_r1i1p1f1.nc")

hus = f0['hus'].data
print(np.nanmean(hus))