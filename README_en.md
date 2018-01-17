[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)

# Assistant LADM_COL
Plugin of [QGIS](http://qgis.org) that helps to capture and maintain data compliant with [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) and generate interchange files of [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

License: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


A project of: [Implementation Agency](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE SAS](http://www.incige.com/))


## Functionalities

The current version (0.0.2) of the LADM_COL Wizard allows:

 - Capture data for the LADM_COL v2.2.0 model.
 - Add points to the `Point Lindero` layer from the CSV file.
   - Validate to avoid inserting overlapping points.
 - Define `Linderos` by digitizing on the map.
   - Aids for digitization:
     - Automatic configuration of snapping and defaults for fields.
     - Split selected lines by segment.
     - Join selected lines.
 - Create `Land`:
   - From selected boundaries.
   - From a source layer with the same field structure.
 - Fill topology tables automatically:
   - `CCL Points` (relates' Punto Lindero` and` Lindero`)
   - `MasCCL` (relates` Lindero` and `Terreno`)

## Automated software testing

This is executed automatically in every commit made to the repository and the results of these are available in:

- Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

To run the tests locally you need to have *docker* and *docker-compose* installed.
- The version of *docker* that we use can be downloaded from your [official site](https://www.docker.com/community-edition#/download), for the development we use Ubuntu / Linux_Mint so we follow the steps from
[Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- The version of *docker-compose* that we use can be installed using the [binaries](https://github.com/docker/compose/releases/tag/1.18.0).

The command to execute the tests is:
`` `sh
docker-compose run --rm qgis
`` `
