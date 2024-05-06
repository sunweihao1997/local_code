; 2024-4-29
; This script is for the test purpose to do power spectrum analysis for single file

begin

    data_path = "/home/sun/data/process/analysis/AerChem/regional_pr_MJJAS_v2/"
    f0 = addfile(data_path + "multiple_model_result.nc", "r")

    ;print(f0)
    prect_sa_m  = f0->hist_model(:, 0, :)
    prect_id_m  = f0->hist_model(:, 1, :)
    prect_ea_m  = f0->hist_model(:, 2, :)

    prect_sa    = dim_avg_n_Wrap(prect_sa_m, 0)
    prect_id    = dim_avg_n_Wrap(prect_id_m, 0)
    prect_ea    = dim_avg_n_Wrap(prect_ea_m, 0)


    value = 1.e20
    replace_ieeenan(prect_sa, value, 0)
    replace_ieeenan(prect_id, value, 0)
    replace_ieeenan(prect_ea, value, 0)

    prect_sa@_FillValue = value
    prect_id@_FillValue = value
    prect_ea@_FillValue = value

    ;print(prect_ea)


    ;************************************************
    ; set function arguments
    ;************************************************
    d   = 0    ; detrending opt: 0=>remove mean 1=>remove mean + detrend
    sm  = 9   ; smooth: should be at least 3 and odd
    pct = 0.1 ; percent taper: (0.0 <= pct <= 1.0) 0.10 common. 
    ;************************************************

    ps_sa = specx_anal(prect_sa,d,sm,pct)
    ps_id = specx_anal(prect_id,d,sm,pct)
    ps_ea = specx_anal(prect_ea,d,sm,pct)

    ;print(ps_sa)

    ;************************************************
    ; plotting parameters
    ;************************************************
    wks  = gsn_open_wks("png","/home/sun/paint/AerMIP/power_spectrum_hist")             ; send graphics to PNG file
    plot = new(3,graphic)                         ; create graphic array 

    r               = True                        ; plot mods desired
    r@gsnDraw       = False                       ; do not draw
    r@gsnFrame      = False                       ; do not advance frame
    r@tiMainString  = "South Asia"                       ; title
    ;r@tiMainPosition= "Left"
    r@tiXAxisString = "Frequency (day)"  ; xaxis
    r@tiYAxisString = "Variance"                  ; yaxis
    r@trXMinF = 5
    r@trXMaxF = 120
    ;************************************************
    ; first plot
    ;************************************************
    splt = specx_ci(ps_sa, 0.05, 0.95)
    ;print(splt(0, :))
    f = ps_sa@frq 
    p   = 1/f                                    ; *highly non-linear*
    p!0 = "f"
    p&f = f
    ;ip= ind(p.le.120)
    plot(0)=gsn_csm_xy(wks, p, splt, r)  ; create plot 
    ;print(p)
    ;plot(0)=gsn_csm_xy(wks, splt, r) 
    ;***********************************************
    ; second plot: Generate quick-n-dirty plot showing 
    ;              5 and 95% "red noise" confidence 
    ;	       bounds
    ;***********************************************
    r@tiMainString  = "Indochina Peninsula" 
    splt = specx_ci(ps_id, 0.05, 0.95)             ; calc confidence interval
    ;printVarSummary(splt)
    f = ps_id@frq 
    p   = 1/f                                    ; *highly non-linear*
    p!0 = "f"
    p&f = f
    plot(1) = gsn_csm_xy(wks,p, splt,r)
    ;***********************************************
    ; Third Plot: Generate fancier plot showing 
    ;             "red noise" confidence bounds
    ;             (a) solid for spectrum and Markov, 
    ;             (b) dash for bounds 
    ;***********************************************
    r@tiMainString  = "East Asia" 
    splt = specx_ci(ps_ea, 0.05, 0.95)             ; calc confidence interval
    f = ps_ea@frq 
    p   = 1/f                                    ; *highly non-linear*
    p!0 = "f"
    p&f = f
    plot(2) = gsn_csm_xy(wks,p, splt,r)
    
    ;***********************************************
    res_P             = True                        ; panel mods desired
    res_P@gsnMaximize = True                        ; blow up plot
    gsn_panel(wks,plot,(/1,3/),res_P)               ; create panel plots

end