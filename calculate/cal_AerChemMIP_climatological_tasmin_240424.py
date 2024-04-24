'''
2024-4-24
This script is to calculate climatological tasmin under historical/SSP370/SSP370lowNTCF simulation

Note:
Here only plot JJAS
'''
import xarray as xr
import numpy as np
import os
import sys
import cftime

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G'] # GISS provide no daily data

path_src = '/data/AerChemMIP/tasmin_mon_postprocess_samegrid/'

# Only consider JJAS and unify the year axis
months   =  [6, 7, 8, 9]
hist_year=  np.linspace(1950, 2014, 2014-1950+1)
furt_year=  np.linspace(2015, 2050, 2050-2015+1)

varname  =  'tasmin'

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

    dataset_allmodel = xr.Dataset()

    file_all = os.listdir(path_src) ; file_all.sort()

    for modelname in models_label:
        group_hist = []
        group_ssp  = []
        group_ntcf = []
        file_model = []

        for ff in file_all:
            if modelname in ff:
                file_model.append(ff)

        print(f'Successfully extract {modelname} from all the file, it includes {len(file_model)}')
            
        for ff2 in file_model:
            if 'historical' in ff2:
                f1 = xr.open_dataset(path_src + ff2)

                f1_JJAS      = f1.sel(time=f1.time.dt.month.isin(months))
                f1_JJAS_hist = f1_JJAS.sel(time=f1_JJAS.time.dt.year.isin(hist_year))

                group_hist.append(f1_JJAS_hist.groupby('time.year').mean())
            elif 'NTCF' in ff2:
                f1 = xr.open_dataset(path_src + ff2)

                f1_JJAS      = f1.sel(time=f1.time.dt.month.isin(months))
                f1_JJAS_furt = f1_JJAS.sel(time=f1_JJAS.time.dt.year.isin(furt_year))

                group_ntcf.append(f1_JJAS_furt.groupby('time.year').mean())
            else:
                f1 = xr.open_dataset(path_src + ff2)

                f1_JJAS      = f1.sel(time=f1.time.dt.month.isin(months))
                f1_JJAS_furt = f1_JJAS.sel(time=f1_JJAS.time.dt.year.isin(furt_year))

                group_ssp.append(f1_JJAS_furt.groupby('time.year').mean())

        if len(group_hist) == len(group_ntcf) == len(group_ssp):
            print('It pass the number test')


## --------------------------------------------------------------------------------------------------------------------        
            if len(group_hist) == 3:
                hist_average = (group_hist[0]['tasmin'].data + group_hist[1]['tasmin'].data + group_hist[2]['tasmin'].data) / 3
                ssp_average  = (group_ssp[0]['tasmin'].data + group_ssp[1]['tasmin'].data + group_ssp[2]['tasmin'].data) / 3
                ntcf_average = (group_ntcf[0]['tasmin'].data + group_ntcf[1]['tasmin'].data + group_ntcf[2]['tasmin'].data) / 3
            elif len(group_hist) == 1:
                hist_average = group_hist[0]['tasmin'].data
                ssp_average  = group_ssp[0]['tasmin'].data
                ntcf_average = group_ntcf[0]['tasmin'].data
            else:
                sys.exit(f'The length of {modelname} is wrong!, which is {len(group_hist)}')
#
#        date0 = cftime.num2date(np.linspace(1, 360, 360), units='days since 2000-01-01', calendar='360_day')
#        # Add them to the DataArray
            time_hist = np.linspace(1950, 2014, 65)
            time_ssp  = np.linspace(2015, 2050, 36)
            lon       = f1.lon.data
            lat       = f1.lat.data
            #print(hist_average.shape)
            da_hist = xr.DataArray(data=hist_average, dims=["time_hist", "lat", "lon"],
                                    coords=dict(
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_hist"], time_hist),
                                    ),
                                    attrs=dict(
                                        description=varname,
                                    ),
                                    )
            da_ssp  = xr.DataArray(data=ssp_average, dims=["time_ssp", "lat", "lon"],
                                    coords=dict(
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_ssp"], time_ssp),
    #                                    reference_time=reference_time,
                                    ),
                                    attrs=dict(
                                        description=varname,
                                    ),
                                    )
            da_ntcf = xr.DataArray(data=ntcf_average, dims=["time_ssp", "lat", "lon"],
                                    coords=dict(
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_ssp"], time_ssp),
                                    ),
                                    attrs=dict(
                                        description=varname,
                                    ),
                                    )

            # Add them to the Dataset
            dataset_allmodel["{}_hist".format(modelname)]    = da_hist
            dataset_allmodel["{}_ssp".format(modelname)]     = da_ssp
            dataset_allmodel["{}_sspntcf".format(modelname)] = da_ntcf
#
            print('Now the dealing with {} has all completed!'.format(modelname))
            print('=============================================================')
#        
        dataset_allmodel.attrs['description'] = 'Created on 2024-4-24. This file includes the counts of the tasmin for single model, covering historical, SSP370 and SSP270lowNTCF experiments. All the variables is climatological, which is 1980-2014 for hist and 2031-2050 for SSP370.'
        dataset_allmodel.to_netcdf('/data/AerChemMIP/process/multiple_model_climate_tasmin_month_JJAS.nc')


        

        

if __name__ == '__main__':
    main()