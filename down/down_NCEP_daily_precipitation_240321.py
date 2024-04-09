'''
2024-3-21
download NCEP precipitation
'''
import os

command0 = 'wget https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/Dailies/surface_gauss/prate.sfc.gauss.yyyy.nc'
command  = []

for years in range(1980, 2015):
    command.append(command0.replace('yyyy', str(years)))

for cmd in command:
    os.system(cmd)