import os 

path1 = '/home/sun/data/download_data/AerChemMIP/tasmax/'
path2 = '/home/sun/data/download_data/AerChemMIP/tasmin/'

file1 = os.listdir(path1) ; file2 = os.listdir(path2)
file1nc = [];file2nc = []

for ff in file1:
    if ff[-2:] == 'nc':
        file1nc.append(ff)

for ff in file2:
    if ff[-2:] == 'nc':
        file2nc.append(ff)

for ff in file2nc:
    ff1 = ff.replace('tasmin', 'tasmax')

    if ff1 in file1nc:
        print('yes')
        continue
    else:
        print(ff)

print(len(file1nc))
print(len(file2nc))