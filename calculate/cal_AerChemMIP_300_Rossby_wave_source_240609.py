'''
2024-6-9
This script is to calculate the RWS at 300 hPa between SSP370 and SSP370lowNTCF
'''
import xarray as xr
import numpy as np
from windspharm.xarray import VectorWind
import os

# =============== File Information ==================
path_u = '/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/'
path_v = '/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/'
path_s = '/home/sun/wd_disk/AerChemMIP/download/mon_rws_cat/'

file_u = os.listdir(path_u) ; file_u.sort()

# ===================================================

# Function about RWS calculating
def cal_rws(ncfileu, ncfilev, level):
    '''
    This function only calculate single layers RWS
    '''
    ncfileu_single = ncfileu.sel(plev=level)
    ncfilev_single = ncfilev.sel(plev=level)

    uwnd           = ncfileu_single['ua']
    vwnd           = ncfilev_single['va']

    w              = VectorWind(uwnd, vwnd)

    eta = w.absolutevorticity()
    div = w.divergence()
    uchi, vchi = w.irrotationalcomponent()
    etax, etay = w.gradient(eta)
    etax.attrs['units'] = 'm**-1 s**-1'
    etay.attrs['units'] = 'm**-1 s**-1'

    # Combine the components to form the Rossby wave source term.
    S = eta * -1. * div - (uchi * etax + vchi * etay)

    return S

if __name__ == '__main__':
    for ff in file_u:
        ufile = xr.open_dataset(path_u + ff)
        vfile = xr.open_dataset(path_v + ff.replace('ua_', 'va_'))

        lev   = 30000

        s_value = cal_rws(ufile, vfile, lev)

        # Write to ncfile
        sfile = ufile.sel(plev=lev)
        sfile['ua'].data = s_value

        sfile = sfile.rename({"ua":"rws"})
        sfile.to_netcdf(path_s + ff.replace('ua_', 'rws_'))


        print(f'Finish calculating the {ff}')


