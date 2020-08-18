INSERT OR IGNORE INTO gpkg_spatial_ref_sys (
  srs_name, srs_id, organization, organization_coordsys_id,
  definition
)
VALUES
  (
    'MAGNA-SIRGAS / Origen-Nacional', 9377, 'EPSG', 9377,
    'PROJCRS["MAGNA-SIRGAS / Origen-Nacional", BASEGEOGCRS["MAGNA-SIRGAS", DATUM["Marco Geocentrico Nacional de Referencia", ELLIPSOID["GRS 1980",6378137,298.257222101, LENGTHUNIT["metre",1]]], PRIMEM["Greenwich",0, ANGLEUNIT["degree",0.0174532925199433]], ID["EPSG",4686]], CONVERSION["Colombia Transverse Mercator", METHOD["Transverse Mercator", ID["EPSG",9807]], PARAMETER["Latitude of natural origin",4, ANGLEUNIT["degree",0.0174532925199433], ID["EPSG",8801]], PARAMETER["Longitude of natural origin",-73, ANGLEUNIT["degree",0.0174532925199433], ID["EPSG",8802]], PARAMETER["Scale factor at natural origin",0.9992, SCALEUNIT["unity",1], ID["EPSG",8805]], PARAMETER["False easting",5000000, LENGTHUNIT["metre",1], ID["EPSG",8806]], PARAMETER["False northing",2000000, LENGTHUNIT["metre",1], ID["EPSG",8807]]], CS[Cartesian,2], AXIS["northing (N)",north, ORDER[1], LENGTHUNIT["metre",1]], AXIS["easting (E)",east, ORDER[2], LENGTHUNIT["metre",1]], USAGE[ SCOPE["unknown"], AREA["Colombia"], BBOX[-4.23,-84.77,15.51,-66.87]], ID["EPSG",9377]]'
  );


UPDATE gpkg_geometry_columns SET "srs_id" = 9377;

UPDATE "gpkg_contents" SET "min_x" = 3980000.000,
                           "min_y" = 1080000.000,
                           "max_x" = 5700000.000,
                           "max_y" = 3100000.000,
                           "srs_id" = 9377;

UPDATE "T_ILI2DB_COLUMN_PROP" SET "setting" = 9377
WHERE "tag" = 'ch.ehi.ili2db.srid';

-- c1:X, c2:Y
UPDATE "T_ILI2DB_COLUMN_PROP" SET "setting" = 5700000.000
WHERE "tag" = 'ch.ehi.ili2db.c1Max';
UPDATE "T_ILI2DB_COLUMN_PROP" SET "setting" = 3100000.000
WHERE "tag" = 'ch.ehi.ili2db.c2Max';
UPDATE "T_ILI2DB_COLUMN_PROP" SET "setting" = 3980000.000
WHERE "tag" = 'ch.ehi.ili2db.c1Min';
UPDATE "T_ILI2DB_COLUMN_PROP" SET "setting" = 1080000.000
WHERE "tag" = 'ch.ehi.ili2db.c2Min';

UPDATE "T_ILI2DB_SETTINGS" SET "setting" = 'EPSG'
WHERE "tag" = 'ch.ehi.ili2db.defaultSrsAuthority';

UPDATE "T_ILI2DB_SETTINGS" SET "setting" = 9377
WHERE "tag" = 'ch.ehi.ili2db.defaultSrsCode';