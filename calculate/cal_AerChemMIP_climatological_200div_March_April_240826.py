'''
2024-5-21
This script is to calculate climatological rsds under SSP370/SSP370lowNTCF simulation

Note:
MJJAS / not include historical simulation
'''
import xarray as xr
import numpy as np
import os
import sys
import cftime

models_label = ['EC-Earth3-AerChem', 'UKESM1-0-LL', 'GFDL-ESM4', 'MRI-ESM2','MPI-ESM-1-2-HAM', 'MIROC6', 'GISS-E2-1-G']

path_src = '/home/sun/data/AerChemMIP/process/200_div_samegrid/'

# Only consider JJAS and unify the year axis
months   =  [3, 4]
hist_year=  np.linspace(1985, 2014, 2014-1985+1)
furt_year=  np.linspace(2015, 2050, 2050-2015+1)

varname  =  'div'

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
            if 'NTCF' in ff2:
                f1 = xr.open_dataset(path_src + ff2)

                f1_JJAS      = f1.sel(time=f1.time.dt.month.isin(months))
                f1_JJAS_furt = f1_JJAS.sel(time=f1_JJAS.time.dt.year.isin(furt_year))

                group_ntcf.append(f1_JJAS_furt.groupby('time.year').mean())
            else:
                f1 = xr.open_dataset(path_src + ff2)

                f1_JJAS      = f1.sel(time=f1.time.dt.month.isin(months))
                f1_JJAS_furt = f1_JJAS.sel(time=f1_JJAS.time.dt.year.isin(furt_year))

                group_ssp.append(f1_JJAS_furt.groupby('time.year').mean())

        if len(group_ntcf) == len(group_ssp):
            print('It pass the number test')


## --------------------------------------------------------------------------------------------------------------------        
            if len(group_ssp) == 3:
                ssp_average  = (group_ssp[0][varname].data + group_ssp[1][varname].data + group_ssp[2][varname].data) / 3
                ntcf_average = (group_ntcf[0][varname].data + group_ntcf[1][varname].data + group_ntcf[2][varname].data) / 3
            elif len(group_ssp) == 1:
                ssp_average  = group_ssp[0][varname].data
                ntcf_average = group_ntcf[0][varname].data
            else:
                sys.exit(f'The length of {modelname} is wrong!, which is {len(group_ssp)}')
#
#        date0 = cftime.num2date(np.linspace(1, 360, 360), units='days since 2000-01-01', calendar='360_day')
#        # Add them to the DataArray
            time_hist = np.linspace(1985, 2014, 2014-1985+1)
            time_ssp  = np.linspace(2015, 2050, 2050-2015+1)
            lon       = f1.lon.data
            lat       = f1.lat.data
            #print(hist_average.shape)
            da_ssp  = xr.DataArray(data=ssp_average, dims=["time_ssp", "lat", "lon"],
                                    coords=dict(
                                        lon=(["lon"], lon),
                                        lat=(["lat"], lat),
                                        time=(["time_ssp"], time_ssp),
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
            dataset_allmodel["{}_ssp".format(modelname)]     = da_ssp
            dataset_allmodel["{}_sspntcf".format(modelname)] = da_ntcf
#
            print('Now the dealing with {} has all completed!'.format(modelname))
            print('=============================================================')
#        
        dataset_allmodel.attrs['description'] = 'Created on 2024-4-24. This file includes the counts of the rsds for single model, covering historical, SSP370 and SSP270lowNTCF experiments. All the variables is climatological, which is 1980-2014 for hist and 2015-2050 for SSP370.'
        dataset_allmodel.to_netcdf('/home/sun/data/AerChemMIP/process/multiple_model_climate_div200_month_MA.nc')



if __name__ == '__main__':
    main()