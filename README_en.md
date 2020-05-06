[![License](https://img.shields.io/github/license/SwissTierrasColombia/Asistente-LADM-COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/SwissTierrasColombia/asistente-ladm_col.svg)](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases)
[![Build Status](https://travis-ci.org/SwissTierrasColombia/Asistente-LADM-COL.svg?branch=master)](https://travis-ci.org/SwissTierrasColombia/Asistente-LADM-COL)
[![Build Status](http://portal.proadmintierra.info:18000/status.svg?branch=master)](http://portal.proadmintierra.info:18000)

# LADM-COL Assistant
[QGIS](http://qgis.org) plugin to capture and maintain data compliant with [LADM-COL](https://github.com/SwissTierrasColombia/LADM-COL) as well as to generate [INTERLIS](http://www.interlis.ch/index_e.htm) interchange files (.XTF).

License: [GNU General Public License v3.0](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/LICENSE)

Links of interest: [Documentation](https://swisstierrascolombia.github.io/Asistente-LADM-COL/), [Gallery](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/README_en.md#gallery)

A project of: [SwissTierras Colombia](https://swisstierrascolombia.com/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE SAS](http://www.incige.com/))


:arrow_right: We suggest you to use QGIS v3.10.x, available at https://qgis.org/downloads/


## Functionalities

The current version ([2.99.3](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases/tag/2.99.3)) of the LADM-COL Assistant depends on [QGIS Model Baker v6.1.1.1](https://github.com/SwissTierrasColombia/QgisModelBaker/releases/download/v6.1.1.1/QgisModelBaker_6111.zip) and allows users to:

 - Integration with the Transitional System:
   - Authentication
   - Task management: start, cancel and finalize tasks.
   - Tasks of cadastral supplies generation and assisted integration of supplies (partial support). 
     - ETL to generate cadastral supplies from cadastral authority (IGAC) data (SNC source).
     - ETL to generate cadastral supplies from cadastral authority (IGAC) data (Cobol source).
 - Roles support and GUI for each role.
 - Create database structures for the LADM-COL v2.9.6 model.
 - Two database engines to manage LADM-COL data:
   - PostgreSQL/PostGIS: Total support.
   - GeoPackage: quality validations and reports are not yet supported.
 - Capture data for the `OPERACION v2.9.6` model ([download](https://github.com/SwissTierrasColombia/LADM-COL/releases/download/2.9.6/LADM_COL-2_9_6.zip)).
 - Import data from transfer files (.XTF).
 - Export data to transfer files (.XTF).
 - Import/export data from/to transfer files (.XTF) disabling data validation.
 - Search for LADM-COL data by component:
   - Basic information.
   - Legal information.
   - Property record card information.
   - Physical information.
   - Economic information.
 - Add points to the `Boundary Point`, `Survey Point` and `Control Point` layers:
   - From CSV files.
     - Validate and avoid insertion of overlapping points.
   - From another layer with any structure, setting a field mapping.
 - Define `Boundaries`:
   - By digitizing on the map.
     - Aids for digitization:
       - Automatic snapping configuration and default field values.
       - Build boundaries from selected lines.
   - From another layer with any structure, setting a field mapping.
 - Create `Plot`:
   - From selected boundaries.
   - From another layer with any structure, setting a field mapping.
 - Fill topology tables automatically:
   - `BFS Points` (relates `Boundary Points` to `Boundary`)
   - `More BFS` (relates `Boundaries` to `Plot`)
   - `Less` (relates `Plots` to their inner rings)
 - Create `Right of Way`:
   - By digitizing on the map the polygon or a centerline with width.
     - Aids for digitization:
       - Automatic snapping configuration and default field values.
   - From another layer with any structure, setting a field mapping.
   - Create relations of benefited and restricted `Parcels`.
 - Associate addresses to `Plots`, `Buildings` and `Unit Buildings`.
 - Create `Parcels`:
   - Using preconfigured forms.
     - And associating the new `Parcel` to selected `Plots` and/or `Buildings`.
   - From another table with any structure, setting a field mapping.
 - Create `Buildings` and `Building Units`:
   - By digitizing on the map.
     - Aids for digitization:
       - Automatic snapping configuration and default field values.
   - From another layer with any structure, setting a field mapping.
 - Create `Natural Parties` and `Legal Parties`:
   - Using preconfigured forms.
   - From another table with any structure, setting a field mapping.
 - Create `Group Party`:
   - Using a preconfigured form.
 - Create `Spatial Sources` and `Administrative Sources`:
   - Using preconfigured forms.
     - And associating the new `Spatial Source` to selected `Plots`, `Boundaries` or `Points`.
   - From another table with any structure, setting a field mapping.
 - Create `Source Files`:
   - Associate sources to source files.
   - Upload source files to a server at saving-edits time or later, in batch mode.
 - Create `Rights`, `Restrictions` and `Responsibilities`:
   - Using preconfigured forms (associating the new object to selected `Administrative Sources`).
   - From another table with any structure, setting a field mapping.
 - Select in a dialog layers to load from any model in the database or schema:
   - Use the 'QGIS Model Baker' plugin (a prerequisite) to load layers with configured forms, relations and domains.
   - Load preconfigured layer sets.
 - Check quality rules (topology):
   - Check overlaps in `Boundary Points`.
   - Check overlaps in `Control Points`.
   - Check overlaps in `Boundary`.
   - Check overlaps in `Plot`.
   - Check overlaps in `Building`.
   - Check overlaps in `Right of Way`.
   - Check missing `Boundary Points` that do not have `Boundary` nodes correctly associated.
   - Check missing `Boundary` nodes that do not have `Boundary Points` correctly associated.
   - Check dangles in `Boundary`.
   - Check that `Boundaries` are not split.
   - Check overlaps between `Right of Way` and `Building`.
   - Check that `Plots` have no gaps in between.
   - Check that `Plot` boundaries are covered by `Boundaries` and their relations are correctly recorded in topology tables (`MoreBFS` and `Less`).
   - Check that `Boundaries` are covered by `Plot` boundaries and their relations are correctly recorded in topology tables (`MoreBFS` and `Less`).
   - Check that `Right of Way` has no multi-part geometries.
   - Check that `Buildings` are within their corresponding `Plots`.
   - Check that `Building Units` are within their corresponding `Plots`.
 - Check quality rules (consistency):
   - Parcel should have one and only one Right.
   - Table records should not be repeated.
   - Group Party Fractions should sum 1.
   - Check that the departamento field of the predio table has two numerical characters.
   - Check that the municipality field of the predio table has three numerical characters.
   - Check that the zona field of the predio table has two numerical characters.
   - Check that the numero_predial has 30 numerical characters.
   - Check that the numero_predial_anterior has 20 numerical characters.
   - Check that attributes are appropriate for parties of type natural.
   - Check that attributes are appropriate for parties of type legal.
   - Check that the type of parcel corresponds to position 22 of the numero_predial.
   - Check that Spatial Units associated with Parcels correspond to the parcel type.
 - Generate report of the quality checks.
 - Generate reports based on selected `Plots` (Annex 17).
 - Generate reports based on selected `Plots` (ANT map).
 - Generate reports of missing supplies.
 - Detect parcel changes:
   - Compare a collected database versus the supplies database and show differences by batch or per parcel.
 - Import data from [intermediate structure in Excel](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/asistente_ladm_col/resources/excel/datos_estructura_excel.xlsx).
 - Configure automatic values for `namespace` and `local_id` attributes.
 - Load styles for newly added layers from preconfigured QML files.
 - Online/offline help.


## Minimum requirements

To use the LADM-COL Assistant you need:

 - Operting System:
   - Windows 8 or Windows 10
   - GNU/Linux
 - Base software:
   - QGIS v3.10.0-A Coruña or higher
   - Java v1.8
   - PostgreSQL 9.5 or higher (PostgreSQL 10 and PostgreSQL 11 works as well). Support for v12 is still experimental.
   - PostGIS 2.4 or higher.
 - QGIS plugins (installing LADM-COL Assistant using QGIS Plugin Manager will also install these automatically):
   - QGIS Model Baker v6.1.1.1
   - MapSwipe Tool v1.2

## Testing

### Unit tests

Unit tests are automatically executed after every commit made to the repository. Results are available for:

- GNU/Linux: https://travis-ci.org/SwissTierrasColombia/Asistente-LADM-COL

To run the tests locally you need to have *docker* and *docker-compose* installed. We suggest to:
- Download *docker* from the [official site](https://hub.docker.com/search/?type=edition&offering=community). For instance, for Ubuntu / Linux_Mint follow the steps in [Install using the convenience script](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Install *docker-compose* using the [binaries](https://github.com/docker/compose/releases).
- NOTE: [installing Docker](https://www.how2shout.com/how-to/how-to-install-docker-ce-on-ubuntu-20-04-lts-focal-fossa.html) on Ubuntu 20.04 is easier.

The command to execute unit tests is (execute from the repository's root folder):
```sh
docker-compose run --rm qgis
```

If you need to recreate docker image, you can use:
```sh
docker-compose down --rmi local && docker-compose build
```

### Assisted tests (for the GUI)

The LADM-COL Assistant uses *QGIS Tester* plugin to support assisted tests for GUI functionalities. 

Prerrequisites:

In order to run the assisted tests, you need to install:

- *QGIS Tester* plugin (available at: https://github.com/planetfederal/qgis-tester-plugin).
- *qgiscommons* library: ```pip install qgiscommons```

See [the docs](https://github.com/planetfederal/qgis-tester-plugin/blob/master/docs/source/usage.rst) for usage instructions.

If these prerrequisites are not met, the LADM-COL Assistant will continue running smoothly and will put a warning in the QGIS log. 


## How to be notified of new relases of the LADM-COL Assistant?

 + If you have a GitHub account or you can create one, go to https://github.com/SwissTierrasColombia/Asistente-LADM-COL/ and click the `Watch` button in the upper part of the web page to follow changes on the repository.

 + If you do not have a GitHub account, you have two options:

   a) Sbscribe to the release feed: https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases.atom

   b) Use gitpunch!

      + Go to https://gitpunch.com/
      + Wait until the animation ends or click on `Skip` (below in the page).
      + Sign in using your e-mail.
      + Search for "Asistente LADM-COL" and choose the `SwissTierrasColombia/Asistente-LADM-COL` repository.
      + That's it! After getting notifications, you will need to wait some hours until the plugin is accepted and available in the QGIS plugin repo.


      
## Gallery

 + Quality Rules:

  ![Quality Rules](https://s3.amazonaws.com/media-p.slid.es/uploads/308098/images/6343636/quality_rules_25-min.gif)

+ Queries:

  ![Queries](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290636/query_25.gif)

+ Reports:

  ![Reports](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290657/report_25.gif)

+ Change detection:

  ![Change detection](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6293473/novedades_short_40_slides.gif)

+ Integration with Transitional System

![insumos](https://user-images.githubusercontent.com/27906888/75196661-73b97b80-572a-11ea-8ae0-30cebccd7996.gif)
