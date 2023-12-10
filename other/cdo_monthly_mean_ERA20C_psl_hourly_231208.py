'''
This script is to cdo calculate PSL monthly-average
'''
import os

path0 = '/Volumes/samssd/ERA20C/hourly/'
path1 = '/Volumes/samssd/ERA20C/monthly/'

file_list = os.listdir(path0)

for ffff in file_list:
    name_new = ffff.replace("3hr", "monthly")

    os.system("cdo monmean "+path0+ffff+" "+path1+name_new)