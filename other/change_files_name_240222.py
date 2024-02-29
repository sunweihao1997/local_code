'''
2024-2-22
This script is to change the files name
'''
import os

path_in = '/home/sun/data/download_data/CESM2_LE/day_PRECT/cdo/'

files   = os.listdir(path_in)

print(files[0][:-2])
print(files[0][-2:])

for ffff in files:
    new_name = ffff[:-2] + '.' + ffff[-2:]

    os.system('mv ' + path_in + ffff + ' ' + path_in + new_name)