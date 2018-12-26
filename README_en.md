[![License](https://img.shields.io/github/license/AgenciaImplementacion/Asistente-LADM_COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/AgenciaImplementacion/asistente-ladm_col.svg)](https://github.com/AgenciaImplementacion/asistente-ladm_col/releases)
[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)
[![Build Status](http://portal.proadmintierra.info:18000/status.svg?branch=master)](http://portal.proadmintierra.info:18000)

# LADM_COL Assistant
[QGIS](http://qgis.org) plugin to capture and maintain data compliant with [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) as well as generate [INTERLIS](http://www.interlis.ch/index_e.htm) interchange files (.XTF).

License: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


A project of: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE SAS](http://www.incige.com/))


:arrow_right: We suggest you to use QGIS v3.4.x, available at https://qgis.org/downloads/


## Functionalities

The current version ([1.0.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases/tag/1.0.0)) of the LADM_COL Assistant depends on [Project Generator v3.3.7](https://github.com/opengisch/projectgenerator/releases/download/v3.3.7/projectgenerator.v3.3.7.zip) and allows users to:

 - Capture data for the `CATASTRO_REGISTRO_NUCLEO v2.2.1` model.
 - Capture data for the `FICHA_PREDIAL v2.2.1` model.
 - Capture data for the `AVALÚOS v2.2.1` model.
 - Preprocess points: Controlled Measurement.
   - Group points by nearness.
   - Average point position from points of the same group.
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
 - Create `Propert Record Card`, `Market Research`, `Nuclear Family`, `Natural Party` and `Legal Party`:
   - Using preconfigured forms.
   - From another table with any structure, setting a field mapping.
 - Select in a dialog layers to load from any model in the database or schema:
   - Use the 'Project Generator' plugin (a prerequisite) to load layers with configured forms, relations and domains.
   - Load preconfigured layer sets.
 - Check quality rules (topology):
   - Check too long `Boundary` segments (exceeding a given tolerance).
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
 - Check quality rules (consistency):
   - Parcel should hace one and only one Right
   - Table records should not be repeated
   - Group Party Fractions should sum 1
   - Check that the departamento field of the predio table has two numerical characters
   - Check that the municipality field of the predio table has three numerical characters
   - Check that the zona field of the predio table has two numerical characters
   - Check that the numero_predial has 30 numerical characters
   - Check that the numero_predial_anterior has 20 numerical characters
   - Check that attributes are appropriate for parties of type natural
   - Check that attributes are appropriate for parties of type legal
   - Check that the type of parcel corresponds to position 22 of the numero_predial
   - Check that Spatial Units associated with Parcels correspond to the parcel type
 - Generate reports based on selected `Plots` (Annex 17).
 - Import data from [intermediate structure in Excel](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/asistente_ladm_col/resources/excel/datos_estructura_excel.xlsx).
 - Configure automatic values for `namespace` and `local_id` attributes.
 - Load styles for newly added layers from preconfigured QML files.
 - View illustrative GIFs in the plugin's online help or download them for offline work.

## Testing

Unit tests are automatically executed after every commit made to the repository. Results are available for:

- GNU/Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

To run the tests locally you need to have *docker* and *docker-compose* installed. We suggest to:
- Download *docker* from the [official site](https://www.docker.com/community-edition#/download). For instance, for Ubuntu / Linux_Mint follow the steps in [Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Install *docker-compose* using the [binaries](https://github.com/docker/compose/releases/tag/1.18.0).

The command to execute unit tests is (execute from the repository's root folder):
```sh
docker-compose run --rm qgis
```

If you need to recreate docker image, you can use:
```sh
docker-compose down --rmi local && docker-compose build
```

## How to be notified of new relases of the LADM_COL Assistant?

 + If you have a GitHub account or you can create one, go to https://github.com/AgenciaImplementacion/Asistente-LADM_COL/ and click the `Watch` button in the upper part of the web page to follow changes on the repository.

 + If you do not have a GitHub account, you have two options:

   a) Sbscribe to the release feed: https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases.atom

   b) Use gitpunch!

      + Go to https://gitpunch.com/
      + Wait until the animation ends or click on `Skip` (below in the page).
      + Sign in using your e-mail.
      + Search for "Asistente LADM_COL" and choose the `AgenciaImplementacion/Asistente-LADM_COL` repository.
      + That's it! After getting notifications, you will need to wait some hours until the plugin is accepted and available in the QGIS plugin repo.
