'''
2024-4-15
This script is to calculate climatological wet days under historical/SSP370/SSP370lowNTCF simulation

Note:
Because the input is the every year's JJAS wet day, so the shape is year-lat-lon
'''
import xarray as xr
import numpy as np
import os
import sys
import cftime

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', ] # GISS provide no daily data
type0        = ['wet_day', 'pr10', 'pr10-25', 'pr1-10', 'pr20', 'pr25']

path_src = '/home/sun/data/process/analysis/AerChem/wet_day_intepolation/'

def return_array(filename, prtype):
    '''
        This function is to generate the shape of the climatological wet day
    '''
    f0 = xr.open_dataset(path_src + prtype + '/' + filename)

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

    for pr_type in type0:
        dataset_allmodel = xr.Dataset()

        file_all = os.listdir(path_src + pr_type + '/') ; file_all.sort()

        for modelname in models_label:
            group_hist = []
            group_ssp  = []
            group_ntcf = []
            file_model = []

            for ff in file_all:
                if modelname in ff:
                    file_model.append(ff)

            print(f'Successfully extract {modelname} from all the file for the type {pr_type}, it includes {len(file_model)}')
            
            for ff2 in file_model:
                if 'historical' in ff2:
                    f1 = xr.open_dataset(path_src + pr_type + '/' + ff2)

                    group_hist.append(f1['wet_day'].data)
                elif 'NTCF' in ff2:
                    f1 = xr.open_dataset(path_src + pr_type + '/' + ff2)

                    group_ntcf.append(f1['wet_day'].data)
                else:
                    f1 = xr.open_dataset(path_src + pr_type + '/' + ff2)

                    group_ssp.append(f1['wet_day'].data)

            if len(group_hist) == len(group_ntcf) == len(group_ssp):
                print('It pass the number test')

            
## --------------------------------------------------------------------------------------------------------------------        
            if len(group_hist) == 3:
                hist_average = np.array([group_hist[0], group_hist[1], group_hist[2]])
                ssp_average  = np.array([group_ssp[0], group_ssp[1], group_ssp[2]])
                ntcf_average = np.array([group_ntcf[0], group_ntcf[1], group_ntcf[2]])
                
            elif len(group_hist) == 1:
                hist_average = np.array([group_hist[0], group_hist[0], group_hist[0]])
                ssp_average  = np.array([group_ssp[0],  group_ssp[0], group_ssp[0]])
                ntcf_average = np.array([group_ntcf[0], group_ntcf[0], group_ntcf[0]])
            else:
                sys.exit(f'The length of {modelname} is wrong!, which is {len(group_hist)}')
#
#        date0 = cftime.num2date(np.linspace(1, 360, 360), units='days since 2000-01-01', calendar='360_day')
#        # Add them to the DataArray
            time_hist = np.linspace(1950, 2014, 65)
            time_ssp  = np.linspace(2015, 2050, 36)
            lon       = f1.lon.data
            lat       = f1.lat.data
            da_hist = xr.DataArray(data=hist_average, dims=["realization", "time_hist", "lat", "lon"],
                                    coords=dict(
                                        realization=(["realization"], [1, 2, 3]),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_hist"], time_hist),
                                    ),
                                    attrs=dict(
                                        description="wet day",
                                    ),
                                    )
            da_ssp  = xr.DataArray(data=ssp_average, dims=["realization", "time_ssp", "lat", "lon"],
                                    coords=dict(
                                        realization=(["realization"], [1, 2, 3]),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_ssp"], time_ssp),
    #                                    reference_time=reference_time,
                                    ),
                                    attrs=dict(
                                        description="wet day",
                                    ),
                                    )
            da_ntcf = xr.DataArray(data=ntcf_average, dims=["realization", "time_ssp", "lat", "lon"],
                                    coords=dict(
                                        realization=(["realization"], [1, 2, 3]),
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_ssp"], time_ssp),
                                    ),
                                    attrs=dict(
                                        description="wet day",
                                    ),
                                    )

            # Add them to the Dataset
            dataset_allmodel["{}_{}_hist".format(pr_type, modelname)]    = da_hist
            dataset_allmodel["{}_{}_ssp".format(pr_type, modelname)]     = da_ssp
            dataset_allmodel["{}_{}_sspntcf".format(pr_type, modelname)] = da_ntcf
#
            print('Now the dealing with {} has all completed!'.format(modelname))
            print('=============================================================')
#        
        dataset_allmodel.attrs['description'] = 'Created on 2024-4-16. This file includes the counts of the wet day for single model, covering historical, SSP370 and SSP270lowNTCF experiments. All the variables is climatological, which is 1980-2014 for hist and 2031-2050 for SSP370. The new means it dropped the NorESM.'
        dataset_allmodel.to_netcdf('/home/sun/data/process/analysis/AerChem/multiple_model_climate_realization_include_{}.nc'.format(pr_type))


        

        

if __name__ == '__main__':
    main()