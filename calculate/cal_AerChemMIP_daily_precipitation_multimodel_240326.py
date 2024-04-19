'''
2024-3-26
This script is to calculate the pentad-averaged precipitation using the daily data
'''
import xarray as xr
import numpy as np

data_path = '/home/sun/data/process/analysis/AerChem/'
data_file = 'multiple_model_climate_prect_daily_new.nc'

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6',]

hist_pentad  = np.zeros((len(models_label), 360, 91, 181))
ssp3_pentad  = np.zeros((len(models_label), 360, 91, 181))
ntcf_pentad  = np.zeros((len(models_label), 360, 91, 181))

f0           = xr.open_dataset(data_path + data_file)
f0_sel1      = f0



def cal_pentad_climate(f1, var):
    # Claim the average array for each month
    #avg_mon = np.zeros((73))

    #print(f1)
    mnum = 0
    
    avg_pentad = np.average(np.average(f1[var].data, axis=1), axis=1)

    print(f'length of array is {len(avg_pentad)}')

    return avg_pentad

def cal_pentad_climate_weighted(f1, var, lats, lons):

    avg_pentad = np.zeros((73))

    for pp in range(73):
        p_value = f1[var].data[pp]

        weights = np.cos(np.radians(lats))

        weights_matrix = np.tile(weights[:, np.newaxis], (1, p_value.shape[1]))

        weighted_sum = np.sum(p_value * weights_matrix)

        total_weight = np.sum(weights_matrix)

        avg_pentad[pp] = weighted_sum / total_weight

    return avg_pentad
#
mnum = 0
for mm in models_label:
    hist1    = f0_sel1[mm + '_hist'].data # (360, 91, 181)
    ssp31    = f0_sel1[mm + '_ssp'].data
    ntcf1    = f0_sel1[mm + '_sspntcf'].data

    print(hist1)
    #print(hist_pentad.shape)
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
            "time": (["time"], np.linspace(1, 73, 73)),
            "lat":  (["lat"],  f0.lat.data),
            "lon":  (["lon"],  f0.lon.data),
        },
        )

ncfile.attrs['description'] = 'Created on 2024-3-27. This file used multiple_model_climate_prect_daily.nc to calculate its pentad average.'
#ncfile.attrs['Note']        = 'This pentad averaged precipitation does not includes NorESM'

ncfile.to_netcdf(data_path + 'multiple_model_climate_prect_pentad.nc')

f_p  =  xr.open_dataset(data_path + 'multiple_model_climate_prect_pentad.nc')

## ------------ Selection for each area -------------
f0_ia     = f_p.sel(lon=slice(70, 87.5),    lat=slice(17, 27))
f0_ic     = f_p.sel(lon=slice(90, 118),     lat=slice(10, 26.5))
f0_sc     = f_p.sel(lon=slice(110, 120),    lat=slice(10, 20))
f0_tp     = f_p.sel(lon=slice(80, 105),     lat=slice(27.5, 37.5))
f0_se     = f_p.sel(lon=slice(110, 122.5),  lat=slice(22.5, 33))


#ia_precip = [cal_pentad_climate_weighted(f0_ia, 'ssp3_pentad_modelmean', f0_ia.lat.data, f0_ia.lon.data), cal_pentad_climate_weighted(f0_ia, 'ntcf_pentad_modelmean', f0_ia.lat.data, f0_ia.lon.data)]
#ic_precip = [cal_pentad_climate_weighted(f0_ic, 'ssp3_pentad_modelmean', f0_ic.lat.data, f0_ic.lon.data), cal_pentad_climate_weighted(f0_ic, 'ntcf_pentad_modelmean', f0_ic.lat.data, f0_ic.lon.data)]
#sc_precip = [cal_pentad_climate_weighted(f0_sc, 'ssp3_pentad_modelmean', f0_sc.lat.data, f0_sc.lon.data), cal_pentad_climate_weighted(f0_sc, 'ntcf_pentad_modelmean', f0_sc.lat.data, f0_sc.lon.data)]
#tp_precip = [cal_pentad_climate_weighted(f0_tp, 'ssp3_pentad_modelmean', f0_tp.lat.data, f0_tp.lon.data), cal_pentad_climate_weighted(f0_tp, 'ntcf_pentad_modelmean', f0_tp.lat.data, f0_tp.lon.data)]
#se_precip = [cal_pentad_climate_weighted(f0_se, 'ssp3_pentad_modelmean', f0_se.lat.data, f0_se.lon.data), cal_pentad_climate_weighted(f0_se, 'ntcf_pentad_modelmean', f0_se.lat.data, f0_se.lon.data)]

ia_precip = [cal_pentad_climate(f0_ia, 'ssp3_pentad_modelmean',), cal_pentad_climate(f0_ia, 'ntcf_pentad_modelmean',)]
ic_precip = [cal_pentad_climate(f0_ic, 'ssp3_pentad_modelmean',), cal_pentad_climate(f0_ic, 'ntcf_pentad_modelmean',)]
sc_precip = [cal_pentad_climate(f0_sc, 'ssp3_pentad_modelmean',), cal_pentad_climate(f0_sc, 'ntcf_pentad_modelmean',)]
tp_precip = [cal_pentad_climate(f0_tp, 'ssp3_pentad_modelmean',), cal_pentad_climate(f0_tp, 'ntcf_pentad_modelmean',)]
se_precip = [cal_pentad_climate(f0_se, 'ssp3_pentad_modelmean',), cal_pentad_climate(f0_se, 'ntcf_pentad_modelmean',)]
#print(ia_precip[0])

