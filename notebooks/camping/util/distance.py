import geopandas as gpd

def distance_merge(to_buffer, left, max_distance, lsuffix, rsuffix):
    # https://stackoverflow.com/questions/58848416/filter-and-merge-points-from-two-dataframe-within-a-specific-distance-in-geopand
    buffer_df = gpd.GeoDataFrame(to_buffer, geometry=gpd.points_from_xy(to_buffer.FacilityLongitude, to_buffer.FacilityLatitude))
    left_df = gpd.GeoDataFrame(left, geometry=(gpd.points_from_xy(left.FacilityLongitude, left.FacilityLatitude)))
    buffer_df.crs = left_df.crs = {'init': 'epsg:4326'} 
    buffer_df = buffer_df.to_crs({'init': 'epsg:3857'})
    left_df = left_df.to_crs({'init': 'epsg:3857'})

    # Create a buffer around each point to perform intersects with point in left df
    buffer_df.geometry = buffer_df.geometry.buffer(max_distance)

    # Join the two Dataframes and convert back to original projection
    merged = gpd.sjoin(left_df, buffer_df, how='left', op='intersects', lsuffix=lsuffix, rsuffix=rsuffix)
    return merged.to_crs({'init': 'epsg:4326'}) # or whatever was used originally
