'''
2024-5-31
This script is to conduct the postprocess for the cdnc variable, it is annoying but the raw data of Aermon is sigma coordination

The workflow for the postprocess:
1. make special function for each model
2. for each grid, interpolate them to the unified plev
'''
import xarray as xr
import numpy as np
import os
from scipy.interpolate import interp1d
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "2309598788@qq.com"  # 替换为你的发件邮箱
    password = "aakziellvvdydihc"  # 替换为你的邮箱密码

    # 设置邮件内容
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 连接到邮件服务器并发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # 使用SSL连接
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

# =========== Send email ================

# claim the plev
ref_file = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_ua_cat/ua_Amon_GISS-E2-1-G_ssp370_r3i1p1f2.nc")
plev     = ref_file.plev.data
#print(plev)


# ============ All the file ==========
path_in  = "/home/sun/wd_disk/AerChemMIP/download/mon_cdnc/"
out_path = "/home/sun/wd_disk/AerChemMIP/download/mon_cdnc_p/"
file_all = os.listdir("/home/sun/wd_disk/AerChemMIP/download/mon_cdnc/")

def unify_lat_lon(f0, new_lat, new_lon,):
    '''
        This function is to unify the lat/lon information for each inputed f0
    '''
    old_lat   = f0['lat'].data
    old_lon   = f0['lon'].data
    time_data = f0['time'].data

    f0_interp = f0.interp(lat = new_lat, lon=new_lon,)

    return f0_interp

def single_model_list(model_tag):
    '''
        This function is to get the filelist for the single model
    '''
    model_list = []
    for ff in file_all:
        if model_tag in ff and ff[0] != '.' and ff[-2:] == 'nc':
            model_list.append(ff)
        else:
            continue
    
    return model_list

# =========== Function for EC-Earth =============
def postprocess_EC():
    modelname = "EC-Earth3-AerChem"
    # 1. get the file list
    file_list_single = single_model_list(modelname)
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.ap.data ; b = f_single.b.data # 1-D
        ps  = f_single.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap + b * ps[tt, ii, jj]

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj] = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

# =========== Function for GFDL =============
def postprocess_GFDL():
    '''GFDL cdnc file do not include ps variable '''
    modelname = 'GFDL'
    # 1. get the file list
    file_list_single = single_model_list(modelname)
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # Read ps file
        f_single_ps = xr.open_dataset("/home/sun/wd_disk/AerChemMIP/download/mon_ps/" + ff_model.replace("cdnc_", "ps_"))

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.ap.data ; b = f_single.b.data # 1-D
        ps  = f_single_ps.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap + b * ps[tt, ii, jj]

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj] = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

# =========== Function for GISS =============
def postprocess_GISS():
    '''lev:formula = "p = a*p0 + b*ps"'''
    modelname = 'GISS'
    # 1. get the file list
    file_list_single = single_model_list("GISS")
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.a.data ; b = f_single.b.data ; p0 = f_single.p0.data  # 1-D
        ps  = f_single.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap*p0 + b * ps[tt, ii, jj]

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj] = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

# =========== Function for MIROC6 =============
def postprocess_MIROC6():
    '''lev:formula = "p = a*p0 + b*ps" '''
    modelname = "MIROC6"
    # 1. get the file list
    file_list_single = single_model_list(modelname)
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.a.data ; b = f_single.b.data ; p0 = f_single.p0.data # 1-D
        ps  = f_single.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap*p0 + b * ps[tt, ii, jj]

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj] = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

# =========== Function for MPI-ESM =============
def postprocess_MPI():
    '''lev:formula = "p = ap + b*ps" '''
    modelname = "MPI-ESM"
    # 1. get the file list
    file_list_single = single_model_list(modelname)
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.ap.data ; b = f_single.b.data # 1-D
        ps  = f_single.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap + b * ps[tt, ii, jj]

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj] = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

