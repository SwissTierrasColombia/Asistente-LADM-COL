FORMS = ../ui/change_detection/changes_all_parcels_panel_widget.ui \
        ../ui/change_detection/changes_parties_panel_widget.ui \
        ../ui/change_detection/changes_per_parcel_panel_widget.ui \
        ../ui/change_detection/dlg_change_detection_settings.ui \
        ../ui/change_detection/dlg_select_duplicate_parcel_change_detection.ui \
        ../ui/change_detection/dockwidget_change_detection.ui \
        ../ui/change_detection/parcels_changes_summary_panel_widget.ui \
        ../ui/dialogs/dlg_about.ui \
        ../ui/dialogs/dlg_custom_model_dir.ui \
        ../ui/dialogs/dlg_get_db_or_schema_name.ui \
        ../ui/dialogs/dlg_import_from_excel.ui \
        ../ui/dialogs/dlg_load_layers.ui \
        ../ui/dialogs/dlg_log_excel.ui \
        ../ui/dialogs/dlg_log_quality.ui \
        ../ui/dialogs/dlg_quality.ui \
        ../ui/dialogs/dlg_settings.ui \
        ../ui/dialogs/dlg_topological_edition.ui \
        ../ui/dialogs/dlg_upload_progress.ui \
        ../ui/dialogs/dlg_welcome_screen.ui \
	    ../ui/dialogs/settings_gpkg.ui \
	    ../ui/dialogs/settings_pg.ui \
        ../ui/dockwidgets/dockwidget_queries.ui \
        ../ui/qgis_model_baker/dlg_import_schema.ui \
        ../ui/qgis_model_baker/dlg_import_data.ui \
        ../ui/qgis_model_baker/dlg_export_data.ui \
        ../ui/supplies/cobol_data_source_widget.ui \
        ../ui/supplies/snc_data_source_widget.ui \
        ../ui/supplies/wig_cobol_supplies.ui \
        ../ui/supplies/wig_missing_cobol_supplies_export.ui \
        ../ui/supplies/wiz_supplies_etl.ui \
        ../ui/transitional_system/dlg_cancel_task.ui \
        ../ui/transitional_system/dlg_login_st.ui \
        ../ui/transitional_system/dlg_upload_file.ui \
        ../ui/transitional_system/dockwidget_transitional_system.ui \
        ../ui/transitional_system/home_widget.ui \
        ../ui/transitional_system/task_widget_item.ui \
        ../ui/transitional_system/tasks_widget.ui \
        ../ui/transitional_system/transitional_system_initial_panel_widget.ui \
        ../ui/transitional_system/transitional_system_task_panel_widget.ui \
        ../ui/wizards/operation/dlg_group_party.ui \
	    ../ui/wizards/operation/wiz_associate_extaddress_operation.ui \
        ../ui/wizards/operation/wiz_create_administrative_source_operation.ui \
        ../ui/wizards/operation/wiz_create_boundaries_operation.ui \
        ../ui/wizards/operation/wiz_create_building_operation.ui \
        ../ui/wizards/operation/wiz_create_building_unit_operation.ui \
        ../ui/wizards/operation/wiz_create_col_party_operation.ui \
        ../ui/wizards/operation/wiz_create_parcel_operation.ui \
        ../ui/wizards/operation/wiz_create_plot_operation.ui \
        ../ui/wizards/operation/wiz_create_points_operation.ui \
        ../ui/wizards/operation/wiz_create_restriction_operation.ui \
        ../ui/wizards/operation/wiz_create_right_of_way_operation.ui \
        ../ui/wizards/operation/wiz_create_right_operation.ui \
        ../ui/wizards/operation/wiz_create_spatial_source_operation.ui \
        ../ui/wizards/valuation/wiz_create_building_unit_qualification_valuation.ui \
        ../ui/wizards/valuation/wiz_create_building_unit_valuation.ui \
        ../ui/wizards/valuation/wiz_create_geoeconomic_zone_valuation.ui \
        ../ui/wizards/valuation/wiz_create_physical_zone_valuation.ui

