'''
2024-2-10
This script is to show : whether the delayed monsoon onset will cause drying trend over tropical Asia

The data used in this script is CESM2 Large Ensemble
'''
import xarray as xr
import numpy as np
import os
import pymannkendall as mk
#from cdo import *

def get_whole_files():
    # ==== File location information ====

    src_path = '/home/sun/data/download_data/CESM2_LE/day_PRECT/raw/'

    # ===================================

    # ==== File list process ====
    # Under this path, the python script and BSSP370 should be removed

    file_list0 = os.listdir(src_path)
    file_list  = []

    for ffff in file_list0:
        if "python" in ffff or "BSSP" in ffff:
            continue
        else:
            file_list.append(ffff)

    file_list.sort() ; print(f'The total files list has been completed, while the number is {len(file_list)}')

    return file_list


# ==== Function: Cdo the discrete files into one file ====

def cdo_cat_LE_prect_files(end_path, list_files, member_str):
    src_path = '/home/sun/data/download_data/CESM2_LE/day_PRECT/raw/'

    cdo = Cdo()

    list_files.sort()

    cdo.cat(input=[(src_path + x) for x in list_files], output=end_path + "CESM2.large_ensemble.prect." + member_str + ".185001-201412.nc")

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ==== Function: filter out the member =======

def return_same_member_file(list_all, keyword):
    '''
        This function is used to return a list including files for each member
    '''
    new_list = []
    for ffff in list_all:
        if keyword in ffff:
            new_list.append(ffff)
        else:
            continue

    print(f"The list including {keyword} has been fitered, which includes {len(new_list)}")

    new_list.sort()

    return new_list

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ==== Function: Calculate May precipitation using daily data ====

def calculate_May_prect(f0, start_year, end_year,):

    prect_BOB = np.zeros((165,))
    prect_SCS = np.zeros((165,))
    prect_SA  = np.zeros((165,))

    j         = 0
    for yy in range(start_year, end_year + 1):
        # 1. Filter out the yearly data
        f0_year = f0.sel(time=f0.time.dt.year.isin([yy]))

        # 2. Filter out the May data
        f0_May  = f0_year.sel(time=f0_year.time.dt.month.isin([5]))

        # 3. Filter out the area data
        f0_BOB  = f0_May.sel(lat=slice(5, 15), lon=slice(85, 100))
        f0_SCS  = f0_May.sel(lat=slice(5, 15), lon=slice(110, 120))
        f0_SA   = f0_May.sel(lat=slice(5, 15), lon=slice(85, 120))

        prect_BOB[j] = np.average(f0_BOB['PRECT'].data)
        prect_SCS[j] = np.average(f0_SCS['PRECT'].data)
        prect_SA[j]  = np.average(f0_SA['PRECT'].data)

        j += 1

    return prect_BOB, prect_SCS, prect_SA

# ==== Function: Plot ====

def plot_May_prect(series, name0):
    import matplotlib.pyplot as plt
    import scipy.signal
    from scipy.signal import firwin, lfilter

    font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 12,
            }

    x  = np.linspace(1850, 2014, 165)
    y1 = series

    # ------- 5. filter ---------------------------------------------
    N = 3
    period = 11
    Wn = 2 * (1 / period) / 1


    # 5.1 butter construction
    b, a = scipy.signal.butter(N, Wn, 'lowpass')

    # 5.2 filter
    y2 = scipy.signal.filtfilt(b, a, series, axis=0)

    plt.plot([1850, 2014], [np.average(series), np.average(series)], 'k-', alpha=0.25)

    plt.plot(x, y1, 'grey', linewidth=0.8)
    plt.plot(x, y2, 'orange', linewidth=1.5)
    
    plt.plot([1890, 1910], [np.average(series[40:60]), np.average(series[40:60])], 'b--', alpha=0.75)
    plt.plot([1995, 2014], [np.average(series[-20:]), np.average(series[-20:])], 'r--', alpha=0.75)

    plt.title('May Prect over {}'.format(name0), loc='left', fontdict=font)
    plt.title('CESM2-LE', loc='right', fontdict=font)

    plt.xlabel('Year', fontdict=font)
    plt.ylabel('Days', fontdict=font)

    plt.grid(True)
    plt.xticks(np.linspace(1850, 2010, 9),)

    #print(f'Early period is {np.average(series[20:40])}, while late period is {np.average(series[-35:])}')


    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.savefig('/home/sun/paint/onset_day/CESM2_LE-{}SM_May_prect_1850_2014.pdf'.format(name0))

    plt.close()




# ========================================= Data process Module ===============================================
def post_process():
    '''
        This is the process module
    '''

    file_list_all = get_whole_files() # 1. Get the whole file lists

    end_path      = '/home/sun/data/download_data/CESM2_LE/day_PRECT/cdo/'

    for i in range(1, 11):            # 2. Cdo cat files for each member
        if i<10:
            list_member = return_same_member_file(file_list_all, ".00"+ str(i) + ".cam.")
            member_str  = "00" + str(i)
            cdo_cat_LE_prect_files(end_path, list_member, member_str)
        else:
            list_member = return_same_member_file(file_list_all, ".0"+ str(i) + ".cam.")
            member_str  = "0" + str(i)
            cdo_cat_LE_prect_files(end_path, list_member, member_str)

# ======================================== Calculate May precipitation =====================================
def prect_series():
    input_path    = '/home/sun/data/download_data/CESM2_LE/day_PRECT/cdo/'

    files         = os.listdir(input_path) ; files.sort()

    BOB           = np.zeros((10, 165))
    SCS           = np.zeros((10, 165))
    SA            = np.zeros((10, 165))

    for i in range(10):
        orign_file = xr.open_dataset(input_path + files[i])

        BOB_m, SCS_m, SA_m = calculate_May_prect(orign_file, 1850, 2014)

        BOB[i]    = BOB_m
        SCS[i]    = SCS_m
        SA[i]     = SA_m

    return np.average(BOB, axis=0), np.average(SCS, axis=0), np.average(SA, axis=0)

def main():
    #post_process()
    BOB, SCS, SA  = prect_series()

    plot_May_prect(BOB * 86400000, 'BOB')
    plot_May_prect(SCS * 86400000, 'SCS')
    plot_May_prect(SA  * 86400000, 'SEA')

if __name__ == '__main__':
    main()
