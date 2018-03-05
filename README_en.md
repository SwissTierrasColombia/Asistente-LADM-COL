[![License](https://img.shields.io/github/license/AgenciaImplementacion/Asistente-LADM_COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/AgenciaImplementacion/asistente-ladm_col.svg)](https://github.com/AgenciaImplementacion/asistente-ladm_col/releases)
[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)

# LADM_COL Assistant
[QGIS](http://qgis.org) plugin to capture and maintain data compliant with [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) as well as generate [INTERLIS](http://www.interlis.ch/index_e.htm) interchange files (.XTF).

License: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


A project of: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE SAS](http://www.incige.com/))


## Functionalities

The current version (0.0.5) of the LADM_COL Assistant depends on [Project Generator](https://github.com/opengisch/projectgenerator/) plugin v3.0.0 and allows to:

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
 - Check too long `Boundary` segments (exceeding a given tolerance).
 - Use the 'Project Generator' plugin (a prerequisite) to load layers with configured forms and relations.
 - Use configured styles for loaded layers.
