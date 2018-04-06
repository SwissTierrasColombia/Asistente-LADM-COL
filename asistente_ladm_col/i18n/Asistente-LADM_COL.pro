FORMS = ../ui/dlg_load_layers.ui \
        ../ui/settings_dialog.ui \
        ../ui/wiz_add_points_cadastre.ui \
        ../ui/wiz_create_administrative_source_cadastre.ui \
        ../ui/wiz_create_plot_cadastre.ui \
        ../ui/wiz_define_boundaries_cadastre.ui \
        ../ui/wiz_create_parcel_cadastre.ui \
        ../ui/wiz_create_party_cadastre.ui \
        ../ui/wiz_create_legal_party_cadastre.ui \
        ../ui/wiz_create_natural_party_cadastre.ui \
        ../ui/wiz_create_party_cadastre.ui \
        ../ui/wiz_create_responsibility_cadastre.ui \
        ../ui/wiz_create_restriction_cadastre.ui \
        ../ui/wiz_create_right_cadastre.ui \
        ../ui/wiz_create_spatial_source_cadastre.ui

SOURCES = ../asistente_ladm_col_plugin.py \
          ../utils/qgis_utils.py \
          ../gui/create_administrative_source_cadastre_wizard.py \
          ../gui/create_legal_party_cadastre_wizard.py \
          ../gui/create_natural_party_cadastre_wizard.py \
          ../gui/create_responsibility_cadastre_wizard.py \
          ../gui/create_restriction_cadastre_wizard.py \
          ../gui/create_right_cadastre_wizard.py \
          ../gui/create_spatial_source_cadastre_wizard.py \
          ../gui/dialog_load_layers.py \
          ../gui/create_plot_cadastre_wizard.py \
          ../gui/define_boundaries_cadastre_wizard.py \
          ../gui/point_spa_uni_cadastre_wizard.py \
          ../gui/create_parcel_cadastre_wizard.py \
          ../gui/settings_dialog.py \
          ../lib/dbconnector/gpkg_connector.py \
          ../lib/dbconnector/pg_connector.py \
          ../config/help_strings.py

TRANSLATIONS = Asistente-LADM_COL_es.ts
