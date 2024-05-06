'''
2024-4-28
This script gives an example of calculating the intra-seasonal variability
'''
import xarray as xr
import numpy as np
from scipy.signal import butter, filtfilt

# Define a function to calculate band-pass filter
def band_pass_calculation(data, fs, low_frq, high_frq, order,):
    '''
        fs: sample freq
    '''
    lowcut  = 1/low_frq
    highcut = 1/high_frq

    b, a    = butter(N=order, Wn=[lowcut, highcut], btype='band', fs=fs)

    filtered_data = filtfilt(b, a, data)

    return filtered_data
