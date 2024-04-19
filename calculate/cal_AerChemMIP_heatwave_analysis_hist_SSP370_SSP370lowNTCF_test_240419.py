'''
2024-4-17
This script is to calculate the heat wave events for the historical, SSP370 and SSP370lowNTCF experiments. Here I only consider summer's HW events.

Note:
A HW is defined when the daily temperature is higher than the relative threshold for at least 3 days. reference: https://journals.ametsoc.org/view/journals/clim/32/14/jcli-d-18-0479.1.xml#bib30

To calculate the HW events, here I would compare hist-ssp370-ssp370ntcf with hist-sample for each model realization. For example, 3 scenarios with EC-Earth3-AerChem_historical_r1i1p1f1.
'''
import xarray as xr
import numpy as np


# ========================== File Information =============================
path_sample = '/home/sun/data/process/analysis/AerChem/heat_wave/sample_JJAS/'

varname = ['tasmax', 'tasmin']
threshold_name = ['threshold90', 'threshold95', 'threshold99']

path_datamin  = '/home/sun/data/process/model/aerchemmip-postprocess/tasmin/'
path_datamax  = '/home/sun/data/process/model/aerchemmip-postprocess/tasmax/'
# =========================================================================

def align_the_ncfile(filename):
    '''
        This function is to filter out a group, for each sample (2, tasmax and tasmin) allocate 6 datafile (3 tasmax and 3 tasmin:hist-ssp370-ssp370lowntcf)
        Note: In different directory the file name is the same

        return value: subset of tasmin and tasmax data, the first element is the same and the following is hist SSP370 SSP370lowNTCF
    '''
    # 1. Get the sample data
    sample_tasmax = xr.open_dataset(path_sample + 'tasmax' + '/' + filename)
    sample_tasmin = xr.open_dataset(path_sample + 'tasmin' + '/' + filename)

    # 2. Get the original data
    # Because the file name are same, here I only need to replace the exp_name
    filename_ssp     = filename.replace('historical', 'SSP370')
    filename_sspntcf = filename.replace('historical', 'SSP370NTCF')

    fhist_min = xr.open_dataset(path_datamin + filename) ; fssp_min = xr.open_dataset(path_datamin + filename_ssp) ; fntcf_min = xr.open_dataset(path_datamin + filename_sspntcf)
    fhist_max = xr.open_dataset(path_datamax + filename) ; fssp_max = xr.open_dataset(path_datamax + filename_ssp) ; fntcf_max = xr.open_dataset(path_datamax + filename_sspntcf)

    #print(np.unique(fhist_max.sel(time=fhist_max.time.dt.month.isin([6, 7, 8, 9])).time.dt.year.data))

    data_tasmax = [sample_tasmax, fhist_max.sel(time=fhist_max.time.dt.month.isin([6, 7, 8, 9])), fssp_max.sel(time=fssp_max.time.dt.month.isin([6, 7, 8, 9])), fntcf_max.sel(time=fntcf_max.time.dt.month.isin([6, 7, 8, 9]))]
    data_tasmin = [sample_tasmin, fhist_min.sel(time=fhist_min.time.dt.month.isin([6, 7, 8, 9])), fssp_min.sel(time=fssp_min.time.dt.month.isin([6, 7, 8, 9])), fntcf_min.sel(time=fntcf_min.time.dt.month.isin([6, 7, 8, 9]))]


    return data_tasmin, data_tasmax # Note the original data have been selected only includes JJAS data

def count_continue_hw_day_duration(array0):
    '''
        The input is 1d-array, corresponding to the 1 yr's JJAS time series. This function is the subfunction of func:cal_frequency, in the input array, 1 means exceeding the threshold, 0 means no.  
        This function can also calculate the duration of the heat wave
    '''
    heatwave_count = 0
    heatwave_event_days = 0
    heatwave_event_anomaly = 0

    consecutive_ones = 0
    # 如果统共没3个那就返回0, 0, 0
    if np.sum(array0 != np.nan) < 3:
        #print('no heatwave')
        return 0, 0, 0
    
    else:
        #print('heatwave')
        start_loc = 0
        while start_loc < len(array0) - 3:
            #print(array0[start_loc])
            # The first judgement, while fail then turn to next location
            if np.isnan(array0[start_loc]):
                #print('no heatwave')
                start_loc += 1

                continue
            
            # If it is surpass the threshold: 
            elif ~np.isnan(array0[start_loc]):
                # Whether it fullfil 3 days
                if np.sum(~np.isnan(array0[start_loc:start_loc+3])) < 3:

                    start_loc += 1

                    continue
                else:
                    #print('detect a hw event')
                    # At this time, a heat wave events has been confirmed
                    heatwave_count += 1
                    #print(heatwave_count)

                    # Now it is to collect the information about duration days and intensity

                    start_loc_sub = 0 
                
                    while start_loc + start_loc_sub < len(array0): # Constraint the number in the length of array0
                        #print(start_loc + start_loc_sub)
                        if ~np.isnan(array0[start_loc_sub + start_loc]):
                            #print('it is continue')
                            heatwave_event_days += 1
                            heatwave_event_anomaly += array0[start_loc_sub + start_loc]

                            start_loc_sub += 1
                        else:
                            #print('it is suspend')
                            start_loc += start_loc_sub # Skip the heatwave events days

                            break

                    start_loc += start_loc_sub

                    


        #print('calculate end')
        if heatwave_count == 0:
            return 0, 0, 0
        else:
            #print(heatwave_count)
            return heatwave_count, (heatwave_event_days / heatwave_count), (heatwave_event_anomaly / heatwave_count) # Frequency, average duration, average intensity

