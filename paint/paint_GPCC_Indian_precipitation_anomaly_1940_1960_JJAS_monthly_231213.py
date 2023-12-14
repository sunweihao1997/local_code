'''
2023-12-13
This script is to plot the monthly anomaly for the period 1940 to 1960 over the Indian continent
'''
import xarray as xr
import numpy as np
import sys
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#module_path = '/Users/sunweihao/local_code/module'
module_path = '/home/sun/local_code/module'
sys.path.append(module_path)

from module_sun import set_cartopy_tick

# ----------------- 1. Dfine the period for calculating the anomaly value -------------------
period1 = 1940 ; period2 = 1960

# ------------------------------------------------------------------------------------------

# ----------------- 2. File location --------------------------------------------------------

file_path = '/mnt/e/data/precipitation/GPCC/'
file_name = 'precip.mon.total.1x1.v2020.nc'
file0     = xr.open_dataset(file_path + file_name)

lat       = file0.lat.data
lon       = file0.lon.data
time      = file0.time.data

lonmin,lonmax,latmin,latmax  =  50,110,-10,40
extent     =  [lonmin,lonmax,latmin,latmax]

#print(file0) # Start from 1891 and has 129 years

# ------------------------------------------------------------------------------------------

# ----------------- 3. Calculation ---------------------------------------------------------

# Because this script is to see the monthly anomaly among the JJAS, so here I need to claim 4 arrays

#Jun_anomaly = np.zeros((int(len(time)/12), int(len(lat)), int(len(lon)))) 
#Jun_anomaly = np.zeros((int(len(lat)), int(len(lon)))) 
#Jul_anomaly = Jun_anomaly.copy()
#Aug_anomaly = Jun_anomaly.copy()
#Sep_anomaly = Jun_anomaly.copy()

JJAS_mon_anomaly = np.zeros((4, int(len(lat)), int(len(lon)))) # First dimension is J-J-A-S

for mm in range(6, 10, 1):
    # 1. Firstly, select the data at that month
    file_single_m = file0.sel(time=file0.time.dt.month.isin([mm]))

    #print(len(file_single_m.time.data))

    # 2. Secondly, select the data at the selected period 1940 to 1960
    # That is, file_period_m is the subset of the file_single_m

    file_period_m = file_single_m.sel(time=file_single_m.time.dt.year.isin(np.linspace(1941, 1960, 20)))

    #print(len(file_period_m.time.data))

    # 3. Thirdly, calculate the anomaly for every year and every frid point

    for yy in range(int(len(lat))):
        for xx in range(int(len(lon))):
            JJAS_mon_anomaly[mm - 6, yy, xx] = np.nanmean(file_period_m['precip'].data[:, yy, xx], axis=0) - np.nanmean(file_single_m['precip'].data[:, yy, xx], axis=0)

#print(np.nanmean(file_single_m.precip.data))
JJAS_mon_anomaly /= 31 # Because the original data is monthly total
# ==================== Up to now, the calculation of each month anomaly of the given period 1940-1960 has been completed ==================================

# ------------------- 4. Painting -----------------------------------------------------------

# 设置画布
proj    =  ccrs.PlateCarree()
fig1    =  plt.figure(figsize=(20,17))
spec1   =  fig1.add_gridspec(nrows=2,ncols=2)

j  =  0

title_left = ['June', 'July', 'August', 'September']

for col in range(2):
    for row in range(2):
        ax = fig1.add_subplot(spec1[row,col],projection=proj)

        # 设置刻度
        set_cartopy_tick(ax=ax,extent=extent,xticks=np.linspace(50,110,4,dtype=int),yticks=np.linspace(-10,40,6,dtype=int),nx=1,ny=1,labelsize=12.5)

        # 添加赤道线
        ax.plot([0,150],[0,0],'k--')

        im  =  ax.contourf(lon, lat, JJAS_mon_anomaly[j], np.linspace(-2, 2, 21),cmap='coolwarm_r', alpha=1, extend='both')

        ax.set_title(title_left[j], loc='left', fontsize=15)
        ax.set_title('1940-1960 anomaly', loc='right', fontsize=15)

        # 海岸线
        ax.coastlines(resolution='110m',lw=2)

        j += 1

# 加colorbar
fig1.subplots_adjust(top=0.8) 
cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
cb  =  fig1.colorbar(im, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
cb.ax.tick_params(labelsize=20)

plt.savefig('GPCC_prect_anomaly_J_J_A_S_monthly_1940_1960.pdf', dpi=600)
    
