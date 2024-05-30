import xarray as xr

f = xr.open_dataset("/home/sun/data/AerChemMIP/process/200_div_ncl/div_Amon_GISS-E2-1-G_ssp370-lowNTCF_r2i1p1f2.nc")

print(f.sf.data)