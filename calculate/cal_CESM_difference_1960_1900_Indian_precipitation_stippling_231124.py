'''
2023-11-24
This script is to plot the difference between two periods (1960 and 1900) in precipitation over Indian

Following Massimo advice:
The stippling principle: when 2/3 members hold the same difference, then stipple it

2023-11-27 update
change the object to the fixEU experiment
'''
import xarray as xr
import numpy as np

# =============== File information ====================
class f1:
    '''
        This class save file location for the files
    '''

    CESM_path = '/mnt/d/samssd/precipitation/CESM/ensemble_JJAS/'
    #CESM_name = 'CESM_BTAL_esemble_JJAS_precipitation.nc'
    # 20231127 update
    CESM_name = 'CESM_noEU_esemble_JJAS_precipitation.nc'

f0 = xr.open_dataset(f1.CESM_path + f1.CESM_name)

periodA_1 = 1900 ; periodA_2 = 1920
periodB_1 = 1940 ; periodB_2 = 1960

# =============== Calculation for two period =================
def calculate_period_diff(pa1, pa2, pb1, pb2, ncfile, varname):
    '''
        This function is to calculate difference between two periods
    '''

    ncfile1 = ncfile.sel(time=slice(pa1, pa2))
    ncfile2 = ncfile.sel(time=slice(pb1, pb2))

    period_diff = np.average(ncfile2[varname].data, axis=0) - np.average(ncfile1[varname].data, axis=0)

    return period_diff

def check_sign(lists, num, size0):
    '''
        This function is to check whether this difference is same among the ensemble members
    '''

    # 1. Claim the array save the information of sign
    sign_array = np.zeros(size0)

    # 2. create a loop for calculation
    for i in range(size0[0]):
        for j in range(size0[1]):
            count_positive = 0
            count_negative = 0
            for k in range(num):
                if lists[k][i, j] >= 0:
                    count_positive += 1
                else:
                    count_negative += 1
            
            if abs(count_negative) >= 6 or abs(count_positive) >= 6:
                sign_array[i, j] = 1
            else:
                continue

    return sign_array

def save_ncfile(array, sign):
    ncfile  =  xr.Dataset(
        {
            "JJAS_prect_diff": (["member", "lat", "lon"], array),
            "sign":            (["lat", "lon"], sign),
        },
        coords={
            "member": (["member"], np.linspace(1, 8, 8)),
            "lat":  (["lat"],  f0['lat'].data),
            "lon":  (["lon"],  f0['lon'].data),
        },
            )

    return ncfile

# =================== Main calculation ==========================
diff_list = []
diff_result = np.zeros((8, 96, 144))
for i in range(8):
    diff_list.append(calculate_period_diff(pa1=periodA_1, pa2=periodA_2, pb1=periodB_1, pb2=periodB_2, ncfile=f0, varname="JJAS_prect_{}".format(i + 1)))
    diff_result[i] = calculate_period_diff(pa1=periodA_1, pa2=periodA_2, pb1=periodB_1, pb2=periodB_2, ncfile=f0, varname="JJAS_prect_{}".format(i + 1))

print("Difference calculation completed")

signs = check_sign(lists=diff_list, num=8, size0=(96, 144))

# Save to the netcdf file
#print(np.average(f0["JJAS_prect_1"]))
diff_ncfile = save_ncfile(array=diff_result, sign=signs)

out_path = "/mnt/d/samssd/precipitation/processed/"

diff_ncfile.attrs['description'] = 'This file save the JJAS precipitation difference between two periods (1901-1920 and 1941-1961). The sign array is the agreement among all the ensemble members.'
diff_ncfile.to_netcdf(out_path + "EUI_CESM_fixEU_precipitation_difference_period_1901_1960_JJAS.nc")