SOURCES = ../__init__.py \
          ../asistente_ladm_col_plugin.py \
          ../config/help_strings.py \
          ../config/mapping_config.py \
          ../config/task_steps_config.py \
          ../config/gui/change_detection_config.py \
          ../config/gui/gui_config.py \
          ../config/transitional_system_config.py \
          ../config/translation_strings.py \
          ../config/wizard_config.py \
          ../gui/change_detection/changes_all_parcels_panel.py \
          ../gui/change_detection/changes_per_parcel_panel.py \
          ../gui/change_detection/dlg_change_detection_settings.py \
          ../gui/change_detection/dockwidget_change_detection.py \
          ../gui/change_detection/parcels_changes_summary_panel.py \
          ../gui/change_detection/dlg_select_duplicate_parcel_change_detection.py \
          ../gui/db_panel/db_schema_db_panel.py \
          ../gui/db_panel/gpkg_config_panel.py \
          ../gui/dialogs/dlg_about.py \
          ../gui/dialogs/dlg_custom_model_dir.py \
          ../gui/dialogs/dlg_get_db_or_schema_name.py \
          ../gui/dialogs/dlg_import_from_excel.py \
          ../gui/dialogs/dlg_load_layers.py \
          ../gui/dialogs/dlg_log_excel.py \
          ../gui/dialogs/dlg_log_quality.py \
          ../gui/dialogs/dlg_quality.py \
          ../gui/dialogs/dlg_settings.py \
          ../gui/dialogs/dlg_upload_progress.py \
          ../gui/gui_builder/gui_builder.py \
          ../gui/gui_builder/role_registry.py \
          ../gui/qgis_model_baker/dlg_import_schema.py \
          ../gui/qgis_model_baker/dlg_import_data.py \
          ../gui/qgis_model_baker/dlg_export_data.py \
          ../gui/queries/dockwidget_queries.py \
          ../gui/reports/reports.py \
          ../gui/supplies/cobol_data_sources_widget.py \
          ../gui/supplies/dlg_cobol_base.py \
          ../gui/supplies/dlg_missing_cobol_supplies.py \
          ../gui/supplies/snc_data_sources_widget.py \
          ../gui/supplies/wiz_supplies_etl.py \
          ../gui/transitional_system/dlg_cancel_task.py \
          ../gui/transitional_system/dlg_login_st.py \
          ../gui/transitional_system/dlg_upload_file.py \
          ../gui/transitional_system/task_panel.py \
          ../gui/transitional_system/tasks_widget.py \
          ../gui/transitional_system/transitional_system_initial_panel.py \
          ../gui/wizards/operation/dlg_create_group_party_operation.py \
          ../gui/wizards/operation/wiz_create_ext_address_operation.py \
          ../gui/wizards/operation/wiz_create_parcel_operation.py \
          ../gui/wizards/operation/wiz_create_plot_operation.py \
          ../gui/wizards/operation/wiz_create_points_operation.py \
          ../gui/wizards/operation/wiz_create_right_of_way_operation.py \
          ../gui/wizards/operation/wiz_create_rrr_operation.py \
          ../gui/wizards/operation/wiz_create_spatial_source_operation.py \
          ../gui/wizards/valuation/wiz_create_building_unit_qualification_valuation.py \
          ../gui/wizards/valuation/wiz_create_building_unit_valuation.py \
          ../gui/wizards/abs_wizard_factory.py \
          ../gui/wizards/map_interaction_expansion.py \
          ../gui/wizards/multi_page_spatial_wizard_factory.py \
          ../gui/wizards/multi_page_wizard_factory.py \
          ../gui/wizards/select_features_on_map_wrapper.py \
          ../gui/wizards/single_page_spatial_wizard_factory.py \
          ../gui/wizards/single_page_wizard_factory.py \
          ../gui/wizards/spatial_wizard_factory.py \
          ../gui/wizards/wizard_factory.py \
          ../gui/right_of_way.py \
          ../gui/toolbar.py \
          ../lib/db/db_connector.py \
          ../lib/db/db_connection_manager.py \
          ../lib/db/gpkg_connector.py \
          ../lib/db/pg_connector.py \
          ../lib/processing/algs/InsertFeaturesToLayer.py \
          ../lib/processing/algs/PolygonsToLines.py \
          ../lib/transitional_system/st_session/st_session.py \
          ../lib/transitional_system/task_manager/task_manager.py \
          ../lib/transitional_system/task_manager/task_steps.py \
          ../lib/source_handler.py \
          ../logic/ladm_col/queries/per_component/pg/logic_validation_queries.py \
          ../logic/quality/logic_checks.py \
          ../logic/quality/quality.py \
          ../utils/decorators.py \
          ../utils/qgis_utils.py \
          ../utils/qt_utils.py \
          ../utils/java_utils.py \
          ../utils/model_parser.py \
          ../utils/qgis_model_baker_utils.py \
          ../utils/st_utils.py \
          ../utils/utils.py

TRANSLATIONS = Asistente-LADM_COL_es.ts
