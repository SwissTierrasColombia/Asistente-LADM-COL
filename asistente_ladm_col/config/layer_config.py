from qgis.core import NULL

from asistente_ladm_col.config.general_config import PLUGINS_DIR
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class LayerConfig:
    SUPPLIES_DB_PREFIX = None
    SUPPLIES_DB_SUFFIX = " (Insumos)"
    PREFIX_LAYER_MODIFIERS = 'prefix'
    SUFFIX_LAYER_MODIFIERS = 'suffix'
    STYLE_GROUP_LAYER_MODIFIERS = 'style_group'
    VISIBLE_LAYER_MODIFIERS = 'visible'

    @staticmethod
    def get_layer_constraints(names, models):
        layer_constraints = dict()

        for model_key in models:
            if model_key == LADMNames.SURVEY_MODEL_KEY:
                layer_constraints = {
                    names.LC_PARCEL_T: {
                        names.LC_PARCEL_T_PARCEL_TYPE_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PARCEL_T_PARCEL_TYPE_F}" =  get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}', True, False) THEN
                                                    num_selected('{LC_PLOT_T}') = 1 AND num_selected('{LC_BUILDING_UNIT_T}') = 0
                                                WHEN  "{LC_PARCEL_T_PARCEL_TYPE_F}" IN  (get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', True, False),
                                                                                  get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', True, False),
                                                                                  get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARENT}', True, False),
                                                                                  get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_PUBLIC_USE}', True, False),
                                                                                  get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}', True, False)) THEN
                                                    num_selected('{LC_PLOT_T}') = 1 AND num_selected('{LC_BUILDING_UNIT_T}') = 0
                                                WHEN  "{LC_PARCEL_T_PARCEL_TYPE_F}" IN  (get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_ROAD}', True, False),
                                                                                  get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}', True, False)) THEN
                                                    num_selected('{LC_PLOT_T}') = 1 AND num_selected('{LC_BUILDING_UNIT_T}') = 0 AND num_selected('{LC_BUILDING_T}') = 0
                                                WHEN  "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}', True, False) THEN
                                                    num_selected('{LC_PLOT_T}') = 0 AND num_selected('{LC_BUILDING_UNIT_T}') != 0 AND num_selected('{LC_BUILDING_T}') = 0
                                                WHEN  "{LC_PARCEL_T_PARCEL_TYPE_F}" IN (get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', True, False),
                                                                                 get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}', True, False)) THEN
                                                    num_selected('{LC_PLOT_T}') = 0 AND num_selected('{LC_BUILDING_UNIT_T}') = 0 AND num_selected('{LC_BUILDING_T}') = 1
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARCEL_T_PARCEL_TYPE_F=names.LC_PARCEL_T_PARCEL_TYPE_F,
                                                          LC_CONDITION_PARCEL_TYPE_D=names.LC_CONDITION_PARCEL_TYPE_D,
                                                          LC_PLOT_T=names.LC_PLOT_T,
                                                          LC_BUILDING_T=names.LC_BUILDING_T,
                                                          LC_BUILDING_UNIT_T=names.LC_BUILDING_UNIT_T,
                                                          PARCEL_TYPE_NO_HORIZONTAL_PROPERTY=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                                                          PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                                                          PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                                                          PARCEL_TYPE_CONDOMINIUM_PARENT=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT,
                                                          PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                                                          PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA,
                                                          PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                                                          PARCEL_TYPE_CEMETERY_PARENT=LADMNames.PARCEL_TYPE_CEMETERY_PARENT,
                                                          PARCEL_TYPE_CEMETERY_PARCEL_UNIT=LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                                                          PARCEL_TYPE_ROAD=LADMNames.PARCEL_TYPE_ROAD,
                                                          PARCEL_TYPE_PUBLIC_USE=LADMNames.PARCEL_TYPE_PUBLIC_USE),
                            'description': 'La parcela debe tener una o varias unidades espaciales asociadas. Verifique las reglas '
                            # ''Parcel must have one or more spatial units associated with it. Check the rules.'
                        },
                        names.LC_PARCEL_T_PARCEL_NUMBER_F: {
                            'expression': """CASE
                                                WHEN  "{LC_PARCEL_T_PARCEL_NUMBER_F}" IS NOT NULL THEN
                                                    CASE
                                                        WHEN length("{LC_PARCEL_T_PARCEL_NUMBER_F}") != 30 OR regexp_match(to_string("{LC_PARCEL_T_PARCEL_NUMBER_F}"), '^[0-9]*$') = 0  THEN
                                                            FALSE
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 0
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 9
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 9
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 8
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 8
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARENT}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 7
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 7
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 5
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 5
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_ROAD}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 4
                                                        WHEN "{LC_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{LC_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_PUBLIC_USE}', True, False) THEN
                                                            substr("{LC_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 3
                                                        ELSE
                                                            TRUE
                                                    END
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARCEL_T_PARCEL_TYPE_F=names.LC_PARCEL_T_PARCEL_TYPE_F,
                                                          LC_CONDITION_PARCEL_TYPE_D=names.LC_CONDITION_PARCEL_TYPE_D,
                                                          PARCEL_TYPE_NO_HORIZONTAL_PROPERTY=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                                                          PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                                                          PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                                                          PARCEL_TYPE_CONDOMINIUM_PARENT=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT,
                                                          PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                                                          PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA,
                                                          PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                                                          PARCEL_TYPE_CEMETERY_PARENT=LADMNames.PARCEL_TYPE_CEMETERY_PARENT,
                                                          PARCEL_TYPE_CEMETERY_PARCEL_UNIT=LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                                                          PARCEL_TYPE_ROAD=LADMNames.PARCEL_TYPE_ROAD,
                                                          PARCEL_TYPE_PUBLIC_USE=LADMNames.PARCEL_TYPE_PUBLIC_USE,
                                                          LC_PARCEL_T_PARCEL_NUMBER_F=names.LC_PARCEL_T_PARCEL_NUMBER_F),
                            'description': 'El campo debe tener 30 caracteres numéricos y la posición 22 debe coincidir con el tipo de predio.'
                        },
                        names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F: {
                            'expression': """CASE
                                                WHEN  "{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}" IS NULL THEN
                                                    TRUE
                                                WHEN length("{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}") != 20 OR regexp_match(to_string("{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}"), '^[0-9]*$') = 0 THEN
                                                    FALSE
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F=names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F),
                            'description': 'El campo debe tener 20 caracteres numéricos.'
                        },
                        names.LC_PARCEL_T_VALUATION_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PARCEL_T_VALUATION_F}" IS NULL THEN
                                                    TRUE
                                                WHEN  "{LC_PARCEL_T_VALUATION_F}" = 0 THEN
                                                    FALSE
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARCEL_T_VALUATION_F=names.LC_PARCEL_T_VALUATION_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        }
                    },
                    names.LC_PARTY_T: {
                        names.LC_PARTY_T_DOCUMENT_TYPE_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PARTY_T_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                                     "{LC_PARTY_T_DOCUMENT_TYPE_F}" !=  get_domain_code_from_value('{LC_PARTY_DOCUMENT_TYPE_D}', '{LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}', True, False)
                                                WHEN  "{LC_PARTY_T_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                                     "{LC_PARTY_T_DOCUMENT_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_DOCUMENT_TYPE_D}', '{LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}', True, False)
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARTY_T_TYPE_F=names.LC_PARTY_T_TYPE_F,
                                                          LC_PARTY_TYPE_D=names.LC_PARTY_TYPE_D,
                                                          LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                          LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                          LC_PARTY_DOCUMENT_TYPE_D=names.LC_PARTY_DOCUMENT_TYPE_D,
                                                          LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V=LADMNames.LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                                                          LC_PARTY_T_DOCUMENT_TYPE_F=names.LC_PARTY_T_DOCUMENT_TYPE_F),
                            'description': 'Si el tipo de interesado es "Persona Natural" entonces el tipo de documento debe ser diferente de \'NIT\'. Pero si el tipo de interesado es "Persona No Natural" entonces el tipo de documento debe ser \'NIT\' o \'Secuencial IGAC\' o \'Secuencial SNR\'. '
                        },
                        names.LC_PARTY_T_FIRST_NAME_1_F: {
                            'expression': """
                                        CASE
                                            WHEN  "{LC_PARTY_T_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False)  THEN
                                                 "{LC_PARTY_T_FIRST_NAME_1_F}" IS NOT NULL AND length(trim("{LC_PARTY_T_FIRST_NAME_1_F}")) != 0
                                            WHEN  "{LC_PARTY_T_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False)  THEN
                                                 "{LC_PARTY_T_FIRST_NAME_1_F}" IS NULL
                                            ELSE
                                                TRUE
                                        END""".format(LC_PARTY_T_TYPE_F=names.LC_PARTY_T_TYPE_F,
                                                      LC_PARTY_TYPE_D=names.LC_PARTY_TYPE_D,
                                                      LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                      LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                      LC_PARTY_T_FIRST_NAME_1_F=names.LC_PARTY_T_FIRST_NAME_1_F),
                            'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
                        },
                        names.LC_PARTY_T_SURNAME_1_F: {
                            'expression': """
                                CASE
                                    WHEN  "{LC_PARTY_T_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                         "{LC_PARTY_T_SURNAME_1_F}" IS NOT NULL AND length(trim("{LC_PARTY_T_SURNAME_1_F}")) != 0
                                    WHEN  "{LC_PARTY_T_TYPE_F}" = get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                         "{LC_PARTY_T_SURNAME_1_F}" IS NULL
                                    ELSE
                                        TRUE
                                END""".format(LC_PARTY_T_TYPE_F=names.LC_PARTY_T_TYPE_F,
                                              LC_PARTY_TYPE_D=names.LC_PARTY_TYPE_D,
                                              LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                              LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                              LC_PARTY_T_SURNAME_1_F=names.LC_PARTY_T_SURNAME_1_F),
                            'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
                        },
                        names.LC_PARTY_T_BUSINESS_NAME_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PARTY_T_TYPE_F}" =  get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                                     "{LC_PARTY_T_BUSINESS_NAME_F}" IS NOT NULL AND  length(trim( "{LC_PARTY_T_BUSINESS_NAME_F}")) != 0
                                                WHEN  "{LC_PARTY_T_TYPE_F}" =  get_domain_code_from_value('{LC_PARTY_TYPE_D}', '{LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                                     "{LC_PARTY_T_BUSINESS_NAME_F}" IS NULL
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARTY_T_TYPE_F=names.LC_PARTY_T_TYPE_F,
                                                          LC_PARTY_TYPE_D=names.LC_PARTY_TYPE_D,
                                                          LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                          LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                          LC_PARTY_T_BUSINESS_NAME_F=names.LC_PARTY_T_BUSINESS_NAME_F),
                            'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

                        },
                        names.LC_PARTY_T_DOCUMENT_ID_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PARTY_T_DOCUMENT_ID_F}"  IS NULL THEN
                                                    FALSE
                                                WHEN length(trim("{LC_PARTY_T_DOCUMENT_ID_F}")) = 0 THEN
                                                    FALSE
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PARTY_T_DOCUMENT_ID_F=names.LC_PARTY_T_DOCUMENT_ID_F),
                            'description': 'El campo es obligatorio.'

                        }
                    },
                    names.LC_PLOT_T: {
                        names.LC_PLOT_T_PLOT_AREA_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PLOT_T_PLOT_AREA_F}" IS NULL THEN
                                                    FALSE
                                                WHEN  "{LC_PLOT_T_PLOT_AREA_F}" = 0 THEN
                                                    FALSE
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PLOT_T_PLOT_AREA_F=names.LC_PLOT_T_PLOT_AREA_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        },
                        names.LC_PLOT_T_PLOT_VALUATION_F: {
                            'expression': """
                                            CASE
                                                WHEN  "{LC_PLOT_T_PLOT_VALUATION_F}" IS NULL THEN
                                                    FALSE
                                                WHEN  "{LC_PLOT_T_PLOT_VALUATION_F}" = 0 THEN
                                                    FALSE
                                                ELSE
                                                    TRUE
                                            END""".format(LC_PLOT_T_PLOT_VALUATION_F=names.LC_PLOT_T_PLOT_VALUATION_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        }
                    },
                    names.LC_BUILDING_T: {
                        names.LC_BUILDING_T_BUILDING_AREA_F: {
                            'expression': """
                                    CASE
                                        WHEN  "{LC_BUILDING_T_BUILDING_AREA_F}" IS NULL THEN
                                            TRUE
                                        WHEN  "{LC_BUILDING_T_BUILDING_AREA_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(LC_BUILDING_T_BUILDING_AREA_F=names.LC_BUILDING_T_BUILDING_AREA_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        },
                        names.LC_BUILDING_T_BUILDING_VALUATION_F: {
                            'expression': """
                                    CASE
                                        WHEN  "{LC_BUILDING_T_BUILDING_VALUATION_F}" IS NULL THEN
                                            FALSE
                                        WHEN  "{LC_BUILDING_T_BUILDING_VALUATION_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(LC_BUILDING_T_BUILDING_VALUATION_F=names.LC_BUILDING_T_BUILDING_VALUATION_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        }
                    },
                    names.LC_BUILDING_UNIT_T: {
                        names.LC_BUILDING_UNIT_T_BUILT_AREA_F: {
                            'expression': """
                                    CASE
                                        WHEN  "{LC_BUILDING_UNIT_T_BUILT_AREA_F}" IS NULL THEN
                                            TRUE
                                        WHEN  "{LC_BUILDING_UNIT_T_BUILT_AREA_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(LC_BUILDING_UNIT_T_BUILT_AREA_F=names.LC_BUILDING_UNIT_T_BUILT_AREA_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        },
                        names.LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F: {
                            'expression': """
                                    CASE
                                        WHEN  "{LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}" IS NULL THEN
                                            TRUE
                                        WHEN  "{LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F=names.LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        },
                        names.LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F: {
                            'expression': """
                                    CASE
                                        WHEN  "{LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F}" IS NULL THEN
                                            TRUE
                                        WHEN  "{LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F=names.LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F),
                            'description': 'El valor debe ser mayor a cero (0).'
                        }
                    }
                }

        return layer_constraints

    @staticmethod
    def get_constraint_types_of_parcels(names):
        # Operations:
        # 1 = One and only one feature must be selected
        # + = One or more features must be selected
        # * = Optional, i.e., zero or more features could be selected
        # None = Won't be stored as a related feature (selected features will be ignored)
        return {
            LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: '*'
            },
            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT: {
                names.LC_PLOT_T: None,
                names.LC_BUILDING_T: None,
                names.LC_BUILDING_UNIT_T: '+'
            },
            LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA: {
                names.LC_PLOT_T: None,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: '+'
            },
            LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA: {
                names.LC_PLOT_T: None,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: '+'
            },
            LADMNames.PARCEL_TYPE_CEMETERY_PARENT: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: None,
                names.LC_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_ROAD: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: None,
                names.LC_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_PUBLIC_USE: {
                names.LC_PLOT_T: 1,
                names.LC_BUILDING_T: '*',
                names.LC_BUILDING_UNIT_T: None
            }
        }

    @staticmethod
    def get_dict_package_icon():
        """
        LADM PACKAGE ICONS
        """
        return {
            # Resources don't seem to be initialized at this point, so return path and build icon when needed
            LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE: ":/Asistente-LADM-COL/resources/images/surveying.png",
            LADMNames.SPATIAL_UNIT_PACKAGE: ":/Asistente-LADM-COL/resources/images/spatial_unit.png",
            LADMNames.BA_UNIT_PACKAGE: ":/Asistente-LADM-COL/resources/images/ba_unit.png",
            LADMNames.RRR_PACKAGE: ":/Asistente-LADM-COL/resources/images/rrr.png",
            LADMNames.PARTY_PACKAGE: ":/Asistente-LADM-COL/resources/images/party.png",
            LADMNames.SOURCE_PACKAGE: ":/Asistente-LADM-COL/resources/images/source.png"
        }

    @staticmethod
    def get_dict_table_package(names):
        return {
            names.LC_PARCEL_T: LADMNames.BA_UNIT_PACKAGE,
            names.LC_PLOT_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.LC_BUILDING_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.LC_BUILDING_UNIT_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.LC_RIGHT_OF_WAY_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.LC_PARTY_T: LADMNames.PARTY_PACKAGE,
            names.LC_GROUP_PARTY_T: LADMNames.PARTY_PACKAGE,
            names.LC_RIGHT_T: LADMNames.RRR_PACKAGE,
            names.LC_RESTRICTION_T: LADMNames.RRR_PACKAGE,
            names.LC_ADMINISTRATIVE_SOURCE_T: LADMNames.SOURCE_PACKAGE,
            names.LC_SPATIAL_SOURCE_T: LADMNames.SOURCE_PACKAGE,
            names.LC_BOUNDARY_POINT_T: LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE,
            names.LC_SURVEY_POINT_T: LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE,
            names.LC_BOUNDARY_T: LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE
        }

    @staticmethod
    def get_dict_automatic_values(db, layer_name, models):
        names = db.names
        ladm_data = LADMData()

        dict_automatic_values = dict()

        for model_key in models:
            if model_key == LADMNames.SURVEY_MODEL_KEY:
                if layer_name == names.LC_BOUNDARY_T:
                    dict_automatic_values = {names.LC_BOUNDARY_T_LENGTH_F: "$length"}
                elif layer_name == names.LC_PARTY_T:
                    dict_automatic_values = {
                        names.COL_PARTY_T_NAME_F: """
                            CASE
                                WHEN {party_type} = get_domain_code_from_value('{domain_party_type}', '{LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False)  THEN
                                    concat({surname_1}, ' ', {surname_2}, ' ', {first_name_1}, ' ', {first_name_2})
                                WHEN {party_type} = get_domain_code_from_value('{domain_party_type}', '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                    {business_name}
                            END
                        """.format(party_type=names.LC_PARTY_T_TYPE_F,
                                   domain_party_type=names.LC_PARTY_TYPE_D,
                                   surname_1=names.LC_PARTY_T_SURNAME_1_F,
                                   surname_2=names.LC_PARTY_T_SURNAME_2_F,
                                   first_name_1=names.LC_PARTY_T_FIRST_NAME_1_F,
                                   first_name_2=names.LC_PARTY_T_FIRST_NAME_2_F,
                                   business_name=names.LC_PARTY_T_BUSINESS_NAME_F,
                                   LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                   LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V),
                        names.LC_PARTY_T_TYPE_F: "{}".format(ladm_data.get_domain_code_from_value(db,
                                                                                                  names.LC_PARTY_TYPE_D,
                                                                                                  LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V)),
                        names.LC_PARTY_T_ETHNIC_GROUP_F: "{}".format(ladm_data.get_domain_code_from_value(db,
                                                                                                          names.LC_ETHNIC_GROUP_TYPE_D,
                                                                                                          LADMNames.LC_PARTY_ETHNIC_GROUP_TYPE_D_NONE_V))
                    }
                elif layer_name == names.LC_PARCEL_T:
                    dict_automatic_values = {
                        names.LC_PARCEL_T_DEPARTMENT_F: 'substr("{}", 0, 2)'.format(names.LC_PARCEL_T_PARCEL_NUMBER_F),
                        names.LC_PARCEL_T_MUNICIPALITY_F: 'substr("{}", 3, 3)'.format(names.LC_PARCEL_T_PARCEL_NUMBER_F)
                    }
                elif layer_name == names.LC_ADMINISTRATIVE_SOURCE_T:
                    dict_automatic_values = {
                        names.COL_SOURCE_T_MAIN_TYPE_F: "{}".format(ladm_data.get_domain_code_from_value(db,
                                                                                                         names.CI_CODE_PRESENTATION_FORM_D,
                                                                                                         LADMNames.CI_CODE_PRESENTATION_FORM_D_DOCUMENT_V))
                    }
            elif model_key == LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY:
                if layer_name == names.FDC_USER_T:
                    dict_automatic_values = {names.FDC_USER_T_DOCUMENT_TYPE_F: "{}".format(
                        ladm_data.get_domain_code_from_value(db,
                                                             names.FDC_PARTY_DOCUMENT_TYPE_D,
                                                             LADMNames.FDC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_CC_V))}

        return dict_automatic_values

    @staticmethod
    def get_layer_variables(names, models):
        layer_variables = dict()

        for model_key in models:
            if model_key == LADMNames.SURVEY_MODEL_KEY:
                layer_variables.update({
                    names.LC_BUILDING_T: {
                        "qgis_25d_angle": 90,
                        "qgis_25d_height": 1
                    },
                    names.LC_BUILDING_UNIT_T: {
                            "qgis_25d_angle": 90,
                            "qgis_25d_height": 'coalesce("{}", 0) * 2.5'.format(
                                names.LC_BUILDING_UNIT_T_TOTAL_FLOORS_F)
                    }})

        return layer_variables

    @staticmethod
    def get_layer_sets(names, models):
        """
        Configure layer sets to appear in the load layers dialog
        Each layer set is a key-value pair where key is the name of the layer set
        and the value is a list of layers to load
        """
        layer_sets = dict()

        for model_key in models:
            if model_key == LADMNames.SURVEY_MODEL_KEY:
                layer_sets.update({
                    'Datos de Interesados': [
                        names.LC_PARTY_T,
                        names.LC_GENRE_D,
                        names.LC_PARTY_DOCUMENT_TYPE_D,
                        names.LC_PARTY_TYPE_D
                    ],
                    'Derechos': [
                        names.LC_PARTY_T,
                        names.LC_PARCEL_T,
                        names.LC_ADMINISTRATIVE_SOURCE_T,
                        names.EXT_ARCHIVE_S,
                        names.LC_GROUP_PARTY_T,
                        names.LC_RIGHT_T
                    ],
                    'Punto Lindero, Lindero y Terreno': [
                        names.LC_BOUNDARY_POINT_T,
                        names.LC_BOUNDARY_T,
                        names.LC_PLOT_T,
                        names.MORE_BFS_T,
                        names.LESS_BFS_T,
                        names.POINT_BFS_T
                    ]
                })

        return layer_sets

    @staticmethod
    def get_tables_to_ignore(names, models):
        tables_to_ignore = list()
        for model_key in models:
            if model_key == LADMNames.SURVEY_MODEL_KEY:
                tables_to_ignore = [names.LC_NU_GROUP_SPATIAL_UNIT_T,
                                    names.LC_NU_BOUNDARY_FACE_T,
                                    names.LC_NU_LEGAL_SPACE_SERVICE_NETWORK_T,
                                    names.LC_NU_LEGAL_SPACE_BUILDING_UNIT_T,
                                    names.LC_NU_LEVEL_T,
                                    names.LC_NU_REQUIRED_RELATION_BAUNITS_T,
                                    names.LC_NU_REQUIRED_RELATION_SPATIAL_UNITS_T]

        return tables_to_ignore


    @staticmethod
    def get_dict_plural(names):
        """
        PLURAL WORDS, FOR DISPLAY PURPOSES
        """
        return {
            names.LC_PLOT_T: "Terrenos",
            names.LC_PARCEL_T: "Predios",
            names.LC_BUILDING_T: "Construcciones",
            names.LC_BUILDING_UNIT_T: "Unidades de Construcción",
            names.EXT_ADDRESS_S: "Direcciones",
            names.LC_PARTY_T: "Interesados",
            names.LC_GROUP_PARTY_T: "Agrupación de interesados",
            names.LC_RIGHT_T: "Derechos",
            names.LC_RESTRICTION_T: "Restricciones",
            names.LC_ADMINISTRATIVE_SOURCE_T: "Fuentes Administrativas",
            names.LC_SPATIAL_SOURCE_T: "Fuentes Espaciales",
            names.LC_BOUNDARY_T: "Linderos",
            names.LC_BOUNDARY_POINT_T: "Puntos de Lindero",
            names.LC_SURVEY_POINT_T: "Puntos de Levantamiento"
        }

    @staticmethod
    def get_logic_consistency_tables(names):
        """
        we define the minimum structure of a table to validate that there are no repeated records
        """
        return {
            # Geometric tables
            names.LC_BOUNDARY_POINT_T: [names.LC_BOUNDARY_POINT_T_AGREEMENT_F,
                                        names.LC_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F,
                                        names.LC_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F,
                                        names.LC_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F,
                                        names.COL_POINT_T_INTERPOLATION_POSITION_F,
                                        names.COL_POINT_T_PRODUCTION_METHOD_F,
                                        names.LC_BOUNDARY_POINT_T_POINT_TYPE_F,
                                        names.COL_POINT_T_ORIGINAL_LOCATION_F],
            names.LC_SURVEY_POINT_T: [names.LC_SURVEY_POINT_T_SURVEY_POINT_TYPE_F,
                                      names.LC_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F,
                                      names.LC_SURVEY_POINT_T_VERTICAL_ACCURACY_F,
                                      names.LC_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F,
                                      names.COL_POINT_T_INTERPOLATION_POSITION_F,
                                      names.COL_POINT_T_PRODUCTION_METHOD_F,
                                      names.LC_SURVEY_POINT_T_POINT_TYPE_F,
                                      names.COL_POINT_T_ORIGINAL_LOCATION_F],
            names.LC_CONTROL_POINT_T: [names.LC_CONTROL_POINT_T_VERTICAL_ACCURACY_F,
                                       names.LC_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F,
                                       names.LC_CONTROL_POINT_T_ID_F,
                                       names.COL_POINT_T_INTERPOLATION_POSITION_F,
                                       names.LC_CONTROL_POINT_T_POINT_TYPE_F,
                                       names.COL_POINT_T_ORIGINAL_LOCATION_F],
            names.LC_BOUNDARY_T: [names.LC_BOUNDARY_T_LENGTH_F,
                                  names.COL_BFS_T_TEXTUAL_LOCATION_F,
                                  names.COL_BFS_T_GEOMETRY_F],
            names.LC_PLOT_T: [names.LC_PLOT_T_PLOT_AREA_F,
                              names.LC_PLOT_T_PLOT_VALUATION_F,
                              names.COL_SPATIAL_UNIT_T_DIMENSION_F,
                              names.COL_SPATIAL_UNIT_T_LABEL_F,
                              names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                              names.LC_PLOT_T_GEOMETRY_F],
            names.LC_BUILDING_T: [names.LC_BUILDING_T_BUILDING_VALUATION_F,
                                  names.LC_BUILDING_T_BUILDING_AREA_F,
                                  names.COL_SPATIAL_UNIT_T_DIMENSION_F,
                                  names.COL_SPATIAL_UNIT_T_LABEL_F,
                                  names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                                  names.COL_SPATIAL_UNIT_T_GEOMETRY_F],
            names.LC_BUILDING_UNIT_T: [names.LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F,
                                       names.LC_BUILDING_UNIT_T_TOTAL_FLOORS_F,
                                       names.LC_BUILDING_UNIT_T_BUILT_AREA_F,
                                       names.LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F,
                                       names.LC_BUILDING_UNIT_T_BUILDING_F,
                                       names.COL_SPATIAL_UNIT_T_DIMENSION_F,
                                       names.COL_SPATIAL_UNIT_T_LABEL_F,
                                       names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                                       names.COL_SPATIAL_UNIT_T_GEOMETRY_F],
            # Alphanumeric tables
            names.LC_PARTY_T: [names.LC_PARTY_T_DOCUMENT_ID_F,
                               names.LC_PARTY_T_DOCUMENT_TYPE_F],
            names.LC_PARCEL_T: [names.LC_PARCEL_T_DEPARTMENT_F,
                                names.LC_PARCEL_T_MUNICIPALITY_F,
                                names.LC_PARCEL_T_NUPRE_F,
                                names.LC_PARCEL_T_ID_OPERATION_F,
                                names.LC_PARCEL_T_FMI_F,
                                names.LC_PARCEL_T_PARCEL_NUMBER_F,
                                names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F,
                                names.LC_PARCEL_T_VALUATION_F,
                                names.COL_BAUNIT_T_NAME_F,
                                names.LC_PARCEL_T_PARCEL_TYPE_F],
            names.LC_RIGHT_T: [names.LC_RIGHT_T_TYPE_F,
                               names.COL_RRR_T_DESCRIPTION_F,
                               names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F,
                               names.COL_RRR_PARTY_T_LC_PARTY_F,
                               names.COL_BAUNIT_RRR_T_UNIT_F],
            names.LC_RESTRICTION_T: [names.LC_RESTRICTION_T_TYPE_F,
                                     names.COL_RRR_T_DESCRIPTION_F,
                                     names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F,
                                     names.COL_RRR_PARTY_T_LC_PARTY_F,
                                     names.COL_BAUNIT_RRR_T_UNIT_F],
            names.LC_ADMINISTRATIVE_SOURCE_T: [names.LC_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F,
                                               names.COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F,
                                               names.COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F,
                                               names.LC_ADMINISTRATIVE_SOURCE_T_TYPE_F,
                                               names.COL_SOURCE_T_DATE_DOCUMENT_F,
                                               names.COL_SOURCE_T_AVAILABILITY_STATUS_F,
                                               names.COL_SOURCE_T_MAIN_TYPE_F]
        }

    @staticmethod
    def get_custom_widget_configuration(names, models):
        widget_config = dict()

        for model_key in models:
            if model_key == LADMNames.LADM_COL_MODEL_KEY:
                if getattr(names, "EXT_ARCHIVE_S", None):
                    widget_config.update({
                        names.EXT_ARCHIVE_S: {
                            'type': 'ExternalResource',
                            'config': {
                                'PropertyCollection': {
                                    'properties': {},
                                    'name': NULL,
                                    'type': 'collection'
                                },
                                'UseLink': True,
                                'FullUrl': True,
                                'FileWidget': True,
                                'DocumentViewer': 0,
                                'RelativeStorage': 0,
                                'StorageMode': 0,
                                'FileWidgetButton': True,
                                'DocumentViewerHeight': 0,
                                'DocumentViewerWidth': 0,
                                'FileWidgetFilter': ''
                            }
                        }
                    })

        return widget_config

    @staticmethod
    def get_custom_read_only_fields(names):
        # Read only fields might be declared in two scenarios:
        #   1. As soon as the layer is loaded (e.g., LC_PARCEL_T_DEPARTMENT_F)
        #   2. Only for a wizard (e.g., PARCEL_TYPE)
        # WARNING: Both modes are exclusive, if you list a field in 1, it shouldn't be in 2. and viceversa!
        return {
            #names.LC_PARCEL_T: [names.LC_PARCEL_T_DEPARTMENT_F,
            #                    names.LC_PARCEL_T_MUNICIPALITY_F]  # list of fields of the layer to block its edition
        }
