'''
2024-2-12
This script is to check whether the downloaded data is completed. Because during the download it sometimes will bring problems into the process

The method is to read every nc file for the given path, if the file is not complete it should give error message
'''
import os
import xarray as xr

def read_all_files(inpath):
    all_files = os.listdir(inpath) ; all_files.sort()

#    print(all_files)

    all_files_filter = []
    for ffff in all_files:
        if ".nc" in ffff:
            all_files_filter.append(ffff)

    for ffff in all_files_filter:
        f = xr.open_dataset(inpath + ffff)

        print('Successfully read {}'.format(ffff))

def main():
    pathlist = [
#        '/home/sun/data/download_data/CESM2_LE/mon_PRECT/',
#        '/home/sun/data/download_data/CESM2_LE/day_u850/temporary/',
#        '/home/sun/data/download_data/CESM2_LE/day_PRECT/raw/',
#        '/home/sun/data/download_data/CESM2_LE/day_PRECT/cdo/',
#        '/home/sun/data/download_data/CESM2_LE/day_u850/raw/',
#        '/home/sun/data/download_data/CESM2_LE/day_PRECT/raw/',
        '/home/sun/data/download_data/CESM2_LE/day_PRECT/cdo/', 
        '/home/sun/data/download_data/CESM2_LE/day_u850/cdo/'
    ]

#    pathlist2 = [
#    '/home/sun/data/download_data/CESM2_SF/'
#    ]
    for pppp in pathlist:
        read_all_files(pppp)

if __name__ == '__main__':
    main()

''' error record '''
'''
/home/sun/data/download_data/CESM2_LE/mon_PRECT/b.e21.BHISTcmip6.f09_g17.LE2-1231.003.cam.h0.PRECL.195001-195912.nc

/home/sun/data/download_data/CESM2_LE/day_u850/raw/b.e21.BHISTcmip6.f09_g17.LE2-1231.009.cam.h1.U850.18900101-18991231.nc

/home/sun/data/download_data/CESM2_LE/day_PRECT/raw/b.e21.BHISTcmip6.f09_g17.LE2-1231.006.cam.h1.PRECT.19100101-19191231.nc
'''