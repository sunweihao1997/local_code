;2023-12-5
;This script is to calculate TN wave activity flux

; Following Liu advice, I calculate geopotential height anomaly first and then calculate wave activity

begin

    ; path_src = "/exports/csce/datastore/geos/users/s2618078/data/model_data/ensemble_JJAS/"
    path_src = "/Volumes/samssd/data/ensemble_JJAS/"

    ; 1. monthly-mean data hgt units:m
    f0            = addfile(path_src + "CESM_BTAL_JJAS_Z3_ensemble.nc", "r")
    f0_BTAL       = addfile(path_src + "CESM_BTAL_JJAS_Z3_ensemble.nc", "r")
    f0_BTALnEU    = addfile(path_src + "CESM_BTALnEU_JJAS_Z3_ensemble.nc", "r")

    ; 2. monthly climatology data
    ; 2.1 hgt could use f0

    ; 2.2 air temperature units: degC (need to be change)
    f_air    = addfile(path_src + "CESM_BTALnEU_JJAS_T_ensemble.nc", "r")

    ; 2.3 zonal wind m/s
    f_u      = addfile(path_src + "CESM_BTALnEU_JJAS_U_ensemble.nc", "r")

    ; 2.4 meridional wind m/s
    f_v      = addfile(path_src + "CESM_BTALnEU_JJAS_V_ensemble.nc", "r")

    ; dimension information
    time = f0->time
    lat  = f0->lat
    lon  = f0->lon
    level= f0->lev

    ; ----------------------

    ntime = dimsizes(time)
    nlat  = dimsizes(lat)
    nlon  = dimsizes(lon)
    nlevel= dimsizes(level)

    period1 = 1940
    period2 = 1960

    ; 3. Data pre-process
    ;----------------------------------------------------------------- BTAL --------------------------------------------------------------------------------
    ; 3.1 Calculate ensemble-average climatology for hgt
    hgt_1_BTAL   = f0_BTAL->JJAS_Z3_1
    hgt_2_BTAL   = f0_BTAL->JJAS_Z3_2
    hgt_3_BTAL   = f0_BTAL->JJAS_Z3_3
    hgt_4_BTAL   = f0_BTAL->JJAS_Z3_4
    hgt_5_BTAL   = f0_BTAL->JJAS_Z3_5
    hgt_6_BTAL   = f0_BTAL->JJAS_Z3_6
    hgt_7_BTAL   = f0_BTAL->JJAS_Z3_7
    hgt_8_BTAL   = f0_BTAL->JJAS_Z3_8

    ; 3.1.1 Replace the nan data
    if (any(isnan_ieee(hgt_1_BTAL))) then
        value = 1.e20
        replace_ieeenan(hgt_1_BTAL, value, 0)
        replace_ieeenan(hgt_2_BTAL, value, 0)
        replace_ieeenan(hgt_3_BTAL, value, 0)
        replace_ieeenan(hgt_4_BTAL, value, 0)
        replace_ieeenan(hgt_5_BTAL, value, 0)
        replace_ieeenan(hgt_6_BTAL, value, 0)
        replace_ieeenan(hgt_7_BTAL, value, 0)
        replace_ieeenan(hgt_8_BTAL, value, 0)
    end if 

    hgt_1_BTAL@_FillValue = value
    hgt_2_BTAL@_FillValue = value
    hgt_3_BTAL@_FillValue = value
    hgt_4_BTAL@_FillValue = value
    hgt_5_BTAL@_FillValue = value
    hgt_6_BTAL@_FillValue = value
    hgt_7_BTAL@_FillValue = value
    hgt_8_BTAL@_FillValue = value

    hgt_1_climatology_BTAL = dim_avg_n_Wrap(hgt_1_BTAL, 0)
    hgt_2_climatology_BTAL = dim_avg_n_Wrap(hgt_2_BTAL, 0)
    hgt_3_climatology_BTAL = dim_avg_n_Wrap(hgt_3_BTAL, 0)
    hgt_4_climatology_BTAL = dim_avg_n_Wrap(hgt_4_BTAL, 0)
    hgt_5_climatology_BTAL = dim_avg_n_Wrap(hgt_5_BTAL, 0)
    hgt_6_climatology_BTAL = dim_avg_n_Wrap(hgt_6_BTAL, 0)
    hgt_7_climatology_BTAL = dim_avg_n_Wrap(hgt_7_BTAL, 0)
    hgt_8_climatology_BTAL = dim_avg_n_Wrap(hgt_8_BTAL, 0)

    ;printVarSummary(hgt_1_climatology)

    ; 3.1.2 Calculate the ensemble-mean clomatology data
    hgt_ensemble_climatology_BTAL = hgt_1_climatology_BTAL
    hgt_ensemble_climatology_BTAL = (hgt_1_climatology_BTAL + hgt_2_climatology_BTAL + hgt_3_climatology_BTAL + hgt_4_climatology_BTAL + hgt_5_climatology_BTAL + hgt_6_climatology_BTAL + hgt_7_climatology_BTAL + hgt_8_climatology_BTAL) / 8

    ; Climatology ensemble-mean hgt has got!

    ; 3.2 Calculate ensemble-average period-average for hgt
    hgt_ensemble_period_BTAL = hgt_1_climatology_BTAL
    hgt_ensemble_period_BTAL = (dim_avg_n_Wrap(hgt_1_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_2_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_3_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_4_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_5_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_6_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_7_BTAL({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_8_BTAL({period1:period2}, :, :, :), 0)) / 8

    zavar_BTAL = hgt_ensemble_period_BTAL - hgt_ensemble_climatology_BTAL ; This is the ght anomaly
    ; Period ensemble-mean averaged hgt has got!
    ; --------------------------------------------------------------- end BTAL ------------------------------------------------------------------------------

    ;----------------------------------------------------------------- BTALnEU --------------------------------------------------------------------------------
    ; 3.1 Calculate ensemble-average climatology for hgt
    hgt_1_BTALnEU   = f0_BTALnEU->JJAS_Z3_1
    hgt_2_BTALnEU   = f0_BTALnEU->JJAS_Z3_2
    hgt_3_BTALnEU   = f0_BTALnEU->JJAS_Z3_3
    hgt_4_BTALnEU   = f0_BTALnEU->JJAS_Z3_4
    hgt_5_BTALnEU   = f0_BTALnEU->JJAS_Z3_5
    hgt_6_BTALnEU   = f0_BTALnEU->JJAS_Z3_6
    hgt_7_BTALnEU   = f0_BTALnEU->JJAS_Z3_7
    hgt_8_BTALnEU   = f0_BTALnEU->JJAS_Z3_8

    ; 3.1.1 Replace the nan data
    if (any(isnan_ieee(hgt_1_BTALnEU))) then
        value = 1.e20
        replace_ieeenan(hgt_1_BTALnEU, value, 0)
        replace_ieeenan(hgt_2_BTALnEU, value, 0)
        replace_ieeenan(hgt_3_BTALnEU, value, 0)
        replace_ieeenan(hgt_4_BTALnEU, value, 0)
        replace_ieeenan(hgt_5_BTALnEU, value, 0)
        replace_ieeenan(hgt_6_BTALnEU, value, 0)
        replace_ieeenan(hgt_7_BTALnEU, value, 0)
        replace_ieeenan(hgt_8_BTALnEU, value, 0)
    end if 

    hgt_1_BTALnEU@_FillValue = value
    hgt_2_BTALnEU@_FillValue = value
    hgt_3_BTALnEU@_FillValue = value
    hgt_4_BTALnEU@_FillValue = value
    hgt_5_BTALnEU@_FillValue = value
    hgt_6_BTALnEU@_FillValue = value
    hgt_7_BTALnEU@_FillValue = value
    hgt_8_BTALnEU@_FillValue = value

    hgt_1_climatology_BTALnEU = dim_avg_n_Wrap(hgt_1_BTALnEU, 0)
    hgt_2_climatology_BTALnEU = dim_avg_n_Wrap(hgt_2_BTALnEU, 0)
    hgt_3_climatology_BTALnEU = dim_avg_n_Wrap(hgt_3_BTALnEU, 0)
    hgt_4_climatology_BTALnEU = dim_avg_n_Wrap(hgt_4_BTALnEU, 0)
    hgt_5_climatology_BTALnEU = dim_avg_n_Wrap(hgt_5_BTALnEU, 0)
    hgt_6_climatology_BTALnEU = dim_avg_n_Wrap(hgt_6_BTALnEU, 0)
    hgt_7_climatology_BTALnEU = dim_avg_n_Wrap(hgt_7_BTALnEU, 0)
    hgt_8_climatology_BTALnEU = dim_avg_n_Wrap(hgt_8_BTALnEU, 0)

    ;printVarSummary(hgt_1_climatology)

    ; 3.1.2 Calculate the ensemble-mean clomatology data
    hgt_ensemble_climatology_BTALnEU = hgt_1_climatology_BTALnEU
    hgt_ensemble_climatology_BTALnEU = (hgt_1_climatology_BTALnEU + hgt_2_climatology_BTALnEU + hgt_3_climatology_BTALnEU + hgt_4_climatology_BTALnEU + hgt_5_climatology_BTALnEU + hgt_6_climatology_BTALnEU + hgt_7_climatology_BTALnEU + hgt_8_climatology_BTALnEU) / 8

    ; Climatology ensemble-mean hgt has got!

    ; 3.2 Calculate ensemble-average period-average for hgt
    hgt_ensemble_period_BTALnEU = hgt_1_climatology_BTALnEU
    hgt_ensemble_period_BTALnEU = (dim_avg_n_Wrap(hgt_1_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_2_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_3_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_4_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_5_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_6_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_7_BTALnEU({period1:period2}, :, :, :), 0) + dim_avg_n_Wrap(hgt_8_BTALnEU({period1:period2}, :, :, :), 0)) / 8

    zavar_BTALnEU = hgt_ensemble_period_BTALnEU - hgt_ensemble_climatology_BTALnEU ; This is the ght anomaly
    ; Period ensemble-mean averaged hgt has got!
    ; --------------------------------------------------------------- end BTALnEU ------------------------------------------------------------------------------

    zavar  =  zavar_BTAL - zavar_BTALnEU
    ; 3.2 Calculate ensemble-average climatology for T, wind
    ; 3.2.1 T
    t_1   = f_air->JJAS_T_1
    t_2   = f_air->JJAS_T_2
    t_3   = f_air->JJAS_T_3
    t_4   = f_air->JJAS_T_4
    t_5   = f_air->JJAS_T_5
    t_6   = f_air->JJAS_T_6
    t_7   = f_air->JJAS_T_7
    t_8   = f_air->JJAS_T_8

    ; 3.2.2 Replace the nan data
    if (any(isnan_ieee(t_1))) then
        value = 1.e20
        replace_ieeenan(t_1, value, 0)
        replace_ieeenan(t_2, value, 0)
        replace_ieeenan(t_3, value, 0)
        replace_ieeenan(t_4, value, 0)
        replace_ieeenan(t_5, value, 0)
        replace_ieeenan(t_6, value, 0)
        replace_ieeenan(t_7, value, 0)
        replace_ieeenan(t_8, value, 0)
    end if 

    t_1@_FillValue = value
    t_2@_FillValue = value
    t_3@_FillValue = value
    t_4@_FillValue = value
    t_5@_FillValue = value
    t_6@_FillValue = value
    t_7@_FillValue = value
    t_8@_FillValue = value

    t_1_climatology = dim_avg_n_Wrap(t_1, 0)
    t_2_climatology = dim_avg_n_Wrap(t_2, 0)
    t_3_climatology = dim_avg_n_Wrap(t_3, 0)
    t_4_climatology = dim_avg_n_Wrap(t_4, 0)
    t_5_climatology = dim_avg_n_Wrap(t_5, 0)
    t_6_climatology = dim_avg_n_Wrap(t_6, 0)
    t_7_climatology = dim_avg_n_Wrap(t_7, 0)
    t_8_climatology = dim_avg_n_Wrap(t_8, 0)

    ;printVarSummary(hgt_1_climatology)

    ; 3.2.3 Calculate the ensemble-mean clomatology data
    t_ensemble_climatology = t_1_climatology
    t_ensemble_climatology = (t_1_climatology + t_2_climatology + t_3_climatology + t_4_climatology + t_5_climatology + t_6_climatology + t_7_climatology + t_8_climatology) / 8 - 273.15

    ;printMinMax(t_ensemble_climatology, 0)

    ; 3.3.1 U
    u_1   = f_u->JJAS_U_1
    u_2   = f_u->JJAS_U_2
    u_3   = f_u->JJAS_U_3
    u_4   = f_u->JJAS_U_4
    u_5   = f_u->JJAS_U_5
    u_6   = f_u->JJAS_U_6
    u_7   = f_u->JJAS_U_7
    u_8   = f_u->JJAS_U_8

    ; 3.3.2 Replace the nan data
    if (any(isnan_ieee(u_1))) then
        value = 1.e20
        replace_ieeenan(u_1, value, 0)
        replace_ieeenan(u_2, value, 0)
        replace_ieeenan(u_3, value, 0)
        replace_ieeenan(u_4, value, 0)
        replace_ieeenan(u_5, value, 0)
        replace_ieeenan(u_6, value, 0)
        replace_ieeenan(u_7, value, 0)
        replace_ieeenan(u_8, value, 0)
    end if 

    u_1@_FillValue = value
    u_2@_FillValue = value
    u_3@_FillValue = value
    u_4@_FillValue = value
    u_5@_FillValue = value
    u_6@_FillValue = value
    u_7@_FillValue = value
    u_8@_FillValue = value

    u_1_climatology = dim_avg_n_Wrap(u_1, 0)
    u_2_climatology = dim_avg_n_Wrap(u_2, 0)
    u_3_climatology = dim_avg_n_Wrap(u_3, 0)
    u_4_climatology = dim_avg_n_Wrap(u_4, 0)
    u_5_climatology = dim_avg_n_Wrap(u_5, 0)
    u_6_climatology = dim_avg_n_Wrap(u_6, 0)
    u_7_climatology = dim_avg_n_Wrap(u_7, 0)
    u_8_climatology = dim_avg_n_Wrap(u_8, 0)

    ;printVarSummary(hgt_1_climatology)

    ; 3.3.3 Calculate the ensemble-mean clomatology data
    u_ensemble_climatology = u_1_climatology
    u_ensemble_climatology = (u_1_climatology + u_2_climatology + u_3_climatology + u_4_climatology + u_5_climatology + u_6_climatology + u_7_climatology + u_8_climatology) / 8

    ; 3.4.1 V
    v_1   = f_v->JJAS_V_1
    v_2   = f_v->JJAS_V_2
    v_3   = f_v->JJAS_V_3
    v_4   = f_v->JJAS_V_4
    v_5   = f_v->JJAS_V_5
    v_6   = f_v->JJAS_V_6
    v_7   = f_v->JJAS_V_7
    v_8   = f_v->JJAS_V_8

    ; 3.4.2 Replace the nan data
    if (any(isnan_ieee(v_1))) then
        value = 1.e20
        replace_ieeenan(v_1, value, 0)
        replace_ieeenan(v_2, value, 0)
        replace_ieeenan(v_3, value, 0)
        replace_ieeenan(v_4, value, 0)
        replace_ieeenan(v_5, value, 0)
        replace_ieeenan(v_6, value, 0)
        replace_ieeenan(v_7, value, 0)
        replace_ieeenan(v_8, value, 0)
    end if 

    v_1@_FillValue = value
    v_2@_FillValue = value
    v_3@_FillValue = value
    v_4@_FillValue = value
    v_5@_FillValue = value
    v_6@_FillValue = value
    v_7@_FillValue = value
    v_8@_FillValue = value

    v_1_climatology = dim_avg_n_Wrap(v_1, 0)
    v_2_climatology = dim_avg_n_Wrap(v_2, 0)
    v_3_climatology = dim_avg_n_Wrap(v_3, 0)
    v_4_climatology = dim_avg_n_Wrap(v_4, 0)
    v_5_climatology = dim_avg_n_Wrap(v_5, 0)
    v_6_climatology = dim_avg_n_Wrap(v_6, 0)
    v_7_climatology = dim_avg_n_Wrap(v_7, 0)
    v_8_climatology = dim_avg_n_Wrap(v_8, 0)

    ;printVarSummary(hgt_1_climatology)

    ; 3.4.3 Calculate the ensemble-mean clomatology data
    v_ensemble_climatology = v_1_climatology
    v_ensemble_climatology = (v_1_climatology + v_2_climatology + v_3_climatology + v_4_climatology + v_5_climatology + v_6_climatology + v_7_climatology + v_8_climatology) / 8

    ; 4. Constant quantity
    ;  Gas constant
    gc=290
    ;  Gravitational acceleration
    ga=9.80665

    ;  Radius of the earth
    re=6378388

    ; scale height
    sclhgt=8000.

    ; pi
    pi = atan(1.0)*4.

    ; Coriolis parameter
    f =  2.*2.*pi/(60.*60.*24.)*sin(pi/180. * lat(:))
    f!0 = "lat"
    f&lat = lat
    f@_FillValue = value

    ;print(f)
    ;mask
    do ilat = 0, nlat-1
    if (abs(lat(ilat) ).lt. 10. ) then
    f(ilat)= f@_FillValue
    end if
    end do
    
    ; cosine
    coslat = cos(lat(:)*pi/180.)

    ; 1-D -> 4-D
    leveltmp = conform_dims(dimsizes(v_ensemble_climatology),level,0)
    coslattmp = conform_dims(dimsizes(v_ensemble_climatology),coslat,1)
    ftmp = conform_dims(dimsizes(v_ensemble_climatology),f,1)

    ; vertical gradient of potential temperature  (K/m)
    dthetadz = center_finite_diff_n(t_ensemble_climatology*(1000./leveltmp)^0.286, -sclhgt*log(level/1000), False, 0, 0) ; the last scalar indicates which dimension to execute center difference

    ; Brunt Vaisala frequency
    NN = (gc*(leveltmp/1000.)^0.286)/sclhgt * dthetadz
    NN@_FillValue = value
    NN = where(NN .gt. 0, NN, NN@_FillValue)

    ; magnitude of climatological wind
    cumag = sqrt(u_ensemble_climatology^2 + v_ensemble_climatology^2)
    cumag@_FillValue = value
    cumag = where(cumag .gt. 0, cumag, cumag@_FillValue)

    ; QG steam function for anomaly
    psidev = zavar*ga /ftmp

    ;dpsidev/dlon
    dpsidevdlon =  center_finite_diff_n(psidev,lon*pi/180.,True,0,2)

    ;ddpsidev/dlonlon
    ddpsidevdlonlon =  center_finite_diff_n(dpsidevdlon,lon*pi/180.,True,0,2)

    ;dpsidev/dlat
    dpsidevdlat = center_finite_diff_n(psidev, lat*pi/180., False,0,1)

    ;ddpsidev/dlonlat
    ddpsidevdlonlat =  center_finite_diff_n(dpsidevdlon,lat*pi/180.,False,0,1)

    ;ddpsidev/dlatdlat
    ddpsidevdlatlat = center_finite_diff_n(dpsidevdlat, lat*pi/180.,False,0,1)

    ;dpsidev/dz
    dpsidevdz = center_finite_diff_n(psidev, -sclhgt*log(level/1000),False,0,0)

    ;ddpsidev/dlondz
    ddpsidevdlonz = center_finite_diff_n(dpsidevdlon, -sclhgt*log(level/1000),False,0,0)

    ;ddpsidev/dlatdz
    ddpsidevdlatz = center_finite_diff_n(dpsidevdlat, -sclhgt*log(level/1000),False,0,0)

    xuterm = (dpsidevdlon*dpsidevdlon - psidev*ddpsidevdlonlon)
    xvterm = (dpsidevdlon*dpsidevdlat - psidev*ddpsidevdlonlat)
    ;yuterm = xvterm
    yvterm = (dpsidevdlat*dpsidevdlat - psidev*ddpsidevdlatlat)

    zuterm = (dpsidevdlon*dpsidevdz - psidev*ddpsidevdlonz)
    zvterm = (dpsidevdlat*dpsidevdz - psidev*ddpsidevdlatz)

    ; Mask out where westerlies is small or negative (less than 5 m/s).
    ;  by using mask
    
    ;x-component of (38)
    Fx = mask( leveltmp/1000./(2.*cumag*re*re)*( u_ensemble_climatology/coslattmp * xuterm + v_ensemble_climatology * xvterm), u_ensemble_climatology.lt.5,False)
    
    ;y-component 
    Fy = mask(leveltmp/1000./(2.*cumag*re*re)*( u_ensemble_climatology*xvterm + coslattmp*v_ensemble_climatology*yvterm),  u_ensemble_climatology.lt.5,False)
    
    ;z-component 
    Fz = mask(leveltmp/1000.*ftmp*ftmp/(2.*cumag*NN*re)*(u_ensemble_climatology*zuterm + coslattmp*v_ensemble_climatology*zvterm), u_ensemble_climatology.lt.5, False)

    ; for output
    Fx!0 = "level"
    Fx&level = level
    Fx!1 = "lat"
    Fx&lat = lat
    Fx!2 = "lon"
    Fx&lon = lon

    Fy!0 = "level"
    Fy&level = level
    Fy!1 = "lat"
    Fy&lat = lat
    Fy!2 = "lon"
    Fy&lon = lon

    Fz!0 = "level"
    Fz&level = level
    Fz!1 = "lat"
    Fz&lat = lat
    Fz!2 = "lon"
    Fz&lon = lon

    psidev!0 = "level"
    psidev&level = level
    psidev!1 = "lat"
    psidev&lat = lat
    psidev!2 = "lon"
    psidev&lon = lon

    NN!0 = "level"
    NN&level = level
    NN!1 = "lat"
    NN&lat = lat
    NN!2 = "lon"
    NN&lon = lon

    Fx@units = "m^2/s^2"
    Fx@units = "m^2/s^2"
    Fz@units = "m^2/s^2"

    psidev@units = "m^2/s"

    NN@units = "1/s^2"

    outpath =  "/Volumes/samssd/data/wave_activity/"
    ncFx =     addfile(outpath + "BTAL_BTALnEU_diff_Z3_for_TN2001-Fx.monthly.period2.nc","c")
    ncFy =     addfile(outpath + "BTAL_BTALnEU_diff_Z3_for_TN2001-Fy.monthly.period2.nc","c")
    ncFz =     addfile(outpath + "BTAL_BTALnEU_diff_Z3_for_TN2001-Fz.monthly.period2.nc","c")
    ncpsidev = addfile(outpath + "BTAL_BTALnEU_diff_Z3_for_psidev.monthly.period2.nc","c")
    ncNN =     addfile(outpath + "BTAL_BTALnEU_diff_Z3_for_NN.monthly.period2.nc","c")

    ncFx->Fx = Fx
    ncFy->Fy = Fy
    ncFz->Fz = Fz
    ncpsidev->psidev = psidev

    ncNN->NN = NN
end