# =========== Function for MRI-ESM =============
def postprocess_MRI():
    '''lev:formula = "p = a*p0 + b*ps"'''
    modelname = "MRI-ESM"
    # 1. get the file list
    file_list_single = single_model_list(modelname)
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.a.data ; b = f_single.b.data ; p0 = f_single.p0.data  # 1-D
        ps  = f_single.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap*p0 + b * ps[tt, ii, jj]

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj] = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

# =========== Function for UKESM =============
def postprocess_UKESM():
    '''lev:formula = "z = a + b*orog" '''
    modelname = "UKESM"
    # 1. get the file list
    file_list_single = single_model_list(modelname)
    file_list_single.sort()

    #print(file_list_single)
    # 2. Deal with each file
    for ff_model in file_list_single:
        print(f'Now it starts to deal with {ff_model}')
        f_single = xr.open_dataset(path_in + ff_model)

        # 2.1 get dimension
        lon = f_single.lon.data ; lat = f_single.lat.data ; time = f_single.time.data ; 

        # 2.2 get variables needed for calculating the pressure
        # formula = "p = ap + b*ps"
        ap  = f_single.lev.data ; b = f_single.b.data ; orog = f_single.orog.data # 1-D
        #ps  = f_single.ps.data # 3-D ; Pa

        # 2.3 get raw data for cdnc
        cdnc0 = f_single.cdnc.data

        # 2.4 claim the array for interpolated data
        cdnc_p = np.zeros((len(time), len(plev), len(lat), len(lon)))
        cdnc_column = np.zeros((len(time), len(lat), len(lon)))

        # 3. calculate for each grid
        for tt in range(len(time)):
            for ii in range(len(lat)):
                for jj in range(len(lon)):
                    p_regress = ap + b * orog[ii, jj] # orog is 2d var

                    #print(p_regress)
                    interpolation_function = interp1d(p_regress, cdnc0[tt, :, ii, jj], kind='linear', fill_value=np.nan, bounds_error=False)

                    cdnc_p[tt, :, ii, jj]   = interpolation_function(plev)
                    cdnc_column[tt, ii, jj] = np.trapz(cdnc_p[tt, :, ii, jj]/1.225/9.8, plev)

                    #cdnc_p[tt, :, ii, jj][plev > ps[tt, ii, jj]] = np.nan

        print(f'Calculation finishes for {ff_model}')
        
        # 4. Write to ncfile
        ncfile  =  xr.Dataset(
            {
                "cdnc":     (["time", "plev", "lat", "lon"], cdnc_p),     
                "cdnc_column":     (["time", "lat", "lon"],  cdnc_column),     
                "time_bnds":(["time", "bnds"], f_single.time_bnds.data),
                "lat_bnds": (["lat",  "bnds"], f_single.lat_bnds.data),
                "lon_bnds": (["lon",  "bnds"], f_single.lon_bnds.data),
            },
            coords={
                "lat":  (["lat"],  f_single.lat.data),
                "lon":  (["lon"],  f_single.lon.data),
                "time": f_single.time,
                "plev": (["plev"], plev),
                "bnds": (["bnds"], f_single.bnds.data)
            },
            )

        ncfile.attrs = f_single.attrs
        ncfile.time.attrs = f_single.time.attrs
        ncfile.lat.attrs  = f_single.lat.attrs
        ncfile.lon.attrs  = f_single.lon.attrs
        ncfile.cdnc.attrs = f_single.cdnc.attrs
        ncfile.plev.attrs = ref_file.plev.attrs

        # interpolate to new lat/lon
        new_lat = np.linspace(-90, 90, 91)
        new_lon = np.linspace(0, 358, 180)

        ncfile_new  = unify_lat_lon(ncfile, new_lat, new_lon)

        ncfile_new.to_netcdf(out_path + ff_model)

        ncfile.close()
        ncfile_new.close()
        f_single.close()

if __name__ == '__main__':
#    send_email("1", "2", "sunweihao97@gmail.com")
#    postprocess_EC()
#    postprocess_GFDL()
#    postprocess_GISS()
#    postprocess_MIROC6()
    postprocess_UKESM()
    postprocess_MPI()
    postprocess_MRI()