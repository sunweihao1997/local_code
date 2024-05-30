; 2024-5-28
; This script is to use the ncl function to calculate the vertical integral of the moisture transportation
begin

    f0 = addfile("/home/sun/data/AerChemMIP/process/modelmean_climate_hus_ua_va_ps_month_MJJAS.nc", "r")

    u_ssp    = f0->ssp_ua
    v_ssp    = f0->ssp_va
    hus_ssp  = f0->ssp_hus
    ps_ssp   = f0->ssp_ps

    u_ntcf    = f0->ntcf_ua
    v_ntcf    = f0->ntcf_va
    hus_ntcf  = f0->ntcf_hus
    ps_ntcf   = f0->ntcf_ps

    lon       = f0->lon
    lat       = f0->lat
    lev       = f0->lev

    ;print(lev(:20))
    ; remove the NaN with FillValue
    if (any(isnan_ieee(u_ssp))) then
        print("Include NAN!")
        value = 1.e20
        replace_ieeenan(u_ssp   , value, 0)
        replace_ieeenan(v_ssp   , value, 0)
        replace_ieeenan(hus_ssp , value, 0)
        replace_ieeenan(ps_ssp  , value, 0)
        replace_ieeenan(u_ntcf  , value, 0)
        replace_ieeenan(v_ntcf  , value, 0)
        replace_ieeenan(hus_ntcf, value, 0)
        replace_ieeenan(ps_ntcf , value, 0)
        u_ssp@_FillValue      = value
        v_ssp@_FillValue      = value
        hus_ssp@_FillValue    = value
        ps_ssp@_FillValue     = value
        u_ntcf@_FillValue     = value
        v_ntcf@_FillValue     = value
        hus_ntcf@_FillValue   = value
        ps_ntcf@_FillValue    = value
    end if

    ;printMinMax(ps_ssp, 0)
    ;print(lev)
    ; --------- Calculate the moisture transportation on single level ---------------
    uq_ssp  = u_ssp * hus_ssp / 9.8
    vq_ssp  = v_ssp * hus_ssp / 9.8
    uq_ntcf = u_ntcf * hus_ntcf / 9.8
    vq_ntcf = v_ntcf * hus_ntcf / 9.8

    div_ssp  = uv2dv_cfd(uq_ssp,  vq_ssp,  lat, lon, 2)
    div_ntcf = uv2dv_cfd(uq_ntcf, vq_ntcf, lat, lon, 2)

    printMinMax(hus_ntcf, 0)

    ;printMinMax(div_ntcf, 0)

    ; -------- Calculate the vertical integral ---------
    vert_integral_ssp  = new((/91, 180/), double)
    vert_integral_ntcf = new((/91, 180/), double)

    pbot   = 100000
    ptop   = 30000
    do latt = 0, 90
        do lonn = 0, 179
            if ismissing(div_ssp(15, latt, lonn)) then 
                ;print("Continue")
                vert_integral_ssp(latt, lonn)  = 0
                vert_integral_ntcf(latt, lonn) = 0
            else
                ;print(ps_ssp(latt, lonn))
                ;print(div_ssp(:, latt, lonn))
                vert_integral_ssp(latt, lonn)  = vibeta(lev, div_ssp(:, latt, lonn),  1, ps_ssp(latt, lonn),  pbot, ptop)
                vert_integral_ntcf(latt, lonn) = vibeta(lev, div_ntcf(:, latt, lonn), 1, ps_ntcf(latt, lonn), pbot, ptop)
            end if
        end do
    end do

    copy_VarCoords(ps_ssp, vert_integral_ssp)
    copy_VarCoords(ps_ssp, vert_integral_ntcf)

    ; Write to ncfile
    system("rm -rf /home/sun/data/AerChemMIP/process/modelmean_climate_water_transportation_integral_MJJAS.nc")
    fout = addfile("/home/sun/data/AerChemMIP/process/modelmean_climate_water_transportation_integral_MJJAS.nc", "c")
    filedimdef(fout,"time",-1,True)
;
    fout->vert_integral_ssp  = vert_integral_ssp
    fout->vert_integral_ntcf  = vert_integral_ntcf

;
    ;; Set file attribute
    setfileoption(fout,"DefineMode",True)
    fAtt = True
    fAtt@description = "Create on 28/May/2024. This file is water transportation vertical integral"
    fileattdef(fout,fAtt)

    
end