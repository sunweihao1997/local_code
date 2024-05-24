; 2024-5-23
; This script is to calculate the water transportation, its divergence and vertical integrity
begin

    path_ua = "/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/"
    path_va = "/home/sun/wd_disk/AerChemMIP/download/mon_va_cat/"
    path_sh = "/home/sun/wd_disk/AerChemMIP/download/mon_hus_cat/"

    out_path= "/home/sun/data/AerChemMIP/process/moisture_transportation/"

    files_string = systemfunc("ls " + path_ua)

    scale_sp     = 1000 ; it transform g/g to g/kg

    do i = 32, 37
        filename0_ua = files_string(i)
        filename0_va = str_sub_str(filename0_ua, "ua_", "va_")
        filename0_sh = str_sub_str(filename0_ua, "ua_", "hus_")

        print("Now it is dealing with " + filename0_ua)
        ; Read the file for each ua, va, hus file
        fu = addfile(path_ua + filename0_ua, "r")
        fv = addfile(path_va + filename0_va, "r")
        fs = addfile(path_sh + filename0_sh, "r")

        u  = fu->ua
        v  = fv->va
        sh = fs->hus

        ; Calculation for water transportation
        printVarSummary(u)
        printVarSummary(sh)
        uq = u * sh * scale_sp
        vq = v * sh * scale_sp

        ;printVarSummary(uq)

        ; Calculation for divergence of the water transportation
        div_q = uv2dv_cfd(uq, vq, u&lat, u&lon, 2)

        ; Calculation for vertical integration
        ; copy coordination
        copy_VarCoords(u, uq)
        copy_VarCoords(u, vq)
        copy_VarCoords(u, div_q)

        ; Write to ncfile
        outname = str_sub_str(filename0_ua, "ua_", "mt_")

        fout = addfile(out_path + outname, "c")
        filedimdef(fout,"time",-1,True)
    ;
        fout->uq  = uq
        fout->vq  = vq
        fout->div_q = div_q
    ;
        ;; Set file attribute
        setfileoption(fout,"DefineMode",True)
        fAtt = True
        fAtt@description = "Create on 23/May/2024. This file is water transportation and its divergence"
        fileattdef(fout,fAtt)

        print("Successfully completed " + outname)

        delete(fu)
        delete(fv)
        delete(fs)
        delete(u)
        delete(v)
        delete(sh)
        delete(uq)
        delete(vq)
        delete(div_q)
        delete(fout)



    end do

end