; 2024-5-22
; This script is to calculate the 200hPa divergence and divergent wind and then save to the file
; This is for comparison purpose with script cal_AerChemMIP_200_divergence_240522.py
begin

    path_ua = "/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/"
    path_va = "/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/"

    out_path= "/home/sun/data/AerChemMIP/process/200_rws_ncl/"

    files_string = systemfunc("ls " + path_ua)

    level = 30000
    ;print(files_string(1))
    do i = 0, 37
        filename0_ua = files_string(i)
        filename0_va = str_sub_str(filename0_ua, "ua_", "va_")

        ;read the file for each ua/va file
        fu = addfile(path_ua + filename0_ua, "r")
        fv = addfile(path_va + filename0_va, "r")

        u  = fu->ua(:, {level}, :, :)
        v  = fv->va(:, {level}, :, :)

        ; divergence
        div = uv2dv_cfd(u, v, u&lat, u&lon, 2)

        copy_VarCoords(u, div)

        ;printVarSummary(div)
        dv  = dv2uvF_Wrap(div)

        ; divergent wind
        divu= dv(0, :, :, :)
        divv= dv(1, :, :, :)

        copy_VarCoords(u, divu)
        copy_VarCoords(v, divv)
        ;printVarSummary(divu)

        ; absolute vorticity
        rel_vorticity = uv2vr_cfd(u, v, u&lat, u&lon, 2)

        omega = 7.2921e-5   ; 地球的角速度 (rad/s)
        f0 = 2 * omega * sin(u&lat * 0.017453292519943295)  ; 将纬度从度转换为弧度

        ;print(dimsizes(rel_vorticity))
        ;print(f)
        f = conform_dims(dimsizes(rel_vorticity), f0, 1)

        abs_vorticity = rel_vorticity + f

        abs_vorticity_gradient = grad_latlon_cfd(abs_vorticity, u&lat, u&lon, True, False)

        ; RWS
        rws = -1 * abs_vorticity * div - (divv*abs_vorticity_gradient[0] + divu*abs_vorticity_gradient[1])

        copy_VarCoords(u, rws)
        copy_VarCoords(u, abs_vorticity)

        ; Save to the ncfile
        outname = str_sub_str(filename0_ua, "ua_", "rws_")
        ;system("rm " + out_path + outname)
        fout = addfile(out_path + outname, "c")
        filedimdef(fout,"time",-1,True)
    ;
        fout->div  = div
        fout->divu = divu
        fout->divv = divv
        fout->avor = abs_vorticity
        fout->rws  = rws
    ;
        ;; Set file attribute
        setfileoption(fout,"DefineMode",True)
        fAtt = True
        fAtt@description = "Create on 9/June/2024. This file is 300 hPa divergence and divergent wind."
        fileattdef(fout,fAtt)

        print("Successfully completed " + outname)

        delete(fu)
        delete(fv)
        delete(u)
        delete(v)
        delete(div)
        delete(divu)
        delete(divv)
        delete(dv)
        delete(fout)
        delete(rel_vorticity)
        delete(f)
        delete(f0)
        delete(abs_vorticity)
        delete(abs_vorticity_gradient)
        delete(rws)

    end do

end