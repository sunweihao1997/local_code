'''
2024-4-9
This script is used to calculate the PET, while involved variables are tas, rh, hfss, hfls, sfcwind, ps
'''
import xarray as xr
import numpy as np

CP = 1.004 * 10**-3   #Specific heat of air at constant pressure (C_p)in MJ/(kg K)
LV = 2.45             # Latent Heat of Vaporization for Water.  FAO uses constant 2.45 MJ/kg

# FAO56 Constants 
CN_GRASS =  900     # define reference values for grass (short crop)
CD_GRASS =  0.34    # units: s/m
CN_ALFALFA =  1600  # define reference values for alfalfa (tall crop)  
CD_ALFALFA =  0.38  # units:   s/m

def scale_wind_FAO56(u_z,z=10):
    '''Calculate 2-meter wind from wind at another height using FAO56 log-layer scaling'''
    import numpy as np
    print('Scaling wind from height of ' + str(z) + ' m to 2m')
    u_2 = 4.87*u_z/np.log(67.8*z - 5.42)
    return u_2

def get_rnet(sh,lh,):

    # If rnet_calculated=True, read in Sensible and Latent heat fluxes and calculate
    #   Rnet - G from the surface energy balance: Rnet - G = SH + LH.
    #   It is assumed that SH and LH are positive-upwards so that Rnet-G is positive downwards
    #   otherwise read rnet in from a file.  Specifying a separate Ground heat flux input file is not supported.
    #
    # Unit conversion factors (FAO56 formulas require units of MJ/m^2/day)
    #    Most climate models use W/m^2.   The ERA5 reanalysis has units of J/m^2 for a specified time interval,
    #    usually a day.  See Documentation at ECMWF for more informatino,  .  
    #

    rnet_conv = 86400.0/10**6

    rnet_temp = rnet_conv*(sh + lh)   #we convert from W/m2 to MJ/day

    return rnet_temp

def PenMon(temp, sh, lh, sfcwind, ps, rh, temp_unit, veg_type='grass'):
    '''
        tas: unit should be degC, so if the unit is K it need to be converted
        sh, lh: unit should be W m**-2, and I checked most models output is this unit
        sfcwind: it should be converted into 2m wind
    '''

    # 1. Pre-process the temp
    if temp_unit == 'K':
        temp = temp - 273.15
    else:
        print(f'For this data the unit of temperature is {temp_unit}')


    # 2. Pre-process the wind
    windspeed = scale_wind_FAO56(sfcwind)

    # 3. Pre-process Radiation
    rnet     = get_rnet(sh, lh)

    # 4. Calculate psychrometric constant from surface pressure
    psychromet = CP*ps/(1000*LV*.622)   # Units: kPa/K  factor of 1000 is to convert PS in Pa to KPa. Units: kPa/K

    # 5. choose vegetation type
    if veg_type == 'grass':
        Cn = CN_GRASS
        Cd = CD_GRASS
    elif veg_type == 'alfalfa':
        Cn = CN_ALFALFA
        Cd = CD_ALFALFA

    # 6. Calculate saturation vapor pressure (svp) Note: I checked the origin script it should be in unit degC
    svp = 0.6108*np.exp( (17.27*temp)/( temp+237.3 ))    #Units: kPa

    # 7. Calculate Vapor Pressure Deficit (VPD) either using dewpoint temperature(tdew) or from relative humidity (rh) 
    vpd = (1.0 -  rh / 100.0 ) * svp 

    # Calculate delta (deriv. of esat w.r.t temperature) saturated vapor pressure curve (svpc)
    svpc = 4098*svp/((temp+237.3)**2)         # Units: kPa/K

    # Calculate PET using the Penman-Monteith formulations from FAO Pub. 56 (FAO56)

    pet = (0.408*svpc*rnet+psychromet*Cn*windspeed*vpd/(temp+273))/\
          (svpc+psychromet*(1 + Cd*windspeed))   # Units: mm/day
    pet_rad = (0.408*svpc*rnet) / (svpc+psychromet*(1 + Cd*windspeed))
    pet_adv = (psychromet*Cn*windspeed*vpd/(temp+273)) / (svpc+psychromet*(1 + Cd*windspeed))

    print(np.nanmean(pet_adv + pet_rad - pet))

    return pet, pet_rad, pet_adv