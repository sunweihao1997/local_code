; 2024-5-7
; This script is calculate the regression to the pc1 for uas under 3 scenarios

begin
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================
    ; uas data
    varname=(/"uas", "vas", "psl", "rlut"/)

    do i = 0, 3
    fname = "/home/sun/data/process/analysis/AerChem/" + varname(i) + "_MJJAS_multiple_model_result.nc"
    f0 = addfile(fname, "r")
    ; PC1
    f1 = addfile("/home/sun/data/process/analysis/AerChem/AerchemMIP_Asia_EOF_land_summertime_8-20_precipitation_hist_SSP370_NTCF.nc", "r")

    ; Read data
    ; uas
    uas_hist = f0->hist_model
    uas_ssp3 = f0->ssp3_model
    uas_ntcf = f0->ntcf_model

    ; pcs
    pc_hist  = f1->pc_hist
    pc_ssp3  = f1->pc_ssp3
    pc_ntcf  = f1->pc_ntcf


    ; Delete NAN value
    if (any(isnan_ieee(uas_hist))) then
        value = 1.e20
        replace_ieeenan(uas_hist, value, 0)
        replace_ieeenan(uas_ssp3, value, 0)
        replace_ieeenan(uas_ntcf, value, 0)
        uas_hist@_FillValue = value
        uas_ssp3@_FillValue = value
        uas_ntcf@_FillValue = value
    end if

    ; Calculates model mean and removes the mean in time axis of the given dimension(s) at all other dimensions.
    uas_hist_abnormal = dim_avg_n_Wrap(uas_hist, 0)
    uas_hist_abnormal = dim_rmvmean_n_Wrap(uas_hist_abnormal, 0)

    uas_ssp3_abnormal = dim_avg_n_Wrap(uas_ssp3, 0)
    uas_ssp3_abnormal = dim_rmvmean_n_Wrap(uas_ssp3_abnormal, 0)

    uas_ntcf_abnormal = dim_avg_n_Wrap(uas_ntcf, 0)
    uas_ntcf_abnormal = dim_rmvmean_n_Wrap(uas_ntcf_abnormal, 0)
    ;printVarSummary(uas_hist_abnormal)
    




    ;=================================================
    ; ================ Data processing1: abnormal, detrend, calculate monthly mean =======================

    ; ================ Data processing2: calculate regression =======================
    ;printVarSummary(u_detrend)
    ;printVarSummary(lstc_detrend_april)

    do lag=0, 12, 1
        N_hist   = dimsizes(pc_hist(:, 0))
        N_furt   = dimsizes(pc_ssp3(:, 0))

        rc_uas_hist = regCoef_n(pc_hist(12:N_hist(0) - 1 - 12, 0), uas_hist_abnormal(0 + (2 * lag):N_hist(0) - 24 - 1 + (2 * lag), :, :), 0, 0)  
        rc_uas_ssp3 = regCoef_n(pc_ssp3(12:N_furt(0) - 1 - 12, 0), uas_ssp3_abnormal(0 + (2 * lag):N_furt(0) - 24 - 1 + (2 * lag), :, :), 0, 0)  
        rc_uas_ntcf = regCoef_n(pc_ntcf(12:N_furt(0) - 1 - 12, 0), uas_ntcf_abnormal(0 + (2 * lag):N_furt(0) - 24 - 1 + (2 * lag), :, :), 0, 0)  

        ; Delete irrelevant attributes
        delete(rc_uas_hist@nptxy)
        delete(rc_uas_hist@rstd)
        delete(rc_uas_hist@yintercept)
        delete(rc_uas_hist@tval)
        delete(rc_uas_ssp3@nptxy)
        delete(rc_uas_ssp3@rstd)
        delete(rc_uas_ssp3@yintercept)
        delete(rc_uas_ssp3@tval)
        delete(rc_uas_ntcf@nptxy)
        delete(rc_uas_ntcf@rstd)
        delete(rc_uas_ntcf@yintercept)
        delete(rc_uas_ntcf@tval)

;        rc_uas_hist_squeeze = rm_single_dims(rc_uas_hist)
;        rc_uas_ssp3_squeeze = rm_single_dims(rc_uas_ssp3)
;        rc_uas_ntcf_squeeze = rm_single_dims(rc_uas_ntcf)
;
;        copy_VarCoords(uas_hist(0, 0, :, :), rc_uas_hist_squeeze)
;        copy_VarCoords(uas_ntcf(0, 0, :, :), rc_uas_ssp3_squeeze)
;        copy_VarCoords(uas_ntcf(0, 0, :, :), rc_uas_ntcf_squeeze)

        ; ================ Write to the nc file ==========================================
        system("rm /home/sun/data/process/analysis/AerChem/regression_v2_"+varname(i)+"_to_8to20_pc1_lag"+lag+"_hist_ssp_ntcf.nc")
        outname = "/home/sun/data/process/analysis/AerChem/regression_v2_"+varname(i)+"_to_8to20_pc1_lag"+lag+"_hist_ssp_ntcf.nc"
        fout = addfile(outname, "c")
        filedimdef(fout,"time",-1,True)
    ;
        fout->rc_uas_hist = rc_uas_hist
        fout->rc_uas_ssp3 = rc_uas_ssp3
        fout->rc_uas_ntcf = rc_uas_ntcf
    ;
        ;; Set file attribute
        setfileoption(fout,"DefineMode",True)
        fAtt = True
        fAtt@description = "Create on 7/5/2023. This file include regression from "+varname(i)+" to the PC1 for 8-20 band-pass."
        fileattdef(fout,fAtt)

        print("Successfully completed " + lag)
    end do

    delete(uas_hist)
    delete(uas_ssp3)
    delete(uas_ntcf)
    delete(pc_hist)
    delete(pc_ssp3)
    delete(pc_ntcf)

    end do

end
