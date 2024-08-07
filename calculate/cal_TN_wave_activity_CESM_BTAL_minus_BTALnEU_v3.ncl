;2023-11-30
;This script is to calculate TN wave activity flux

begin

    ; path_src = "/exports/csce/datastore/geos/users/s2618078/data/model_data/ensemble_JJAS/"
    path_src = "/Volumes/samssd/data/ensemble_JJAS/"

    ; 1. monthly-mean data hgt units:m
    f0       = addfile(path_src + "CESM_BTALnEU_JJAS_Z3_ensemble.nc", "r")

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

    ; 3. Data pre-process
    ; 3.1 Calculate ensemble-average climatology for hgt
    hgt_1   = f0->JJAS_Z3_1
    hgt_2   = f0->JJAS_Z3_2
    hgt_3   = f0->JJAS_Z3_3
    hgt_4   = f0->JJAS_Z3_4
    hgt_5   = f0->JJAS_Z3_5
    hgt_6   = f0->JJAS_Z3_6
    hgt_7   = f0->JJAS_Z3_7
    hgt_8   = f0->JJAS_Z3_8

    ; 3.1.1 Replace the nan data
    if (any(isnan_ieee(hgt_1))) then
        value = 1.e20
        replace_ieeenan(hgt_1, value, 0)
        replace_ieeenan(hgt_2, value, 0)
        replace_ieeenan(hgt_3, value, 0)
        replace_ieeenan(hgt_4, value, 0)
        replace_ieeenan(hgt_5, value, 0)
        replace_ieeenan(hgt_6, value, 0)
        replace_ieeenan(hgt_7, value, 0)
        replace_ieeenan(hgt_8, value, 0)
    end if 

    hgt_1@_FillValue = value
    hgt_2@_FillValue = value
    hgt_3@_FillValue = value
    hgt_4@_FillValue = value
    hgt_5@_FillValue = value
    hgt_6@_FillValue = value
    hgt_7@_FillValue = value
    hgt_8@_FillValue = value

    hgt_1_climatology = hgt_1
    hgt_2_climatology = hgt_2
    hgt_3_climatology = hgt_3
    hgt_4_climatology = hgt_4
    hgt_5_climatology = hgt_5
    hgt_6_climatology = hgt_6
    hgt_7_climatology = hgt_7
    hgt_8_climatology = hgt_8

    ;printVarSummary(hgt_1_climatology)

    ; 3.1.2 Calculate the ensemble-mean clomatology data
    hgt_ensemble_climatology = hgt_1_climatology
    hgt_ensemble_climatology = (hgt_1_climatology + hgt_2_climatology + hgt_3_climatology + hgt_4_climatology + hgt_5_climatology + hgt_6_climatology + hgt_7_climatology + hgt_8_climatology) / 8

    ; Climatology ensemble-mean hgt has got!

    ; 3.2 Calculate ensemble-average period-average for hgt
    hgt_ensemble_period = hgt_1_climatology


    ;printVarSummary(dim_avg_n_Wrap(hgt_ensemble_climatology, 0))
    zavar = hgt_ensemble_period
    zavar = hgt_ensemble_period - conform_dims(dimsizes(hgt_ensemble_period),dim_avg_n_Wrap(hgt_ensemble_climatology, 0),(/1,2,3/))
    ;printVarSummary(zavar)



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

    t_1_climatology = t_1
    t_2_climatology = t_2
    t_3_climatology = t_3
    t_4_climatology = t_4
    t_5_climatology = t_5
    t_6_climatology = t_6
    t_7_climatology = t_7
    t_8_climatology = t_8

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

    u_1_climatology = u_1
    u_2_climatology = u_2
    u_3_climatology = u_3
    u_4_climatology = u_4
    u_5_climatology = u_5
    u_6_climatology = u_6
    u_7_climatology = u_7
    u_8_climatology = u_8

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

    v_1_climatology = v_1
    v_2_climatology = v_2
    v_3_climatology = v_3
    v_4_climatology = v_4
    v_5_climatology = v_5
    v_6_climatology = v_6
    v_7_climatology = v_7
    v_8_climatology = v_8

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
    printVarSummary(v_ensemble_climatology)
    leveltmp = conform_dims(dimsizes(v_ensemble_climatology),level,1)
    coslattmp = conform_dims(dimsizes(v_ensemble_climatology),coslat,2)
    ftmp = conform_dims(dimsizes(v_ensemble_climatology),f,2)

    ; vertical gradient of potential temperature  (K/m)
    dthetadz = center_finite_diff_n(t_ensemble_climatology*(1000./leveltmp)^0.286, -sclhgt*log(level/1000), False, 0, 1) ; the last scalar indicates which dimension to execute center difference

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
    dpsidevdlon =  center_finite_diff_n(psidev,lon*pi/180.,True,0,3)

    ;ddpsidev/dlonlon
    ddpsidevdlonlon =  center_finite_diff_n(dpsidevdlon,lon*pi/180.,True,0,3)

    ;dpsidev/dlat
    dpsidevdlat = center_finite_diff_n(psidev, lat*pi/180., False,0,2)

    ;ddpsidev/dlonlat
    ddpsidevdlonlat =  center_finite_diff_n(dpsidevdlon,lat*pi/180.,False,0,2)

    ;ddpsidev/dlatdlat
    ddpsidevdlatlat = center_finite_diff_n(dpsidevdlat, lat*pi/180.,False,0,2)

    ;dpsidev/dz
    dpsidevdz = center_finite_diff_n(psidev, -sclhgt*log(level/1000),False,0,1)

    ;ddpsidev/dlondz
    ddpsidevdlonz = center_finite_diff_n(dpsidevdlon, -sclhgt*log(level/1000),False,0,1)

    ;ddpsidev/dlatdz
    ddpsidevdlatz = center_finite_diff_n(dpsidevdlat, -sclhgt*log(level/1000),False,0,1)

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

    ;exit
    ; for output
    Fx!0 = "time"
    Fx&time = time
    Fx!1 = "level"
    Fx&level = level
    Fx!2 = "lat"
    Fx&lat = lat
    Fx!3 = "lon"
    Fx&lon = lon

    Fy!0 = "time"
    Fy&time = time
    Fy!1 = "level"
    Fy&level = level
    Fy!2 = "lat"
    Fy&lat = lat
    Fy!3 = "lon"
    Fy&lon = lon

    Fz!0 = "time"
    Fz&time = time
    Fz!1 = "level"
    Fz&level = level
    Fz!2 = "lat"
    Fz&lat = lat
    Fz!3 = "lon"
    Fz&lon = lon

    ; Compute the divergence
    div_wave = Fx
    div_wave = uv2dv_cfd(Fx, Fy, lat, lon, 2)

    psidev!0 = "time"
    psidev&time = time
    psidev!1 = "level"
    psidev&level = level
    psidev!2 = "lat"
    psidev&lat = lat
    psidev!3 = "lon"
    psidev&lon = lon

    NN!0 = "time"
    NN&time = time
    NN!1 = "level"
    NN&level = level
    NN!2 = "lat"
    NN&lat = lat
    NN!3 = "lon"
    NN&lon = lon


    Fx@units = "m^2/s^2"
    Fx@units = "m^2/s^2"
    Fz@units = "m^2/s^2"

    psidev@units = "m^2/s"

    NN@units = "1/s^2"

    outpath =  "/Volumes/samssd/data/wave_activity/"
    ncFx =     addfile(outpath + "BTALnEU_TN2001-Fx.monthly.157year_jjas.nc","c")
    ncFy =     addfile(outpath + "BTALnEU_TN2001-Fy.monthly.157year_jjas.nc","c")
    ncFz =     addfile(outpath + "BTALnEU_TN2001-Fz.monthly.157year_jjas.nc","c")
    ncpsidev = addfile(outpath + "BTALnEU_psidev.monthly.157year_jjas.nc","c")
    ncNN =     addfile(outpath + "BTALnEU_NN.monthly.157year_jjas.nc","c")

    ncFx->Fx = Fx
    ncFy->Fy = Fy
    ncFz->Fz = Fz
    ncFz->div=div_wave
    ncpsidev->psidev = psidev

    ncNN->NN = NN
end
