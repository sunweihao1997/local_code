'''
2024-3-18
This script is to plot the spatial difference for the different pollutions between SSP370 and SSP370NTCF, for the 2031-2050
'''
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib import cm
from matplotlib.colors import ListedColormap

import sys
sys.path.append("/Users/sunweihao/local_code/module/")
from module_sun import set_cartopy_tick

path0 = '/Users/sunweihao/Downloads/test_emission/so2/'
f1    = xr.open_dataset(path0 + 'emiso2_EC_ssp370.nc')
f2    = xr.open_dataset(path0 + 'emiso2_EC_ssp370ntcf.nc')

lat   = f1.lat.data
lon   = f1.lon.data
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
varname = 'emiso2'
#
year_list   = np.linspace(2031, 2050, 2050 - 2031 + 1)
#emivoc_year = np.zeros((3, len(year_list))) # Here look at the change per year
#
emivoc_ec = np.zeros((2, len(lat), len(lon)))
#emivoc_gfdl = np.zeros((len(year_list)))
#emivoc_cesm = np.zeros((len(year_list)))
#emivoc_mpi2 = np.zeros((len(year_list)))

f1_year = f1.sel(time=f1.time.dt.year.isin(year_list))
f2_year = f2.sel(time=f2.time.dt.year.isin(year_list))
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
emivoc_ec[0,] = np.average(f1_year[varname].data, axis=0)
emivoc_ec[1,] = np.average(f2_year[varname].data, axis=0)
#    emivoc_giss[2, yyyy] = np.nanmean(f6_year[varname].data)
#    emivoc_gfdl[yyyy]    = np.nanmean(f7_year[varname].data)
#    emivoc_cesm[yyyy]    = np.nanmean(f8_year[varname].data)
#    emivoc_mpi2[yyyy]    = np.nanmean(f9_year[varname].data)

#fig, ax1 = plt.subplots()
##ax1.plot(emivoc_year[0] * 31536000, 'k')
##ax1.plot(emivoc_year[1] * 31536000, 'g--')
##ax1.plot(emivoc_year[2] * 31536000, 'r:')
#ax1.plot(year_list, emivoc_ec[0] * 31536000 * (510100000000000/ 1000000000), 'r',    linewidth=2.5,  label='SSP370')
#ax1.plot(year_list, emivoc_ec[1] * 31536000 * (510100000000000/ 1000000000), 'b--',  linewidth=2.5,  label='SSP370lowNTCF')
##x1.plot(emivoc_giss[1] * 31536000 * (510100000000000/ 1000000000), 'g--')
##x1.plot(emivoc_giss[2] * 31536000 * (510100000000000/ 1000000000), 'r:')
##x1.plot(emivoc_gfdl * 31536000 * (510100000000000/ 1000000000), 'b:')
##x1.plot(emivoc_cesm * 31536000 * (510100000000000/ 1000000000), 'navy')
##x1.plot(emivoc_mpi2 * 31536000 * (510100000000000/ 1000000000), 'yellow')
#
#plt.legend()
#plt.savefig('/Users/sunweihao/Downloads/test_emission/emibc_cesm.png')

viridis = cm.get_cmap('Reds', 21)
newcolors = viridis(np.linspace(0, 1, 21))
newcmp = ListedColormap(newcolors)
newcmp.set_under('white')
newcmp.set_over('brown')

diff = emivoc_ec[0] - emivoc_ec[1]
print(diff.shape)

fig, ax = plt.subplots(figsize=(20, 15), subplot_kw={'projection': ccrs.PlateCarree()})

lonmin,lonmax,latmin,latmax  =  45,150,0,50
extent     =  [lonmin,lonmax,latmin,latmax]


# 设置刻度
set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,150,6,dtype=int),yticks=np.linspace(-10,50,7,dtype=int),nx=1,ny=1,labelsize=12.5)

im  =  ax.contourf(lon, lat, 1e11*(emivoc_ec[0]-emivoc_ec[1]), levels=np.linspace(10, 60, 7), cmap=newcmp, alpha=1, extend='both')
#im  =  ax.contourf(lon, lat, 1e11*diff, transform=ccrs.PlateCarree())


# 海岸线
ax.coastlines(resolution='50m',lw=1.65)

ax.set_title(varname, loc='left', fontsize=25)
ax.set_title('1e11 ' + f1[varname].attrs['units'], loc='right', fontsize=25)

plt.colorbar(im,orientation='horizontal')
plt.savefig('/Users/sunweihao/Downloads/test_emission/spatial_emiso2_ec.png')