def cal_frequency(tasmin, tasmax, out_path, out_name):
    '''
        This function is the subfunction of the func:cal_HW, which focus on the HW frequency
    '''
    # 1. Initialize the array
    year_hist = np.unique(tasmin[1].time.dt.year.data) ; year_ssp = np.unique(tasmin[2].time.dt.year.data) ; year_ntcf = np.unique(tasmin[3].time.dt.year.data)
    year_hist = year_hist[-50:] ; year_ssp = year_ssp[:36] ; year_ntcf = year_ntcf[:36]

    #print(year_hist)

    lat       = tasmin[1].lat.data ; lon       = tasmin[1].lon.data

    # The first axis is events, duration, intensity
    hist_hw_tasmin = np.zeros((3, len(year_hist),len(lat), len(lon)))  ; hist_hw_tasmax = hist_hw_tasmin.copy()
    ssp_hw_tasmin  = np.zeros((3, len(year_ssp), len(lat), len(lon)))  ; ssp_hw_tasmax  = ssp_hw_tasmin.copy()
    ntcf_hw_tasmin = np.zeros((3, len(year_ssp), len(lat), len(lon)))  ; ntcf_hw_tasmax = ntcf_hw_tasmin.copy()

    # 2. calculate the events for each year
    # 2.1 calculate the historical simulation
    j = 0 # Number control the iteration for historical
    for yyyy0 in year_hist:
        hist_hw_tasmin_1yr = tasmin[1].sel(time=tasmin[1].time.dt.year.isin([yyyy0]))
        hist_hw_tasmax_1yr = tasmax[1].sel(time=tasmax[1].time.dt.year.isin([yyyy0]))

        # The following can be replaced with the line 101-102
        #bool_hist_tasmin        = (hist_hw_tasmin_1yr['tasmin'].data > tasmin[0]['threshold90'].data)
        #bool_hist_tasmax        = (hist_hw_tasmax_1yr['tasmax'].data > tasmax[0]['threshold90'].data)

        anomaly_hist_tasmin     = hist_hw_tasmin_1yr['tasmin'].data - tasmin[0]['threshold90'].data ; anomaly_hist_tasmin[anomaly_hist_tasmin < 0] = np.nan  # Mask the negative value, only contain the anomalies in possible heatwave 
        anomaly_hist_tasmax     = hist_hw_tasmax_1yr['tasmax'].data - tasmax[0]['threshold90'].data ; anomaly_hist_tasmax[anomaly_hist_tasmax < 0] = np.nan  # Mask the negative value, only contain the anomalies in possible heatwave

        # for every grid calculate the heat wave information
        for yy in range(len(lat)):
            for xx in range(len(lon)):
                hist_hw_tasmin[:, j, yy, xx] = count_continue_hw_day_duration(anomaly_hist_tasmin[:, yy, xx])
                hist_hw_tasmax[:, j, yy, xx] = count_continue_hw_day_duration(anomaly_hist_tasmax[:, yy, xx])

        j += 1
        print(f'Now it is in the year {yyyy0} for historical {out_name}')

    # 2.2 calculate the SSP370/ simulation
    j = 0 # Number control the iteration for SSP370
    for yyyy0 in year_ssp:
        ssp_hw_tasmin_1yr  = tasmin[2].sel(time=tasmin[2].time.dt.year.isin([yyyy0]))
        ssp_hw_tasmax_1yr  = tasmax[2].sel(time=tasmax[2].time.dt.year.isin([yyyy0]))

        # The following can be replaced with the line 101-102
        #bool_hist_tasmin        = (hist_hw_tasmin_1yr['tasmin'].data > tasmin[0]['threshold90'].data)
        #bool_hist_tasmax        = (hist_hw_tasmax_1yr['tasmax'].data > tasmax[0]['threshold90'].data)

        anomaly_ssp_tasmin     = ssp_hw_tasmin_1yr['tasmin'].data - tasmin[0]['threshold90'].data ; anomaly_ssp_tasmin[anomaly_ssp_tasmin < 0] = np.nan  # Mask the negative value, only contain the anomalies in possible heatwave 
        anomaly_ssp_tasmax     = ssp_hw_tasmax_1yr['tasmax'].data - tasmax[0]['threshold90'].data ; anomaly_ssp_tasmax[anomaly_ssp_tasmax < 0] = np.nan  # Mask the negative value, only contain the anomalies in possible heatwave

        # for every grid calculate the heat wave information
        for yy in range(len(lat)):
            for xx in range(len(lon)):
                ssp_hw_tasmin[:, j, yy, xx]  = count_continue_hw_day_duration(anomaly_ssp_tasmin[:, yy, xx])
                ssp_hw_tasmax[:, j, yy, xx]  = count_continue_hw_day_duration(anomaly_ssp_tasmax[:, yy, xx])

        j += 1
        print(f'Now it is in the year {yyyy0} for SSP {out_name}')

    # 2.3 calculate the SSP370lowNTCF simulation
    j = 0 # Number control the iteration for SSP370
    for yyyy0 in year_ntcf:
        ntcf_hw_tasmin_1yr = tasmin[3].sel(time=tasmin[3].time.dt.year.isin([yyyy0]))
        ntcf_hw_tasmax_1yr = tasmax[3].sel(time=tasmax[3].time.dt.year.isin([yyyy0]))

        # The following can be replaced with the line 101-102
        #bool_hist_tasmin        = (hist_hw_tasmin_1yr['tasmin'].data > tasmin[0]['threshold90'].data)
        #bool_hist_tasmax        = (hist_hw_tasmax_1yr['tasmax'].data > tasmax[0]['threshold90'].data)

        anomaly_ntcf_tasmin    = ntcf_hw_tasmin_1yr['tasmin'].data - tasmin[0]['threshold90'].data ; anomaly_ntcf_tasmin[anomaly_ntcf_tasmin < 0] = np.nan  # Mask the negative value, only contain the anomalies in possible heatwave 
        anomaly_ntcf_tasmax    = ntcf_hw_tasmax_1yr['tasmax'].data - tasmax[0]['threshold90'].data ; anomaly_ntcf_tasmax[anomaly_ntcf_tasmax < 0] = np.nan  # Mask the negative value, only contain the anomalies in possible heatwave

        # for every grid calculate the heat wave information
        for yy in range(len(lat)):
            for xx in range(len(lon)):
                ntcf_hw_tasmin[:, j, yy, xx] = count_continue_hw_day_duration(anomaly_ntcf_tasmin[:, yy, xx])
                ntcf_hw_tasmax[:, j, yy, xx] = count_continue_hw_day_duration(anomaly_ntcf_tasmax[:, yy, xx])

        j += 1
        print(f'Now it is in the year {yyyy0} for SSP370lowNTCF {out_name}')

    # Write to ncfile
    ncfile  =  xr.Dataset(
        {
            "hist_hw_tasmin":     (["info", "time0", "lat", "lon"], hist_hw_tasmin), 
            "hist_hw_tasmax":     (["info", "time0", "lat", "lon"], hist_hw_tasmax), 
            "ssp_hw_tasmin":      (["info", "time1", "lat", "lon"], ssp_hw_tasmin), 
            "ssp_hw_tasmax":      (["info", "time1", "lat", "lon"], ssp_hw_tasmax), 
            "ntcf_hw_tasmin":     (["info", "time2", "lat", "lon"], ntcf_hw_tasmin), 
            "ntcf_hw_tasmax":     (["info", "time2", "lat", "lon"], ntcf_hw_tasmax),             
        },
        coords={
            "time0": (["time0"], year_hist),
            "info":  (["info"],  ['events_number', 'duration', 'intensity']),
            "time1": (["time1"], year_ssp),
            "time2": (["time2"], year_ntcf),
            "lat":  (["lat"],    lat),
            "lon":  (["lon"],    lon),
        },
        )

    ncfile.attrs['description'] = 'Created on 2024-4-17. This file generated by cal_AerChemMIP_heatwave_analysis_hist_SSP370_SSP370lowNTCF_240417.py from Huaibei server. This file save the result of Heat Wave information for the tasmin/tasmax under 3 scenarios.'
    #ncfile.attrs['Note']        = 'This pentad averaged precipitation does not includes NorESM'

    ncfile.to_netcdf(out_path + out_name)


if __name__ == '__main__':
    import os

    out_path = '/home/sun/data/process/analysis/AerChem/heat_wave/result/'

    sample_lists = os.listdir(path_sample + 'tasmax/') ; sample_lists.sort()

    
#    print(sample_lists)
    for sample0 in sample_lists:
        print('Now it is deal with {}'.format(sample0))
        testmin, testmax = align_the_ncfile(sample0)
        #print(testmin[1])
        cal_frequency(testmin, testmax, out_path, sample0.replace('historical', 'heat_wave'))


#    testmin, testmax = align_the_ncfile('MRI-ESM2_historical_r1i1p1f1.nc')
#    print('success')
#
#    cal_frequency(testmin, testmax, out_path, 'test.nc')