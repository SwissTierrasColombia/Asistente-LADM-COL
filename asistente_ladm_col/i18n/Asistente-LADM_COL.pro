FORMS = ../ui/settings_dialog.ui \
        ../ui/wiz_add_points_cadaster.ui \
        ../ui/wiz_create_plot_cadaster.ui \
        ../ui/wiz_define_boundaries_cadaster.ui \
        ../ui/wiz_create_parcel_cadastre.ui \
        ../ui/wiz_create_party_cadastre.ui

SOURCES = ../asistente_ladm_col_plugin.py \
          ../utils/qgis_utils.py \
          ../gui/create_plot_cadaster_wizard.py \
          ../gui/define_boundaries_cadaster_wizard.py \
          ../gui/point_spa_uni_cadaster_wizard.py \
          ../gui/create_parcel_cadastre_wizard.py \
          ../gui/create_party_cadastre_wizard.py \
          ../gui/settings_dialog.py \
          ../lib/dbconnector/gpkg_connector.py \
          ../lib/dbconnector/pg_connector.py

TRANSLATIONS = Asistente-LADM_COL_es.ts