# ------------ paint from chatGPT ------------------
import plotly.graph_objects as go

# 月份
#months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

# ----------- Indian --------------
# 创建柱状图
bar1 = go.Bar(x=np.linspace(1, 73, 73), y=ia_precip[0] * 86400, name='SSP370')
bar2 = go.Bar(x=np.linspace(1, 73, 73), y=ia_precip[1] * 86400, name='SSP370lowNTCF')

# 创建曲线图
line1 = go.Scatter(x=np.linspace(1, 73, 73), y=ia_precip[0] * 86400, mode='lines', line=dict(color='blue'), name='SSP370')
line2 = go.Scatter(x=np.linspace(1, 73, 73), y=ia_precip[1] * 86400, mode='lines', line=dict(color='red'),  name='SSP370lowNTCF')

# 将柱状图和曲线图组合在一起
fig = go.Figure(data=[bar1, bar2, line1, line2])

# 更新布局
fig.update_layout(title='Indian', xaxis_title='pentad', yaxis_title='mm/day')

# 显示图表
fig.write_image("/home/sun/paint/AerMIP/pentad_evolution_indian.png")

del fig

# ----------- Indochina --------------
# 创建柱状图
bar1 = go.Bar(x=np.linspace(1, 73, 73), y=ic_precip[0] * 86400, name='SSP370')
bar2 = go.Bar(x=np.linspace(1, 73, 73), y=ic_precip[1] * 86400, name='SSP370lowNTCF')

# 创建曲线图
line1 = go.Scatter(x=np.linspace(1, 73, 73), y=ic_precip[0] * 86400, mode='lines', line=dict(color='blue'), name='SSP370')
line2 = go.Scatter(x=np.linspace(1, 73, 73), y=ic_precip[1] * 86400, mode='lines', line=dict(color='red'),  name='SSP370lowNTCF')

# 将柱状图和曲线图组合在一起
fig = go.Figure(data=[bar1, bar2, line1, line2])

# 更新布局
fig.update_layout(title='Indochina', xaxis_title='pentad', yaxis_title='mm/day')

# 显示图表
fig.write_image("/home/sun/paint/AerMIP/pentad_evolution_indochina.png")

# ----------- SCS --------------
# 创建柱状图
bar1 = go.Bar(x=np.linspace(1, 73, 73), y=sc_precip[0] * 86400, name='SSP370')
bar2 = go.Bar(x=np.linspace(1, 73, 73), y=sc_precip[1] * 86400, name='SSP370lowNTCF')

# 创建曲线图
line1 = go.Scatter(x=np.linspace(1, 73, 73), y=sc_precip[0] * 86400, mode='lines', line=dict(color='blue'), name='SSP370')
line2 = go.Scatter(x=np.linspace(1, 73, 73), y=sc_precip[1] * 86400, mode='lines', line=dict(color='red'),  name='SSP370lowNTCF')

# 将柱状图和曲线图组合在一起
fig = go.Figure(data=[bar1, bar2, line1, line2])

# 更新布局
fig.update_layout(title='South China Sea', xaxis_title='pentad', yaxis_title='mm/day')

# 显示图表
fig.write_image("/home/sun/paint/AerMIP/pentad_evolution_scs.png")

# ----------- tp --------------
# 创建柱状图
bar1 = go.Bar(x=np.linspace(1, 73, 73), y=tp_precip[0] * 86400, name='SSP370')
bar2 = go.Bar(x=np.linspace(1, 73, 73), y=tp_precip[1] * 86400, name='SSP370lowNTCF')

# 创建曲线图
line1 = go.Scatter(x=np.linspace(1, 73, 73), y=tp_precip[0] * 86400, mode='lines', line=dict(color='blue'), name='SSP370')
line2 = go.Scatter(x=np.linspace(1, 73, 73), y=tp_precip[1] * 86400, mode='lines', line=dict(color='red'),  name='SSP370lowNTCF')

# 将柱状图和曲线图组合在一起
fig = go.Figure(data=[bar1, bar2, line1, line2])

# 更新布局
fig.update_layout(title='Qinghai-Tibet Plateau', xaxis_title='pentad', yaxis_title='mm/day')

# 显示图表
fig.write_image("/home/sun/paint/AerMIP/pentad_evolution_tp.png")

# ----------- EA --------------
# 创建柱状图
bar1 = go.Bar(x=np.linspace(1, 73, 73), y=se_precip[0] * 86400, name='SSP370')
bar2 = go.Bar(x=np.linspace(1, 73, 73), y=se_precip[1] * 86400, name='SSP370lowNTCF')

# 创建曲线图
line1 = go.Scatter(x=np.linspace(1, 73, 73), y=se_precip[0] * 86400, mode='lines', line=dict(color='blue'), name='SSP370')
line2 = go.Scatter(x=np.linspace(1, 73, 73), y=se_precip[1] * 86400, mode='lines', line=dict(color='red'),  name='SSP370lowNTCF')

# 将柱状图和曲线图组合在一起
fig = go.Figure(data=[bar1, bar2, line1, line2])

# 更新布局
fig.update_layout(title='Southeastern China', xaxis_title='pentad', yaxis_title='mm/day')

# 显示图表
fig.write_image("/home/sun/paint/AerMIP/pentad_evolution_se.png")

del fig