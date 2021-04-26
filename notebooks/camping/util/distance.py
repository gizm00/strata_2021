import geopandas as gpd

def distance_merge(nf_data, ridb_data, max_distance, lsuffix='ridb', rsuffix='nf'):
    # https://stackoverflow.com/questions/58848416/filter-and-merge-points-from-two-dataframe-within-a-specific-distance-in-geopand
    ridb_data = ridb_data[['FacilityID', 'CampsiteID', 'FacilityLatitude', 'FacilityLongitude']]
    buffer_df = gpd.GeoDataFrame(nf_data, geometry=gpd.points_from_xy(nf_data.FacilityLongitude, nf_data.FacilityLatitude))
    ridb_data_df = gpd.GeoDataFrame(ridb_data, geometry=(gpd.points_from_xy(ridb_data.FacilityLongitude, ridb_data.FacilityLatitude)))
    buffer_df.crs = ridb_data_df.crs = {'init': 'epsg:4326'} 
    buffer_df = buffer_df.to_crs({'init': 'epsg:3857'})
    ridb_data_df = ridb_data_df.to_crs({'init': 'epsg:3857'})

    # Create a buffer around each point to perform intersects with point in ridb_data df
    buffer_df.geometry = buffer_df.geometry.buffer(max_distance)

    # Join the two Dataframes and convert back to original projection
    merged = gpd.sjoin(ridb_data_df, buffer_df, how='left', op='intersects', lsuffix=lsuffix, rsuffix=rsuffix)
    merged = merged.to_crs({'init': 'epsg:4326'})
    return merged

