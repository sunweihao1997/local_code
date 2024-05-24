'''
2024-5-22
This script checks whether the vertical level is the same among the models
'''
import xarray as xr

f0 = xr.open_dataset("/home/sun/data/AerChemMIP/mon_hus_samegrid/hus_Amon_EC-Earth3-AerChem_ssp370-lowNTCF_r1i1p1f1.nc")

f1 = xr.open_dataset("/home/sun/data/AerChemMIP/mon_hus_samegrid/hus_Amon_UKESM1-0-LL_ssp370-lowNTCF_r3i1p1f2.nc")

if (f0.plev.data == f1.plev.data).all():
    print("yes")

print(f0.plev.data)
print(f1.plev.data)