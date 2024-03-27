'''
2024-3-14
This script is to calculate climatological annual evolution of the precipitation for each model, which would be used to calculate the monsoon onset date.

Some point should be noted:
1. I am going to calculate climatological onset date for each model and then calculate the multi-model mean
2. As I know, the models I utilize can be divided into three parts: include leap year, no leap year, 360 days per year. For the leap year I would only keep the first 365 days
'''
import xarray as xr
import numpy as np
import os
import sys
import cftime

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ]

path_src = '/home/sun/data/download_data/AerChemMIP/day_prect/cdo_cat_samegrid/'

file_all = os.listdir(path_src) ; file_all.sort()

ref_file = xr.open_dataset(path_src + file_all[5])
lat      = ref_file.lat.data
lon      = ref_file.lon.data

def return_array(filename):
    '''
        This function is to generate the shape of the climatological daily precipitation
        1. for leap year and no leap year it returns (365, 91, 181)
        2. for 360 days model it returns (360, 91, 181)
    '''
    f0 = xr.open_dataset(path_src + filename)

    if 'historical' in filename:
        f1 = f0.sel(time=f0.time.dt.year.isin([2000]))
    else:
        f1 = f0.sel(time=f0.time.dt.year.isin([2024]))

    day_length = len(f1.time.data)
    lat_length = len(f1.lat.data)
    lon_length = len(f1.lon.data)

    if day_length == 360:
        return np.zeros((day_length, lat_length, lon_length)), 360, cftime.num2date(range(1, 361), units='days since 2000-01-01', calendar='360_day')
    elif day_length == 365 or day_length == 366:
        return np.zeros((365, lat_length, lon_length)), 365, cftime.num2date(range(1, 366), units='days since 2000-01-01', calendar='365_day') # dump the leap year
    else:
        sys.exit(f'Encounter problem when deal with {filename}')

def calculate_climate_precip(climate_prect, filename, length_peryear, year_range):
    year_list = np.linspace(year_range[0], year_range[1], year_range[1] - year_range[0] + 1)

    f0        = xr.open_dataset(path_src + filename)
    year_num  = year_range[1] - year_range[0] + 1

    for yyyy in year_list:
        f1        = f0.sel(time=f0.time.dt.year.isin([yyyy]))

        climate_prect += (f1.pr.data[:length_peryear] / year_num)

    
    return climate_prect
    



def main(): 

    dataset_allmodel = xr.Dataset()

    for modelname in models_label:
        group_hist = []
        group_ssp  = []
        group_ntcf = []
        file_model = []

        for ff in file_all:
            if modelname in ff:
                file_model.append(ff)
        
        print(f'Successfully extract {modelname} from all the file, it includes {len(file_model)}')

        for ff in file_model:
            climate_prect0, day_length0, date0 = return_array(ff) # Check if it could return the correct result; Yes it is.

            # 2. Select the range of the year
            if 'historical' in ff:
                year_range0 = [1980, 2014]
            else:
                year_range0 = [2031, 2050]

            climate_prect1  = calculate_climate_precip(climate_prect0, ff, day_length0, year_range0)

            if 'historical' in ff:
                group_hist.append(climate_prect1)
            elif 'NTCF' in ff:
                group_ntcf.append(climate_prect1)
            else:  
                group_ssp.append(climate_prect1)

        print(f'Now the calculation for the {modelname} has been finished, the number of historical, SSP and NTCF is {len(group_hist)}, {len(group_ssp)}, {len(group_ntcf)}')
        
        if len(group_hist) == 3:
            hist_average = (group_hist[0] + group_hist[1] + group_hist[2]) / 3
            ssp_average  = (group_ssp[0] + group_ssp[1] + group_ssp[2]) / 3
            ntcf_average = (group_ntcf[0] + group_ntcf[1] + group_ntcf[2]) / 3
        elif len(group_hist) == 1:
            hist_average = group_hist[0]
            ssp_average  = group_ssp[0] 
            ntcf_average = group_ntcf[0]
        else:
            sys.exit(f'The length of {modelname} is wrong!, which is {len(group_hist)}')

        date0 = cftime.num2date(np.linspace(1, 360, 360), units='days since 2000-01-01', calendar='360_day')
        # Add them to the DataArray
        da_hist = xr.DataArray(data=hist_average[:360], dims=["time", "lat", "lon"],
                                coords=dict(
                                    lon=(["lon"], lon),
                                    lat=(["lat"], lat),
                                    time=(["time"], date0),
#                                    reference_time=reference_time,
                                ),
                                attrs=dict(
                                    description="precipitation",
                                    units=ref_file.pr.attrs['units'],
                                ),
                                )
        da_ssp  = xr.DataArray(data=ssp_average[:360], dims=["time", "lat", "lon"],
                                coords=dict(
                                    lon=(["lon"], lon),
                                    lat=(["lat"], lat),
                                    time=(["time"], date0),
#                                    reference_time=reference_time,
                                ),
                                attrs=dict(
                                    description="precipitation",
                                    units=ref_file.pr.attrs['units'],
                                ),
                                )
        da_ntcf = xr.DataArray(data=ntcf_average[:360], dims=["time", "lat", "lon"],
                                coords=dict(
                                    lon=(["lon"], lon),
                                    lat=(["lat"], lat),
                                    time=(["time"], date0),
#                                    reference_time=reference_time,
                                ),
                                attrs=dict(
                                    description="precipitation",
                                    units=ref_file.pr.attrs['units'],
                                ),
                                )
        
        # Add them to the Dataset
        dataset_allmodel["{}_hist".format(modelname)]    = da_hist
        dataset_allmodel["{}_ssp".format(modelname)]     = da_ssp
        dataset_allmodel["{}_sspntcf".format(modelname)] = da_ntcf

        print('Now the dealing with {} has all completed!'.format(modelname))
        print('=============================================================')
        
    dataset_allmodel.attrs['description'] = 'Created on 2024-3-14. This file includes the daily precipitation for single model, covering historical, SSP370 and SSP270lowNTCF experiments. All the variables is climatological, which is 1980-2014 for hist and 2031-2050 for SSP370. The new means it dropped the NorESM.'
    dataset_allmodel.to_netcdf('/home/sun/data/process/analysis/AerChem/multiple_model_climate_prect_daily_new.nc')
        

        

if __name__ == '__main__':
    main()