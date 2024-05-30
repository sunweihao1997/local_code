; 2024-5-22
; This script is to calculate the 200hPa divergence and divergent wind and then save to the file
; This is for comparison purpose with script cal_AerChemMIP_200_divergence_240522.py
begin

    path_ua = "/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/"
    path_va = "/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/"

    out_path= "/home/sun/data/AerChemMIP/process/200_div_ncl/"

    files_string = systemfunc("ls " + path_ua)

    level = 20000
    ;print(files_string(1))
    do i = 10, 10
        filename0_ua = files_string(i)
        filename0_va = str_sub_str(filename0_ua, "ua_", "va_")

        ;read the file for each ua/va file
        fu = addfile(path_ua + filename0_ua, "r")
        fv = addfile(path_va + filename0_va, "r")

        u  = fu->ua(:, {level}, :, :)
        v  = fv->va(:, {level}, :, :)

        div = uv2dv_cfd(u, v, u&lat, u&lon, 2)

        sf0 = uv2sfvpF(u, v)

        copy_VarCoords(u, div)

        ;printVarSummary(div)
        dv  = dv2uvF_Wrap(div)

        divu= dv(0, :, :, :)
        divv= dv(1, :, :, :)

        copy_VarCoords(u, divu)
        copy_VarCoords(v, divv)
        ;printVarSummary(divu)

        sf  = sf0(0, :, :, :)
        copy_VarCoords(u, sf)

        print(sf)

        ; Save to the ncfile
        outname = str_sub_str(filename0_ua, "ua_", "div_")
        system("rm " + out_path + outname)
        fout = addfile(out_path + outname, "c")
        filedimdef(fout,"time",-1,True)
    ;
        fout->div  = div
        fout->divu = divu
        fout->divv = divv
        fout->sf   = sf
    ;
        ;; Set file attribute
        setfileoption(fout,"DefineMode",True)
        fAtt = True
        fAtt@description = "Create on 22/May/2024. This file is 200 hPa divergence and divergent wind."
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
        delete(sf)
        delete(sf0)

    end do

end