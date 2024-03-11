'''
2024-3-8
Because the downloaded the JRA55 data is .tar format, this script is to untar these files

'''
import os
from multiprocessing import Pool

path0    = '/home/sun/data/download_data/JRA55/'

path_out = '/home/sun/data/download_data/JRA55/untar_files/'

files_all = os.listdir(path0)

files_tar = []
for ff in files_all:
    if ff[-3:] == 'tar':
        files_tar.append(ff)

for fff in files_tar:
    os.system('tar xopf ' + path0 + fff + ' -C ' + path_out)

    print(f'Successfully dealt with {fff}')