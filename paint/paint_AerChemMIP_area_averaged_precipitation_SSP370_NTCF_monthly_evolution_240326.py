'''
2024-3-26
This script is to calculate and visualize the annual evolution of the precipitation in the five different areas
The areas are: Indian, Indochina, SCS, TP, East-Asia

The criterion of the selection can be found in paint_AerChemMIP_difference_prect_JJAS_SSP370_NTCF_240227.py
'''
import xarray as xr
import numpy as np

# === Read file ===
data_path = '/data/AerChemMIP/LLNL_download/model_average/'
diff_f    = 'CMIP6_model_historical_SSP370_SSP370NTCF_monthly_precipitation_2015-2050_new.nc'

f0        = xr.open_dataset(data_path + diff_f)

year_list = np.linspace(2031, 2050, 20)
f0        = f0.sel(time=f0.time.dt.year.isin(year_list))


# === calculate the area-averaged precipitation in the different areas ===
f0_ia     = f0.sel(lon=slice(70, 87.5),    lat=slice(17, 27))
f0_ic     = f0.sel(lon=slice(90, 118),     lat=slice(10, 26.5))
f0_sc     = f0.sel(lon=slice(110, 120),    lat=slice(10, 20))
f0_tp     = f0.sel(lon=slice(80, 105),     lat=slice(27.5, 37.5))
f0_se     = f0.sel(lon=slice(110, 122.5),  lat=slice(22.5, 33))


def cal_20year_climate(f1, var):
    # Claim the average array for each month
    avg_mon = np.zeros((12))

    #print(f1)
    mnum = 0
    for mm in np.linspace(1, 12, 12):
        f1_single_m = f1.sel(time=f1.time.dt.month.isin([mm]))

        #print(np.max(f1_single_m[var].data))

        #print(f1_single_m)

        if len(f1_single_m.time.data) != 20:
            print('Error the time length is not 20 year')

        avg_mon[mnum] = np.average(np.average(np.average(f1_single_m[var].data, axis=0), axis=0), axis=0)

        mnum += 1

    return avg_mon

ia_ssp_ntcf = [cal_20year_climate(f0_ia, 'pr_ssp'), cal_20year_climate(f0_ia, 'pr_ntcf')]
ic_ssp_ntcf = [cal_20year_climate(f0_ic, 'pr_ssp'), cal_20year_climate(f0_ic, 'pr_ntcf')]
sc_ssp_ntcf = [cal_20year_climate(f0_sc, 'pr_ssp'), cal_20year_climate(f0_sc, 'pr_ntcf')]
tp_ssp_ntcf = [cal_20year_climate(f0_tp, 'pr_ssp'), cal_20year_climate(f0_tp, 'pr_ntcf')]
se_ssp_ntcf = [cal_20year_climate(f0_se, 'pr_ssp'), cal_20year_climate(f0_se, 'pr_ntcf')]

#print(ia_ssp_ntcf[0].shape)
# Start paint the bar
import matplotlib.pyplot as plt

group_labels = ['SSP370', 'SSP370lowNTCF']
month        = np.linspace(1, 12, 12, dtype=int)

import plotly.graph_objects as go

# ---Indian---
fig = go.Figure(data=[
    go.Bar(name='SSP370lowNTCF - SSP370', x=month, y=(ia_ssp_ntcf[1] - ia_ssp_ntcf[0]) * 30,),
])

# Change the bar mode
fig.update_layout(barmode='group',
                  title=dict(text="Indian", font=dict(size=20), automargin=True, yref='paper', x=0.12)  
                )

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

fig.write_image("/data/paint/diff_hist_ia.png")

del fig

# ---Indochina---
fig = go.Figure(data=[
    go.Bar(name='SSP370lowNTCF - SSP370', x=month, y=(ic_ssp_ntcf[1] - ic_ssp_ntcf[0]) * 30),
])

# Change the bar mode
fig.update_layout(barmode='group',
                  title=dict(text="Indochina", font=dict(size=20), automargin=True, yref='paper', x=0.12)  
                )

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

fig.write_image("/data/paint/diff_hist_ic.png")

del fig

# ---SCS---
fig = go.Figure(data=[
    go.Bar(name='SSP370lowNTCF - SSP370', x=month, y=(sc_ssp_ntcf[1] - sc_ssp_ntcf[0]) * 30),
])

# Change the bar mode
fig.update_layout(barmode='group',
                  title=dict(text="South China Sea", font=dict(size=20), automargin=True, yref='paper', x=0.12)  
                )

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

fig.write_image("/data/paint/diff_hist_scs.png")

del fig

# ---TP---
fig = go.Figure(data=[
    go.Bar(name='SSP370lowNTCF - SSP370', x=month, y=(tp_ssp_ntcf[1] - tp_ssp_ntcf[0]) * 30),
])

# Change the bar mode
fig.update_layout(barmode='group',
                  title=dict(text="Qinghai-Tibet Plateau", font=dict(size=20), automargin=True, yref='paper', x=0.12)  
                )

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

fig.write_image("/data/paint/diff_hist_tp.png")

del fig

# ---EA---
#fig = go.Figure(data=[
#    go.Bar(name=group_labels[0], x=month, y=se_ssp_ntcf[0] * 30),
#    go.Bar(name=group_labels[1], x=month, y=se_ssp_ntcf[1] * 30), 
#])

fig = go.Figure(data=[
    go.Bar(name='SSP370lowNTCF - SSP370', x=month, y=(se_ssp_ntcf[1] - se_ssp_ntcf[0]) * 30),
])

# Change the bar mode
fig.update_layout(barmode='group',
                  title=dict(text="Southeastern China", font=dict(size=20), automargin=True, yref='paper', x=0.12)  
                )

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

fig.write_image("/data/paint/diff_hist_southeast_asia.png")

del fig