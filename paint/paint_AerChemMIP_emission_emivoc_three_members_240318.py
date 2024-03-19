'''
2024-3-18
This script is to check: for the same model, is it the same for the time-series of emission? The variable used here is emivoc
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

path0 = '/Users/sunweihao/Downloads/test_emission/emibc/'
f1    = xr.open_dataset(path0 + 'emibc_AERmon_CESM2-WACCM_ssp370_r1i1p1f1_gn_201501-206412.nc')
f2    = xr.open_dataset(path0 + 'emibc_AERmon_CESM2-WACCM_ssp370-lowNTCF_r1i2p1f1_gn_201501-205512.nc')
#f3    = xr.open_dataset(path0 + 'emivoc_EC_r4.nc')

# --- GISS ---
#f4    = xr.open_dataset(path0 + 'emiso2_UKESM_r1.nc')
#f5    = xr.open_dataset(path0 + 'emiso2_UKESM_r2.nc')
#f6    = xr.open_dataset(path0 + 'emiso2_UKESM_r3.nc')
#
## --- GFDL ---
#f7    = xr.open_dataset(path0 + 'emiso2_AERmon_GFDL-ESM4_ssp370-lowNTCF_r1i1p1f1_gr1_201501-205912.nc')
#
## --- CESM2 ---
#f8    = xr.open_dataset(path0 + 'emiso2_AERmon_CESM2-WACCM_ssp370-lowNTCF_r1i2p1f1_gn_201501-205512.nc')
#
## --- MPI ---
#f9    = xr.open_dataset(path0 + 'emiso2_MPI_r2.nc')
#
varname = 'emibc'
#
year_list   = np.linspace(2015, 2050, 2050 - 2015 + 1)
#emivoc_year = np.zeros((3, len(year_list))) # Here look at the change per year
#
emivoc_ec = np.zeros((2, len(year_list)))
#emivoc_gfdl = np.zeros((len(year_list)))
#emivoc_cesm = np.zeros((len(year_list)))
#emivoc_mpi2 = np.zeros((len(year_list)))

for yyyy in range(len(year_list)):
    f1_year = f1.sel(time=f1.time.dt.year.isin([year_list[yyyy]]))
    f2_year = f2.sel(time=f2.time.dt.year.isin([year_list[yyyy]]))
#    f3_year = f3.sel(time=f3.time.dt.year.isin([year_list[yyyy]]))
#    f4_year = f4.sel(time=f4.time.dt.year.isin([year_list[yyyy]]))
#    f5_year = f5.sel(time=f5.time.dt.year.isin([year_list[yyyy]]))
#    f6_year = f6.sel(time=f6.time.dt.year.isin([year_list[yyyy]]))
#    f7_year = f7.sel(time=f7.time.dt.year.isin([year_list[yyyy]]))
#    f8_year = f8.sel(time=f8.time.dt.year.isin([year_list[yyyy]]))
#    f9_year = f9.sel(time=f9.time.dt.year.isin([year_list[yyyy]]))

    #print(f1_year)

#    emivoc_year[0, yyyy] = np.nanmean(f1_year[varname].data)
#    emivoc_year[1, yyyy] = np.nanmean(f2_year[varname].data)
#    emivoc_year[2, yyyy] = np.nanmean(f3_year[varname].data)
    emivoc_ec[0, yyyy] = np.nanmean(f1_year[varname].data)
    emivoc_ec[1, yyyy] = np.nanmean(f2_year[varname].data)
#    emivoc_giss[2, yyyy] = np.nanmean(f6_year[varname].data)
#    emivoc_gfdl[yyyy]    = np.nanmean(f7_year[varname].data)
#    emivoc_cesm[yyyy]    = np.nanmean(f8_year[varname].data)
#    emivoc_mpi2[yyyy]    = np.nanmean(f9_year[varname].data)

fig, ax1 = plt.subplots()
#ax1.plot(emivoc_year[0] * 31536000, 'k')
#ax1.plot(emivoc_year[1] * 31536000, 'g--')
#ax1.plot(emivoc_year[2] * 31536000, 'r:')
ax1.plot(year_list, emivoc_ec[0] * 31536000 * (510100000000000/ 1000000000), 'r',    linewidth=2.5,  label='SSP370')
ax1.plot(year_list, emivoc_ec[1] * 31536000 * (510100000000000/ 1000000000), 'b--',  linewidth=2.5,  label='SSP370lowNTCF')
#x1.plot(emivoc_giss[1] * 31536000 * (510100000000000/ 1000000000), 'g--')
#x1.plot(emivoc_giss[2] * 31536000 * (510100000000000/ 1000000000), 'r:')
#x1.plot(emivoc_gfdl * 31536000 * (510100000000000/ 1000000000), 'b:')
#x1.plot(emivoc_cesm * 31536000 * (510100000000000/ 1000000000), 'navy')
#x1.plot(emivoc_mpi2 * 31536000 * (510100000000000/ 1000000000), 'yellow')

plt.legend()
plt.savefig('/Users/sunweihao/Downloads/test_emission/emibc_cesm.png')