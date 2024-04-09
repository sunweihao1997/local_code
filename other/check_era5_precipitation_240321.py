'''
This file is to see how era5 precipitation works
'''

import xarray as xr
import numpy as np
f0 = xr.open_dataset('/Users/sunweihao/test_ERA5/download_4hr.nc')

#print(f0.tp)


var = f0.tp.data
#
#print(var[1:, 360, 720] * 1000)
##print(np.sum(var[1, 360, 720] * 1000))
##print(np.sum(var[2, 360, 720] * 1000))
##print(np.sum(var[3, 360, 720] * 1000))
#
f1 = xr.open_dataset('/Users/sunweihao/test_ERA5/download_1hr.nc')
var1 = f1.tp.data
#print('===============================================================')
##print(var1[1:, 360, 720] * 1000)
#print(np.sum(var1[1:5, 360, 720] * 1000))

zon_avg1 = np.sum(var[:, 360, :], axis=1)
zon_avg2 = np.sum(var1[:, 360, :], axis=1)
print(zon_avg1)
print(zon_avg2)
print('===============================================================')
print(f1.time.data)

import matplotlib.pyplot as plt

plt.plot(f0.time.data, zon_avg1, 'r')

plt.plot(f1.time.data, zon_avg2, 'k')

plt.show()

#print(np.average(zon_avg1) * 18)
#print(np.sum(zon_avg2[:19]))