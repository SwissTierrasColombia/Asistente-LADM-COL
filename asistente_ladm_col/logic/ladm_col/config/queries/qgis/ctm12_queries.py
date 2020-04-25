def get_ctm12_exists_query():
    return "SELECT count(srs_id) FROM tbl_srs WHERE srs_id=38820 and auth_name='STC'"


def get_insert_ctm12_query():
    return """INSERT INTO tbl_srs (srs_id, description, projection_acronym, ellipsoid_acronym, parameters, srid, auth_name, auth_id, is_geo, deprecated)
              VALUES (38820,
                      'MAGNA-SIRGAS / CTM12',
                      'tmerc',
                      'GRS80',
                      '+proj=tmerc +lat_0=4.0 +lon_0=-73.0 +k=0.9992 +x_0=5000000 +y_0=2000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs ',
                      38820,
                      'STC',
                      '38820',
                      0,
                      0
              );"""


def get_insert_cm12_bounds_query():
    return """INSERT INTO tbl_bounds (srid, west_bound_lon, north_bound_lat, east_bound_lon, south_bound_lat)
              VALUES (38820, -82.2, 16.1, -66.5, -4.3);"""
