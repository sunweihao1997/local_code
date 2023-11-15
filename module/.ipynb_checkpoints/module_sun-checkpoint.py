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