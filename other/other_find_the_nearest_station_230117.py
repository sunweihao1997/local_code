'''
2024-1-17
This script is to help lxl to calculate the distance from the Harbour to the meteorological station

The output of this script mainly contains:
1. The distance from each horbour to other observation station
2. The nearst five stations from each harbour
'''
import geopy
import pandas as pd
import numpy as np

# ======================== Area of function ============================================

def cal_distance(lat1, lon1, lat2, lon2):
    '''
        lat1, lon1: location of the harbour
        latw, lon2: location of the station
    '''
    from geopy.distance import geodesic

    distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers # units is kilometer

    return distance



# ======================== 1. Read the geography information ============================

file_path = "/Users/sunweihao/Downloads/"

file_station  = "district_China.csv" 
file_harbour  = "harbour.xlsx"

f1            = pd.read_csv(file_path + file_station)
lat_station   = f1['lat'].values #; print(lat_station.shape) # .values will return an array with length of (2168, )
lon_station   = f1['lon'].values

f2            = pd.read_excel(file_path + file_harbour)
lat_harbour   = f2['lat'].values
lon_harbour   = f2['lon'].values
#print(len(lat_harbour)) # Totally 45 harbours
#print(f1.iloc[1])
#print(f1[f1['lat'].isin([lat_station[1]])])
#a = f1['lat'].isin([lat_station[1]])
#b = f1['lon'].isin([lon_station[1]])
#print(f1[a & b])
#print(f2.iloc[:, 4])

# =======================================================================================

# ========================= 2. Calculation ==============================================

# 2.1 Claim the array to save the distance to every observation station and calculate

distance_from_harbour = np.zeros((45, 2168))

for i in range(len(lat_harbour)):
    for j in range(len(lat_station)):
        distance_from_harbour[i, j] = cal_distance(lat1=lat_harbour[i], lon1=lon_harbour[i], lat2=lat_station[j], lon2=lon_station[j])

#print(distance_from_harbour[5])

# 2.2 Find the nearst five station and their distance to the harbour

# 2.2.1 Here I modifed the pandas Dataframe from the district_China.csv, for each station row I add the distance to the total 45 harbours in the end

for i in range(45):
    num_column = f1.shape[1]

    f1.insert(loc=num_column, column='This station to {} distance(km)'.format(f2.iloc[i, 4]), value=distance_from_harbour[i])

# After insertation, the new dataframe's shape is (2168, 52), behind the original columns are the distance from station to the 45 harbours distance (km)

f1.to_excel(file_path + "Distance_station_to_each_harbour.xlsx")

# ========================= 3. Select the nearest five stations ==============================
#print(f1)

a = f1.columns.values
#print(a[7]) # 7 is the start of the harbours names
#f2 = f1.sort_values(by=[a[9]])
#
#print(f2.iloc[:5])

# 3.1 Claim the array

ids = [] ; names = []

names_check = []

five_nearst = []
for i in range(45):
    f_select = f1.sort_values(by=[a[7 + i]])
    f_select2 = f_select.iloc[:15, :7].join(f_select.iloc[:15, 7+i])

    five_nearst.append(f_select2)
    names_check.append(a[7 + i])

    for idd in f_select2['id']:
        ids.append(idd)
    for namee in f_select2['name'].values:
        names.append(namee)

#print(five_nearst[10])
for ii in range(len(five_nearst)):
    five_nearst[ii].to_excel(file_path + "The_nearst_ten_stations_to_{}.xlsx".format(a[ii + 7]))

new_id = [] ; new_name = []
for ii in ids:
    if ii not in new_id:
        new_id.append(ii)

for jj in names:
    if jj not in new_name:
        new_name.append(jj)

with open(file_path + 'id.txt', 'w') as fp:
    for item in new_id:
        # write each item on a new line
        fp.write("%s\n" % item)
    
with open(file_path + 'name.txt', 'w') as fp2:
    for item in new_name:
        # write each item on a new line
        fp2.write("%s\n" % item)