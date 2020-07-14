def get_ctm12_exists_query():
    return "SELECT count(srid) FROM tbl_srs WHERE srid=9377 and auth_name='EPSG'"


def get_insert_ctm12_query():
    return """INSERT INTO tbl_srs (srs_id, description, projection_acronym, ellipsoid_acronym, parameters, srid, auth_name, auth_id, is_geo, deprecated)
              VALUES (9377,
                      'MAGNA-SIRGAS / CTM12',
                      'tmerc',
                      'GRS80',
                      '+proj=tmerc +lat_0=4.0 +lon_0=-73.0 +k=0.9992 +x_0=5000000 +y_0=2000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs ',
                      9377,
                      'EPSG',
                      '9377',
                      0,
                      0
              );"""


def get_ctm12_bounds_exist_query():
    return "SELECT count(srid) FROM tbl_bounds WHERE srid=9377;"


def get_insert_cm12_bounds_query():
    return """INSERT INTO tbl_bounds (srid, west_bound_lon, north_bound_lat, east_bound_lon, south_bound_lat)
              VALUES (9377, -84.77, 15.51, -66.87, -4.23);"""
