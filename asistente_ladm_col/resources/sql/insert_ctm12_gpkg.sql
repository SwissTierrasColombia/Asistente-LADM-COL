INSERT OR IGNORE INTO gpkg_spatial_ref_sys (
  srs_name, srs_id, organization, organization_coordsys_id,
  definition
)
VALUES
  (
    'MAGNA-SIRGAS / CTM12', 38820, 'EPSG', 38820,
    'PROJCS["MAGNA-SIRGAS / CTM12",GEOGCS["MAGNA-SIRGAS",DATUM["Marco_Geocentrico_Nacional_de_Referencia",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6686"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4686"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",4.0],PARAMETER["central_meridian",-73.0],PARAMETER["scale_factor",0.9992],PARAMETER["false_easting",5000000],PARAMETER["false_northing",2000000],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","38820"]]'
  );


UPDATE gpkg_geometry_columns SET "srs_id" = 38820;

UPDATE "gpkg_contents" SET "min_x" = 3980000.000,
                           "min_y" = 1080000.000,
                           "max_x" = 5700000.000,
                           "max_y" = 3100000.000,
                           "srs_id" = 38820;

UPDATE "T_ILI2DB_COLUMN_PROP" SET "setting" = 38820
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

UPDATE "T_ILI2DB_SETTINGS" SET "setting" = 38820
WHERE "tag" = 'ch.ehi.ili2db.defaultSrsCode';