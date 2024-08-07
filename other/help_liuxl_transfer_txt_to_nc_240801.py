'''
2024-8-1
This script helps Liuxl to transfer txt to nc
'''
import pandas as pd
import xarray as xr
import numpy as np

# 读取文本文件
data = pd.read_csv('/Users/sunweihao/Downloads/new.txt', delim_whitespace=True, header=None)

# 假设你的列没有表头，我们可以给它们命名为 A, B, C, D
#data.columns = ['A', 'B', 'C', 'D']

# 将DataFrame转换为xarray数据数组
data_array = data.to_xarray()

# 显示xarray数据数组
#print(data_array[3])
anom = data_array[3]
#print(type(anom[5]))
print(pd.to_numeric(anom[1:], errors='coerce').shape)

ncfile  =  xr.Dataset(
        {
            "anomaly":        (["time",], pd.to_numeric(anom[1:], errors='coerce')),  
        },
        coords={
            "time": (["time"], np.linspace(1, 893, 893)),
        },
    )

ncfile['anomaly'].attrs["_FillValue"] = 999
ncfile['time'].attrs["_FillValue"]   = 999
ncfile.to_netcdf('/Users/sunweihao/Downloads/new.nc')