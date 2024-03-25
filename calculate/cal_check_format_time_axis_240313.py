'''
2024-3-13
This script is to show the format of the time-series, because in some model the number of day is 360 per year
'''
import os
import xarray as xr

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','NorESM2-LM', 'MPI-ESM-1-2-HAM', 'MIROC6', ]

path0        = '/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid/'

files_all    = os.listdir(path0)

def return_time_format(modelname):
    model_group = []
    for ffff in files_all:
        if modelname in ffff and 'historical' in ffff:
            model_group.append(ffff)
    print(model_group)
    f0 = xr.open_dataset(path0 + model_group[0])
    f1 = f0.sel(time=f0.time.dt.year.isin([2000]))

    print(f'Now it is model {modelname}, its time format is: \n')
    print(f1.time.shape)
    print('\n')

for nn in models_label:
    return_time_format(nn)