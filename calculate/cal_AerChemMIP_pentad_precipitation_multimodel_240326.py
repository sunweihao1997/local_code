'''
2024-3-26
This script is to calculate the pentad-averaged precipitation using the daily data
'''
import xarray as xr
import numpy as np

data_path = '/home/sun/data/process/analysis/AerChem/'
data_file = 'multiple_model_climate_prect_daily.nc'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6',]

hist_pentad  = np.average((len(models_label), 73, 91, 181))
ssp3_pentad  = np.average((len(models_label), 73, 91, 181))
ntcf_pentad  = np.average((len(models_label), 73, 91, 181))

f0           = xr.open_dataset(data_path + data_file)
f0_sel1      = f0.sel(time=f0.time.dt.year.isin(np.linspace(2031, 2050, 20))):

def cal_pentad_average(array):
    pentad_array = np.zeros((73, 91, 181))

    for pp in range(72):
        pentad_array[pp] = np.average(array[pp * 5: pp * 5 + 5], axis=0)

    pentad_array[72] = pentad_array[0]

    return pentad_array
    

mnum = 0
for mm in models_label:
    hist1    = f0_sel1[mm + '_hist'].data # (360, 91, 181)
    ssp31    = f0_sel1[mm + '_ssp'].data
    ntcf1    = f0_sel1[mm + '_sspntcf'].data

    hist_pentad[mnum] = cal_pentad_average(hist1)
    ssp3_pentad[mnum] = cal_pentad_average(ssp31)
    ntcf_pentad[mnum] = cal_pentad_average(ntcf1)

    mnum += 1

# ------------ Write to a ncfile  ------------------
ncfile  =  xr.Dataset(
        {
            "hist_pentad_modelmean":     (["time", "lat", "lon"], np.nanmean(hist_pentad, axis=0)),     
            "ssp3_pentad_modelmean":     (["time", "lat", "lon"], np.nanmean(ssp3_pentad, axis=0)),     
            "ntcf_pentad_modelmean":     (["time", "lat", "lon"], np.nanmean(ntcf_pentad, axis=0)),          
        },
        coords={
            "time": (["time"], np.linspace(1, 73, 73))
            "lat":  (["lat"],  f0.lat.data),
            "lon":  (["lon"],  f0.lon.data),
        },
        )

ncfile.attrs['description'] = 'Created on 2024-3-27. This file used multiple_model_climate_prect_daily.nc to calculate its pentad average.'
#ncfile.attrs['Note']        = 'This pentad averaged precipitation does not includes NorESM'

ncfile.to_netcdf(data_path + 'multiple_model_climate_prect_pentad.nc')

f_p  =  xr.open_dataset(data_path + 'multiple_model_climate_prect_pentad.nc')


# ------------ paint from chatGPT ------------------
import plotly.graph_objects as go

# 月份
months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

# 创建柱状图
bar = go.Bar(x=months, y=precipitation_this_year, name='今年降水量')

# 创建曲线图
line = go.Scatter(x=months, y=precipitation_last_year, mode='lines+markers', name='去年降水量')

# 将柱状图和曲线图组合在一起
fig = go.Figure(data=[bar, line])

# 更新布局
fig.update_layout(title='1-12月降水量对比图', xaxis_title='月份', yaxis_title='降水量 (毫米)')

# 显示图表
fig.show()