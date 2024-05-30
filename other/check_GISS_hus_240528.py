import xarray as xr
import numpy as np

f = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_hus_cat/hus_Amon_MIROC6_ssp370-lowNTCF_r1i1p1f1.nc")

print(np.nanmean(f['hus'].data))