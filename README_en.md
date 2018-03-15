[![License](https://img.shields.io/github/license/AgenciaImplementacion/Asistente-LADM_COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/AgenciaImplementacion/asistente-ladm_col.svg)](https://github.com/AgenciaImplementacion/asistente-ladm_col/releases)
[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)

# LADM_COL Assistant
[QGIS](http://qgis.org) plugin to capture and maintain data compliant with [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) as well as generate [INTERLIS](http://www.interlis.ch/index_e.htm) interchange files (.XTF).

License: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


A project of: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE SAS](http://www.incige.com/))


## Functionalities

The current version (0.0.6) of the LADM_COL Assistant depends on [Project Generator](https://github.com/opengisch/projectgenerator/) plugin [v3.0.2.1](https://github.com/AgenciaImplementacion/projectgenerator/releases/tag/v3.0.2.1) and allows users to:

 - Capture data for the LADM_COL v2.2.1 model.
 - Add points to the `Boundary Point` and `Survey Point` layers from CSV files.
   - Validate and avoid insertion of overlapping points.
 - Define `Boundaries` by digitizing on the map.
   - Aids for digitization:
     - Automatic snapping configuration and default field values.
     - Explode selected lines (split per segment).
     - Merge selected lines.
 - Create `Plot`:
   - From selected boundaries.
   - From a source layer with the same field structure as the `Plot` layer.
 - Fill topology tables automatically:
   - `BFS Points` (relates `Boundary Points` to `Boundary`)
   - `More BFS` (relates `Boundaries` to `Plot`)
   - `Less` (relates `Plots` to their inner rings)
 - Create `Parcels` from existing `Plots`.
 - Create `Natural Parties` and `Legal Parties` using preconfigured forms.
 - Create `Spatial Sources` and `Administrative Sources` using preconfigured forms.
 - Select layers to load from any model in the database or schema:
   - Use the 'Project Generator' plugin (a prerequisite) to load layers with configured forms and relations.
   - Load preconfigured layer sets.
 - Check quality:
   - Check too long `Boundary` segments (exceeding a given tolerance).
   - Check overlapping `Boundary Points`.
 - Use configured styles for loaded layers.

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
docker-compose build
```
