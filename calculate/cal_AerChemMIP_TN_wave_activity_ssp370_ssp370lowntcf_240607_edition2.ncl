;2024-6-7
;This script is to calculate TN wave activity flux for SSP370 and SSP370lowNTCF

; Following Liu advice, I calculate geopotential height anomaly first and then calculate wave activity

begin

    ; 1. monthly-mean data hgt units:m
    f0            = addfile("/home/sun/data/AerChemMIP/process/multiple_modelmean_climate_utvz_month_MJJAS.nc", "r")

    ; 2. monthly climatology data
    ; 2.1 hgt could use f0
    z_ssp      = f0->z_diff
    z_ntcf     = f0->z_ntcf

    ; u
    u_ssp      = f0->u_ssp
    u_ntcf     = f0->u_ntcf


    ; v
    v_ssp      = f0->v_ssp
    v_ntcf     = f0->v_ntcf


    ; t
    t_ssp      = f0->t_ssp
    t_ntcf     = f0->t_ntcf


    ; dimension information
    lat  = f0->lat
    lon  = f0->lon
    level= f0->lev ; units: hPa
    level= level/100

    nlat = dimsizes(lat)
    nlon = dimsizes(lon)
    nlev = dimsizes(level)
    

    ; 3. Replace the NAN data
    value = 1.e20
    replace_ieeenan(z_ssp,  value, 0)
    replace_ieeenan(z_ntcf, value, 0)
    replace_ieeenan(u_ssp,  value, 0)
    replace_ieeenan(u_ntcf, value, 0)
    replace_ieeenan(t_ssp,  value, 0)
    replace_ieeenan(t_ntcf, value, 0)
    replace_ieeenan(v_ssp,  value, 0)
    replace_ieeenan(v_ntcf, value, 0)
    z_ssp@_FillValue       = value
    z_ntcf@_FillValue      = value
    u_ssp@_FillValue       = value
    u_ntcf@_FillValue      = value
    t_ssp@_FillValue       = value
    t_ntcf@_FillValue      = value
    v_ssp@_FillValue       = value
    v_ntcf@_FillValue      = value

    zavar = z_ssp
    copy_VarCoords(z_ssp, zavar)



    ; ============== Start calculating WAF ==================
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

    ; 1-D -> 3-D
    leveltmp  = conform_dims(dimsizes(v_ssp), level, 0)
    coslattmp = conform_dims(dimsizes(v_ssp), coslat,1)
    ftmp      = conform_dims(dimsizes(v_ssp), f, 1)


    ; vertical gradient of potential temperature  (K/m)
    dthetadz_ssp  = center_finite_diff_n(t_ssp*(1000./leveltmp)^0.286,  -sclhgt*log(level/1000), False, 0, 0) ; the last scalar indicates which dimension to execute center difference
    dthetadz_ntcf = center_finite_diff_n(t_ntcf*(1000./leveltmp)^0.286, -sclhgt*log(level/1000), False, 0, 0) ; the last scalar indicates which dimension to execute center difference
    

    ; Brunt Vaisala frequency
    NN_ssp = (gc*(leveltmp/1000.)^0.286)/sclhgt * dthetadz_ssp
    NN_ssp@_FillValue = value
    NN_ssp = where(NN_ssp .gt. 0, NN_ssp, NN_ssp@_FillValue)

    NN_ntcf = (gc*(leveltmp/1000.)^0.286)/sclhgt * dthetadz_ntcf
    NN_ntcf@_FillValue = value
    NN_ntcf = where(NN_ntcf .gt. 0, NN_ntcf, NN_ntcf@_FillValue)

    ; magnitude of climatological wind
    cumag_ssp = sqrt(u_ssp^2 + v_ssp^2)
    cumag_ssp@_FillValue = value
    cumag_ssp = where(cumag_ssp .gt. 0, cumag_ssp, cumag_ssp@_FillValue)

    cumag_ntcf = sqrt(u_ntcf^2 + v_ntcf^2)
    cumag_ntcf@_FillValue = value
    cumag_ntcf = where(cumag_ntcf .gt. 0, cumag_ntcf, cumag_ntcf@_FillValue)



    ; QG steam function for anomaly
    psidev = zavar * ga / ftmp

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
    Fx = mask( leveltmp/1000./(2.*cumag_ssp*re*re)*( u_ssp/coslattmp * xuterm + v_ssp * xvterm), u_ssp.lt.5,False)
    
    ;y-component 
    Fy = mask( leveltmp/1000./(2.*cumag_ssp*re*re)*( u_ssp*xvterm + coslattmp*v_ssp*yvterm),     u_ssp.lt.5,False)
    
    ;z-component 
    Fz = mask(leveltmp/1000.*ftmp*ftmp/(2.*cumag_ssp*NN_ssp*re)*(u_ssp*zuterm + coslattmp*v_ssp*zvterm), u_ssp.lt.5, False)

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
;
;    NN!0 = "level"
;    NN&level = level
;    NN!1 = "lat"
;    NN&lat = lat
;    NN!2 = "lon"
;    NN&lon = lon

    Fx@units = "m^2/s^2"
    Fx@units = "m^2/s^2"
    Fz@units = "m^2/s^2"

    psidev@units = "m^2/s"
;
;    NN@units = "1/s^2"

    outpath =  "/home/sun/data/AerChemMIP/process/"
    system("rm -rf " + outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fx.MJJAS.nc")
    system("rm -rf " + outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fy.MJJAS.nc")
    system("rm -rf " + outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fz.MJJAS.nc")
    system("rm -rf " + outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-psidev.MJJAS.nc")

    ncFx =     addfile(outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fx.MJJAS.nc","c")
    ncFy =     addfile(outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fy.MJJAS.nc","c")
    ncFz =     addfile(outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-Fz.MJJAS.nc","c")
    ncpsidev =     addfile(outpath + "AerChemMIP_SSP370_SSP370lowNTCF_diff_Z3_for_TN2001-psidev.MJJAS.nc","c")

    ncFx->Fx = Fx
    ncFy->Fy = Fy
    ncFz->Fz = Fz
    ncpsidev->psidev = psidev
;
;    ncNN->NN = NN
end
