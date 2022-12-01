from qgis.core import QgsWkbTypes

from asistente_ladm_col.config.ladm_names import LADMNames


class Symbology:
    @staticmethod
    def get_default_style_group(names, models):
        style_dict = dict()
        for model_key in models:
            if model_key == LADMNames.SURVEY_MODEL_KEY:
                if getattr(names, "LC_BOUNDARY_T", None):
                    style_dict[names.LC_BOUNDARY_T] = 'style_boundary'
                if getattr(names, "LC_BOUNDARY_POINT_T", None):
                    style_dict[names.LC_BOUNDARY_POINT_T] = 'style_boundary_point'
                if getattr(names, "LC_SURVEY_POINT_T", None):
                    style_dict[names.LC_SURVEY_POINT_T] = 'style_survey_point'
                if getattr(names, "LC_CONTROL_POINT_T", None):
                    style_dict[names.LC_CONTROL_POINT_T] = 'style_control_point'
                if getattr(names, "LC_PLOT_T", None):
                    style_dict[names.LC_PLOT_T] = 'style_plot_polygon'
                if getattr(names, "LC_BUILDING_T", None):
                    style_dict[names.LC_BUILDING_T] = 'style_building'
                if getattr(names, "LC_BUILDING_UNIT_T", None):
                    style_dict[names.LC_BUILDING_UNIT_T] = 'style_building_unit_25'
                if getattr(names, "LC_RIGHT_OF_WAY_T", None):
                    style_dict[names.LC_RIGHT_OF_WAY_T] = 'style_right_of_way'
            elif model_key == LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY:
                if getattr(names, "FDC_GENERAL_AREA_T", None):
                    style_dict[names.FDC_GENERAL_AREA_T] = 'style_general_area_fdc'
                if getattr(names, "FDC_SPECIFIC_AREA_T", None):
                    style_dict[names.FDC_SPECIFIC_AREA_T] = 'style_specific_area_fdc'
                if getattr(names, "FDC_BOUNDARY_T", None):
                    style_dict[names.FDC_BOUNDARY_T] = 'style_boundary'
                if getattr(names, "FDC_BOUNDARY_POINT_T", None):
                    style_dict[names.FDC_BOUNDARY_POINT_T] = 'style_boundary_point'
                if getattr(names, "FDC_SURVEY_POINT_T", None):
                    style_dict[names.FDC_SURVEY_POINT_T] = 'style_survey_point'
                if getattr(names, "FDC_CONTROL_POINT_T", None):
                    style_dict[names.FDC_CONTROL_POINT_T] = 'style_control_point'
                if getattr(names, "FDC_PLOT_T", None):
                    style_dict[names.FDC_PLOT_T] = 'style_plot_polygon'
                if getattr(names, "FDC_LEGACY_PLOT_T", None):
                    style_dict[names.FDC_LEGACY_PLOT_T] = 'style_plot_legacy_fdc'
                if getattr(names, "FDC_BUILDING_T", None):
                    style_dict[names.FDC_BUILDING_T] = 'style_building'
                if getattr(names, "FDC_LEGACY_BUILDING_T", None):
                    style_dict[names.FDC_LEGACY_BUILDING_T] = 'style_building_legacy_fdc'
                if getattr(names, "FDC_BUILDING_UNIT_T", None):
                    style_dict[names.FDC_BUILDING_UNIT_T] = 'style_building_unit_fdc'
                if getattr(names, "FDC_LEGACY_BUILDING_UNIT_T", None):
                    style_dict[names.FDC_LEGACY_BUILDING_UNIT_T] = 'style_building_unit_legacy_fdc'
                #if getattr(names, "FDC_PARCEL_T", None):
                #    style_dict[names.FDC_PARCEL_T] = 'style_parcel_fdc'
            elif model_key == LADMNames.QUALITY_ERROR_MODEL_KEY:
                if getattr(names, "ERR_POINT_T", None):
                    style_dict[names.ERR_POINT_T] = 'style_point_error'
                if getattr(names, "ERR_LINE_T", None):
                    style_dict[names.ERR_LINE_T] = 'style_line_error'
                if getattr(names, "ERR_POLYGON_T", None):
                    style_dict[names.ERR_POLYGON_T] = 'style_polygon_error'

        return style_dict

    @staticmethod
    def get_style_group_layer_modifiers(names):
        return {
            names.GC_PLOT_T: 'style_supplies_plot_polygon'
        }

    @staticmethod
    def get_style_informal_layers(names):
        return {
            names.LC_PLOT_T: 'style_informal_plots',
            names.LC_BUILDING_T: 'style_informal_buildings',
            names.LC_BUILDING_UNIT_T: 'style_informal_building_units'
        }
