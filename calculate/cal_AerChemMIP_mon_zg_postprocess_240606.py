'''
2024-6-6
This script is to calculate the postprocess for some variables: monthly zg

Note: It is multiple variable post-process and I do not want to change the script so I would deal with each variable manually
'''
import os

data_path = '/home/sun/wd_disk/AerChemMIP/download/mon_zg/'

files_all = os.listdir(data_path)

variable_list  =  ['zg']

var0           =  variable_list[0]

end_path  = '/home/sun/wd_disk/AerChemMIP/download/mon_zg_cat/'

from cdo import *
cdo = Cdo()

ncfiles   = []

for ff in files_all:
    if ff[:len(var0)] == var0 and ff[-2:] == 'nc':
        ncfiles.append(ff)

    else:
        continue

#print(ncfiles)
# Sort them by their names
historical_file = []
ssp370          = []
ssp370_NTCF     = []
ssp370_NTCFCH4  = []

for fff in ncfiles:
    if 'historical' in fff:
        historical_file.append(fff)

    elif 'ssp370' in fff and 'lowNTCF' not in fff:
        ssp370.append(fff)
    elif 'lowNTCF' in fff and 'NTCFCH4' not in fff:
        ssp370_NTCF.append(fff)
    elif 'NTCFCH4' in fff:
        ssp370_NTCFCH4.append(fff)

# Deal with data by the models name

def return_same_model(list0, modelname):
    '''
        This function return the same model groups files
    '''
    same_group = []
    for ff in list0:
        if modelname in ff:
            same_group.append(ff)
        else:
            continue
    
    same_group.sort()

    return same_group

def return_same_variantid(list1, variantid):
    '''
        This function deal with data, sorting them by variant id
    '''
    same_group = []
    for ff in list1:
        if variantid in ff:
            same_group.append(ff)
        else:
            continue
    
    same_group.sort()

    return same_group

def show_group_names(list2):
    '''
        Even for the same experiment and same model, the variantid may be different, this function is to show how many variant group they are
    '''
    variant_names = []
    for ff in list2:
        # Split each character by _
        ff_split = ff.split("_")
        if ff_split[4] in variant_names:
            continue
        else:
            variant_names.append(ff_split[4])

    return variant_names

def cdo_inputfiles(datalists, new_name):
    cdo.cat(input = [(data_path + x) for x in datalists],output = end_path + new_name)

def ec_earth_data():

    Model_name         = 'EC-Earth3-AerChem'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'EC-Earth3 historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with EC-Earth3-AerChem historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'EC-Earth3 ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with EC-Earth3-AerChem SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'EC-Earth3 ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with EC-Earth3-AerChem SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'EC-Earth3 ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with EC-Earth3-AerChem SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def ukesm_data():

    Model_name         = 'UKESM1-0-LL'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def gfdl_data():

    Model_name         = 'GFDL-ESM4'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def mri_data():

    Model_name         = 'MRI-ESM2'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def giss_data():

    Model_name         = 'GISS-E2-1-G'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def cesm_data():

    Model_name         = 'CESM2-WACCM'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def mpiesm_data():

    Model_name         = 'MPI-ESM-1-2-HAM'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def bcc_data():

    Model_name         = 'BCC-ESM1'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def miroc6_data():

    Model_name         = 'MIROC6'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def noresm_data():

    Model_name         = 'NorESM2-LM'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')

def cnrm_data():

    Model_name         = 'CNRM-ESM'

    # -------------- Historical ----------------
    ecearth_historical = return_same_model(historical_file, Model_name)

    ecearth_variantid  = show_group_names(ecearth_historical)

    print(f'{Model_name} historical variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_historical)}')

    # Now cdo cat them into one file for each variant member
    for vid in ecearth_variantid:
        # 1. Sort out the same group
        ecearth_historical_group = []
        for fff in ecearth_historical:
            if vid in fff:
                ecearth_historical_group.append(fff)
            else:
                continue
        print(f'It is now deal with {Model_name} historical {vid}, this subset includes {len(ecearth_historical_group)}')
        ecearth_historical_group.sort()

        # 2. Put them into cdo post-procss
        cdo_inputfiles(ecearth_historical_group, Model_name + '_' + 'historical_' + vid + '.nc')
    print('=================================================================================================')

    # -------------- SSP370 ----------------
    ecearth_ssp370     = return_same_model(ssp370, Model_name)

    ecearth_variantid  = show_group_names(ecearth_ssp370) ; print(f'The variant-id for SSP370 is {ecearth_variantid}')

    print(f'{Model_name} ssp370 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370_group = []
            for fff in ecearth_ssp370:
                if vid in fff:
                    ecearth_ssp370_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370 {vid}, this subset includes {len(ecearth_ssp370_group)}')
            ecearth_ssp370_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370_group, Model_name + '_' + 'SSP370_' + vid + '.nc')
    else:
        print(Model_name + ' provide no SSP370 experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCF ----------------
    ecearth_ssp370NTCF     = return_same_model(ssp370_NTCF, Model_name)

    ecearth_variantid      = show_group_names(ecearth_ssp370NTCF) ; print(f'The variant-id for SSP370NTCF is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCF variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCF)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCF_group = []
            for fff in ecearth_ssp370NTCF:
                if vid in fff:
                    ecearth_ssp370NTCF_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCF {vid}, this subset includes {len(ecearth_ssp370NTCF_group)}')
            ecearth_ssp370NTCF_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCF_group, Model_name + '_' + 'SSP370NTCF_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCF experiment!')
    print('=================================================================================================')

    # -------------- SSP370NTCFCH4 ----------------
    ecearth_ssp370NTCFCH4     = return_same_model(ssp370_NTCFCH4, Model_name)

    ecearth_variantid         = show_group_names(ecearth_ssp370NTCFCH4) ; print(f'The variant-id for SSP370NTCFCH4 is {ecearth_variantid}')

    print(f'{Model_name} ssp370NTCFCH4 variantid number is {len(ecearth_variantid)}, if there is no problem the number should be {165 * (len(ecearth_variantid))}, while the total number is {len(ecearth_ssp370NTCFCH4)}')

    # Now cdo cat them into one file for each variant member
    if len(ecearth_variantid) != 0:
        for vid in ecearth_variantid:
            # 1. Sort out the same group
            ecearth_ssp370NTCFCH4_group = []
            for fff in ecearth_ssp370NTCFCH4:
                if vid in fff:
                    ecearth_ssp370NTCFCH4_group.append(fff)
                else:
                    continue
            print(f'It is now deal with {Model_name} SSP370NTCFCH4 {vid}, this subset includes {len(ecearth_ssp370NTCFCH4_group)}')
            ecearth_ssp370NTCFCH4_group.sort()

            # 2. Put them into cdo post-procss
            cdo_inputfiles(ecearth_ssp370NTCFCH4_group, Model_name + '_' + 'SSP370NTCFCH4_' + vid + '.nc')
    else:
        print(Model_name + 'provide no SSP370NTCFCH4 experiment!')
    print('=================================================================================================')



def main():
    ec_earth_data()
    gfdl_data()
    giss_data()
    mri_data()
#    cesm_data()
#    bcc_data()
    ukesm_data()
    mpiesm_data()
    miroc6_data()
#    noresm_data()
#    cnrm_data()

if __name__ == "__main__":
    main()