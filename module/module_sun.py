def mask_use_shapefile(ncfile, latname, lonname, shp):
    '''
    This function is to mask the data which is out of the bound

    shp is the path + filename
    '''
    import geopandas
    import rioxarray
    from shapely.geometry import mapping

    ncfile.rio.set_spatial_dims(x_dim=lonname, y_dim=latname, inplace=True)
    ncfile.rio.write_crs("epsg:4326", inplace=True)

    shape_file = geopandas.read_file(shp)

    clipped    = ncfile.rio.clip(shape_file.geometry.apply(mapping), shape_file.crs, drop=False)

    return clipped

def set_cartopy_tick(ax, extent, xticks, yticks, nx=0, ny=0,
    xformatter=None, yformatter=None,labelsize=20):
    import cartopy.crs as ccrs
    import matplotlib.ticker as mticker
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    # 本函数设置地图上的刻度 + 地图的范围
    proj = ccrs.PlateCarree()
    ax.set_xticks(xticks, crs=proj)
    ax.set_yticks(yticks, crs=proj)
    # 设置次刻度.
    xlocator = mticker.AutoMinorLocator(nx + 1)
    ylocator = mticker.AutoMinorLocator(ny + 1)
    ax.xaxis.set_minor_locator(xlocator)
    ax.yaxis.set_minor_locator(ylocator)

    # 设置Formatter.
    if xformatter is None:
        xformatter = LongitudeFormatter()
    if yformatter is None:
        yformatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(xformatter)
    ax.yaxis.set_major_formatter(yformatter)

    # 设置axi label_size，这里默认为两个轴
    ax.tick_params(axis='both',labelsize=labelsize)

    # 在最后调用set_extent,防止刻度拓宽显示范围.
    if extent is None:
        ax.set_global()
    else:
        ax.set_extent(extent, crs=proj)