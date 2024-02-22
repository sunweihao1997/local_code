'''
2024-2-5
This script is to plot the correlation between the May precipitation and Nino34 index
'''
import xarray as xr
import numpy as np
import sys
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

module_path = '/home/sun/local_code/module'
sys.path.append(module_path)

from module_sun import set_cartopy_tick

data_path = '/home/sun/data/process/analysis/'
f0        = xr.open_dataset(data_path + 'CESM2_pacemaker_correlation_May_precipitation_Nino34.nc')

# ==== Painting ====
lonmin,lonmax,latmin,latmax  =  30,130,-10,40
extent     =  [lonmin,lonmax,latmin,latmax]

# 设置画布
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# 设置刻度
set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(30,130,11,dtype=int),yticks=np.linspace(-10,40,6,dtype=int),nx=1,ny=1,labelsize=9)

# 添加赤道线
ax.plot([0,150],[0,0],'k--')

im   =  ax.contourf(f0.lon.data, f0.lat.data, f0['corre'].data, np.linspace(-1, 1, 11), cmap='coolwarm', alpha=1, extend='both')

dot  =  ax.contourf(f0['lon'].data, f0['lat'].data, f0['p_value'], levels=[0., 0.05], colors='none', hatches=['...'])

ax.set_title('Nino34 & Precip', loc='left', fontsize=15)
ax.set_title('CESM2', loc='right', fontsize=15)

# 海岸线
ax.coastlines(resolution='110m',lw=2)

# 加colorbar
#fig.subplots_adjust(top=0.8) 

cb  =  fig.colorbar(im, ax=ax, orientation='horizontal')
cb.ax.tick_params(labelsize=15)

plt.savefig('/home/sun/paint/monsoon_onset/CESM2_pacemaker_May_precip_Nino34.pdf', dpi=600)