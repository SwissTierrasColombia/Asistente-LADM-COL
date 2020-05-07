from qgis.core import NULL
from asistente_ladm_col.config.ladm_names import LADMNames


class LayerConfig:

    SUPPLIES_DB_PREFIX = None
    SUPPLIES_DB_SUFFIX = " (Insumos)"
    PREFIX_LAYER_MODIFIERS = 'prefix'
    SUFFIX_LAYER_MODIFIERS = 'suffix'
    STYLE_GROUP_LAYER_MODIFIERS = 'style_group'
    VISIBLE_LAYER_MODIFIERS = 'visible'

    @staticmethod
    def get_layer_constraints(names):
        return {
            names.OP_PARCEL_T: {
                names.OP_PARCEL_T_PARCEL_TYPE_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARCEL_T_PARCEL_TYPE_F}" =  get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}', True, False) THEN
                                            num_selected('{OP_PLOT_T}') = 1 AND num_selected('{OP_BUILDING_UNIT_T}') = 0
                                        WHEN  "{OP_PARCEL_T_PARCEL_TYPE_F}" IN  (get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', True, False),
                                                                          get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', True, False),
                                                                          get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARENT}', True, False),
                                                                          get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_PUBLIC_USE}', True, False),
                                                                          get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}', True, False)) THEN
                                            num_selected('{OP_PLOT_T}') = 1 AND num_selected('{OP_BUILDING_UNIT_T}') = 0
                                        WHEN  "{OP_PARCEL_T_PARCEL_TYPE_F}" IN  (get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_ROAD}', True, False),
                                                                          get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}', True, False)) THEN
                                            num_selected('{OP_PLOT_T}') = 1 AND num_selected('{OP_BUILDING_UNIT_T}') = 0 AND num_selected('{OP_BUILDING_T}') = 0
                                        WHEN  "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}', True, False) THEN
                                            num_selected('{OP_PLOT_T}') = 0 AND num_selected('{OP_BUILDING_UNIT_T}') != 0 AND num_selected('{OP_BUILDING_T}') = 0
                                        WHEN  "{OP_PARCEL_T_PARCEL_TYPE_F}" IN (get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', True, False),
                                                                         get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}', True, False)) THEN
                                            num_selected('{OP_PLOT_T}') = 0 AND num_selected('{OP_BUILDING_UNIT_T}') = 0 AND num_selected('{OP_BUILDING_T}') = 1
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_PARCEL_TYPE_F=names.OP_PARCEL_T_PARCEL_TYPE_F,
                                                  OP_CONDITION_PARCEL_TYPE_D=names.OP_CONDITION_PARCEL_TYPE_D,
                                                  OP_PLOT_T=names.OP_PLOT_T,
                                                  OP_BUILDING_T=names.OP_BUILDING_T,
                                                  OP_BUILDING_UNIT_T=names.OP_BUILDING_UNIT_T,
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
                names.OP_PARCEL_T_PARCEL_NUMBER_F: {
                    'expression': """CASE
                                        WHEN  "{OP_PARCEL_T_PARCEL_NUMBER_F}" IS NOT NULL THEN
                                            CASE
                                                WHEN length("{OP_PARCEL_T_PARCEL_NUMBER_F}") != 30 OR regexp_match(to_string("{OP_PARCEL_T_PARCEL_NUMBER_F}"), '^[0-9]*$') = 0  THEN
                                                    FALSE
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 0
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 9
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 9
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 8
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 8
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARENT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 7
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 7
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 5
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 5
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_ROAD}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 4
                                                WHEN "{OP_PARCEL_T_PARCEL_TYPE_F}" = get_domain_code_from_value('{OP_CONDITION_PARCEL_TYPE_D}', '{PARCEL_TYPE_PUBLIC_USE}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 3
                                                ELSE
                                                    TRUE
                                            END
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_PARCEL_TYPE_F=names.OP_PARCEL_T_PARCEL_TYPE_F,
                                                  OP_CONDITION_PARCEL_TYPE_D=names.OP_CONDITION_PARCEL_TYPE_D,
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
                                                  OP_PARCEL_T_PARCEL_NUMBER_F=names.OP_PARCEL_T_PARCEL_NUMBER_F),
                    'description': 'El campo debe tener 30 caracteres numéricos y la posición 22 debe coincidir con el tipo de predio.'
                },
                names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F: {
                    'expression': """CASE
                                        WHEN  "{OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}" IS NULL THEN
                                            TRUE
                                        WHEN length("{OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}") != 20 OR regexp_match(to_string("{OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}"), '^[0-9]*$') = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F=names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F),
                    'description': 'El campo debe tener 20 caracteres numéricos.'
                },
                names.OP_PARCEL_T_VALUATION_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARCEL_T_VALUATION_F}" IS NULL THEN
                                            TRUE
                                        WHEN  "{OP_PARCEL_T_VALUATION_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_VALUATION_F=names.OP_PARCEL_T_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            },
            names.OP_PARTY_T: {
                names.OP_PARTY_T_DOCUMENT_TYPE_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_DOCUMENT_TYPE_F}" !=  get_domain_code_from_value('{OP_PARTY_DOCUMENT_TYPE_D}', '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}', True, False)
                                        WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_DOCUMENT_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_DOCUMENT_TYPE_D}', '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}', True, False)
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARTY_T_TYPE_F=names.OP_PARTY_T_TYPE_F,
                                                  OP_PARTY_TYPE_D=names.OP_PARTY_TYPE_D,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                  OP_PARTY_DOCUMENT_TYPE_D=names.OP_PARTY_DOCUMENT_TYPE_D,
                                                  OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V=LADMNames.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                                                  OP_PARTY_T_DOCUMENT_TYPE_F=names.OP_PARTY_T_DOCUMENT_TYPE_F),
                    'description': 'Si el tipo de interesado es "Persona Natural" entonces el tipo de documento debe ser diferente de \'NIT\'. Pero si el tipo de interesado es "Persona No Natural" entonces el tipo de documento debe ser \'NIT\' o \'Secuencial IGAC\' o \'Secuencial SNR\'. '
                },
                names.OP_PARTY_T_FIRST_NAME_1_F: {
                    'expression': """
                                CASE
                                    WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False)  THEN
                                         "{OP_PARTY_T_FIRST_NAME_1_F}" IS NOT NULL AND length(trim("{OP_PARTY_T_FIRST_NAME_1_F}")) != 0
                                    WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False)  THEN
                                         "{OP_PARTY_T_FIRST_NAME_1_F}" IS NULL
                                    ELSE
                                        TRUE
                                END""".format(OP_PARTY_T_TYPE_F=names.OP_PARTY_T_TYPE_F,
                                              OP_PARTY_TYPE_D=names.OP_PARTY_TYPE_D,
                                              OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                              OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                              OP_PARTY_T_FIRST_NAME_1_F=names.OP_PARTY_T_FIRST_NAME_1_F),
                    'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
                },
                names.OP_PARTY_T_SURNAME_1_F: {
                    'expression': """
                        CASE
                            WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                 "{OP_PARTY_T_SURNAME_1_F}" IS NOT NULL AND length(trim("{OP_PARTY_T_SURNAME_1_F}")) != 0
                            WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                 "{OP_PARTY_T_SURNAME_1_F}" IS NULL
                            ELSE
                                TRUE
                        END""".format(OP_PARTY_T_TYPE_F=names.OP_PARTY_T_TYPE_F,
                                      OP_PARTY_TYPE_D=names.OP_PARTY_TYPE_D,
                                      OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                      OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                      OP_PARTY_T_SURNAME_1_F=names.OP_PARTY_T_SURNAME_1_F),
                    'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
                },
                names.OP_PARTY_T_BUSINESS_NAME_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARTY_T_TYPE_F}" =  get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_BUSINESS_NAME_F}" IS NOT NULL AND  length(trim( "{OP_PARTY_T_BUSINESS_NAME_F}")) != 0
                                        WHEN  "{OP_PARTY_T_TYPE_F}" =  get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_BUSINESS_NAME_F}" IS NULL
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARTY_T_TYPE_F=names.OP_PARTY_T_TYPE_F,
                                                  OP_PARTY_TYPE_D=names.OP_PARTY_TYPE_D,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                  OP_PARTY_T_BUSINESS_NAME_F=names.OP_PARTY_T_BUSINESS_NAME_F),
                    'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

                },
                names.OP_PARTY_T_DOCUMENT_ID_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARTY_T_DOCUMENT_ID_F}"  IS NULL THEN
                                            FALSE
                                        WHEN length(trim("{OP_PARTY_T_DOCUMENT_ID_F}")) = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARTY_T_DOCUMENT_ID_F=names.OP_PARTY_T_DOCUMENT_ID_F),
                    'description': 'El campo es obligatorio.'

                }
            },
            names.OP_PLOT_T: {
                names.OP_PLOT_T_PLOT_AREA_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PLOT_T_PLOT_AREA_F}" IS NULL THEN
                                            FALSE
                                        WHEN  "{OP_PLOT_T_PLOT_AREA_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PLOT_T_PLOT_AREA_F=names.OP_PLOT_T_PLOT_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                names.OP_PLOT_T_PLOT_VALUATION_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PLOT_T_PLOT_VALUATION_F}" IS NULL THEN
                                            FALSE
                                        WHEN  "{OP_PLOT_T_PLOT_VALUATION_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PLOT_T_PLOT_VALUATION_F=names.OP_PLOT_T_PLOT_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            },
            names.OP_BUILDING_T: {
                names.OP_BUILDING_T_BUILDING_AREA_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_T_BUILDING_AREA_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_T_BUILDING_AREA_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_T_BUILDING_AREA_F=names.OP_BUILDING_T_BUILDING_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                names.OP_BUILDING_T_BUILDING_VALUATION_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_T_BUILDING_VALUATION_F}" IS NULL THEN
                                    FALSE
                                WHEN  "{OP_BUILDING_T_BUILDING_VALUATION_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_T_BUILDING_VALUATION_F=names.OP_BUILDING_T_BUILDING_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            },
            names.OP_BUILDING_UNIT_T: {
                names.OP_BUILDING_UNIT_T_BUILT_AREA_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_AREA_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_AREA_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_UNIT_T_BUILT_AREA_F=names.OP_BUILDING_UNIT_T_BUILT_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F=names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                names.OP_BUILDING_UNIT_T_BUILDING_VALUATION_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILDING_VALUATION_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILDING_VALUATION_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_UNIT_T_BUILDING_VALUATION_F=names.OP_BUILDING_UNIT_T_BUILDING_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            }
        }

    @staticmethod
    def get_constraint_types_of_parcels(names):
        # Operations:
        # 1 = One and only one feature must be selected
        # + = One or more features must be selected
        # * = Optional, i.e., zero or more features could be selected
        # None = Won't be stored as a related feature (selected features will be ignored)
        return {
            LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: '*'
            },
            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT: {
                names.OP_PLOT_T: None,
                names.OP_BUILDING_T: None,
                names.OP_BUILDING_UNIT_T: '+'
            },
            LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA: {
                names.OP_PLOT_T: None,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: '+'
            },
            LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA: {
                names.OP_PLOT_T: None,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: '+'
            },
            LADMNames.PARCEL_TYPE_CEMETERY_PARENT: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: None,
                names.OP_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_ROAD: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: None,
                names.OP_BUILDING_UNIT_T: None
            },
            LADMNames.PARCEL_TYPE_PUBLIC_USE: {
                names.OP_PLOT_T: 1,
                names.OP_BUILDING_T: '*',
                names.OP_BUILDING_UNIT_T: None
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
            names.OP_PARCEL_T: LADMNames.BA_UNIT_PACKAGE,
            names.OP_PLOT_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.OP_BUILDING_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.OP_BUILDING_UNIT_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.OP_RIGHT_OF_WAY_T: LADMNames.SPATIAL_UNIT_PACKAGE,
            names.OP_PARTY_T: LADMNames.PARTY_PACKAGE,
            names.OP_GROUP_PARTY_T: LADMNames.PARTY_PACKAGE,
            names.OP_RIGHT_T: LADMNames.RRR_PACKAGE,
            names.OP_RESTRICTION_T: LADMNames.RRR_PACKAGE,
            names.OP_ADMINISTRATIVE_SOURCE_T: LADMNames.SOURCE_PACKAGE,
            names.OP_SPATIAL_SOURCE_T: LADMNames.SOURCE_PACKAGE,
            names.OP_BOUNDARY_POINT_T: LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE,
            names.OP_SURVEY_POINT_T: LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE,
            names.OP_BOUNDARY_T: LADMNames.SURVEYING_AND_REPRESENTATION_PACKAGE
        }

    @staticmethod
    def get_dict_automatic_values(names):
        return {
            names.OP_BOUNDARY_T: {names.OP_BOUNDARY_T_LENGTH_F: "$length"},
            names.OP_PARTY_T: {
                names.COL_PARTY_T_NAME_F: """
                    CASE
                        WHEN {party_type} = get_domain_code_from_value('{domain_party_type}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False)  THEN
                            concat({surname_1}, ' ', {surname_2}, ' ', {first_name_1}, ' ', {first_name_2})
                        WHEN {party_type} = get_domain_code_from_value('{domain_party_type}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                            {business_name}
                    END
                """.format(party_type=names.OP_PARTY_T_TYPE_F,
                           domain_party_type=names.OP_PARTY_TYPE_D,
                           surname_1=names.OP_PARTY_T_SURNAME_1_F,
                           surname_2=names.OP_PARTY_T_SURNAME_2_F,
                           first_name_1=names.OP_PARTY_T_FIRST_NAME_1_F,
                           first_name_2=names.OP_PARTY_T_FIRST_NAME_2_F,
                           business_name=names.OP_PARTY_T_BUSINESS_NAME_F,
                           OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                           OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V)
            },
            names.OP_PARCEL_T: {
                names.OP_PARCEL_T_DEPARTMENT_F: 'substr("{}", 0, 2)'.format(names.OP_PARCEL_T_PARCEL_NUMBER_F),
                names.OP_PARCEL_T_MUNICIPALITY_F: 'substr("{}", 3, 3)'.format(names.OP_PARCEL_T_PARCEL_NUMBER_F)
            }
        }

    @staticmethod
    def get_dict_display_expressions(names):
        return {
            names.OP_PARTY_T: "concat({}, ' - ',  {})".format(names.OP_PARTY_T_DOCUMENT_ID_F, names.COL_PARTY_T_NAME_F),
            names.OP_PARCEL_T: "concat({}, ' - ', {}, ' - ', {})".format(names.T_ID_F, names.OP_PARCEL_T_PARCEL_NUMBER_F, names.OP_PARCEL_T_FMI_F),
            names.OP_GROUP_PARTY_T: "concat({}, ' - ', {})".format(names.T_ID_F, names.COL_PARTY_T_NAME_F),
            names.OP_BUILDING_T: '"{}"  || \' \' ||  "{}"'.format(names.OID_T_NAMESPACE_F, names.T_ID_F),
            names.GC_PARCEL_T: "concat('(', {}, ') ', {})".format(names.T_ID_F, names.GC_PARCEL_T_PARCEL_NUMBER_F),
            names.SNR_PARCEL_REGISTRY_T:  "concat('(', {}, ') ', {})".format(names.T_ID_F, names.SNR_PARCEL_REGISTRY_T_NEW_PARCEL_NUMBER_IN_FMI_F)
        }

    @staticmethod
    def get_layer_variables(names):
        return {
            names.OP_BUILDING_T: {
                "qgis_25d_angle": 90,
                "qgis_25d_height": 1
            },
            names.OP_BUILDING_UNIT_T: {
                "qgis_25d_angle": 90,
                "qgis_25d_height": '"{}" * 2.5'.format(names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F)
            }
        }

    @staticmethod
    def get_layer_sets(names):
        """
        Configure layer sets to appear in the load layers dialog
        Each layer set is a key-value pair where key is the name of the layer set
        and the value is a list of layers to load
        """
        return {
            'Datos de Interesados': [
                names.OP_PARTY_T,
                names.OP_GENRE_D,
                names.OP_PARTY_DOCUMENT_TYPE_D,
                names.OP_PARTY_TYPE_D
            ],
            'Derechos': [
                names.OP_PARTY_T,
                names.OP_PARCEL_T,
                names.OP_ADMINISTRATIVE_SOURCE_T,
                names.EXT_ARCHIVE_S,
                names.OP_GROUP_PARTY_T,
                names.OP_RIGHT_T
            ],
            'Punto Lindero, Lindero y Terreno': [
                names.OP_BOUNDARY_POINT_T,
                names.OP_BOUNDARY_T,
                names.OP_PLOT_T,
                names.MORE_BFS_T,
                names.LESS_BFS_T,
                names.POINT_BFS_T
            ]
        }

    @staticmethod
    def get_dict_plural(names):
        """
        PLURAL WORDS, FOR DISPLAY PURPOSES
        """
        return {
            names.OP_PLOT_T: "Terrenos",
            names.OP_PARCEL_T: "Predios",
            names.OP_BUILDING_T: "Construcciones",
            names.OP_BUILDING_UNIT_T: "Unidades de Construcción",
            names.EXT_ADDRESS_S: "Direcciones",
            names.OP_PARTY_T: "Interesados",
            names.OP_GROUP_PARTY_T: "Agrupación de interesados",
            names.OP_RIGHT_T: "Derechos",
            names.OP_RESTRICTION_T: "Restricciones",
            names.OP_ADMINISTRATIVE_SOURCE_T: "Fuentes Administrativas",
            names.OP_SPATIAL_SOURCE_T: "Fuentes Espaciales",
            names.OP_BOUNDARY_T: "Linderos",
            names.OP_BOUNDARY_POINT_T: "Puntos de Lindero",
            names.OP_SURVEY_POINT_T: "Puntos de Levantamiento"
        }

    @staticmethod
    def get_logic_consistency_tables(names):
        """
        we define the minimum structure of a table to validate that there are no repeated records
        """
        return {
            # Geometric tables
            names.OP_BOUNDARY_POINT_T: [names.OP_BOUNDARY_POINT_T_AGREEMENT_F,
                                        names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F,
                                        names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F,
                                        names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F,
                                        names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F,
                                        names.COL_POINT_T_INTERPOLATION_POSITION_F,
                                        names.COL_POINT_T_MONUMENTATION_F,
                                        names.COL_POINT_T_PRODUCTION_METHOD_F,
                                        names.OP_BOUNDARY_POINT_T_POINT_TYPE_F,
                                        names.COL_POINT_T_ORIGINAL_LOCATION_F],
            names.OP_SURVEY_POINT_T: [names.OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F,
                                      names.OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F,
                                      names.OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F,
                                      names.OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F,
                                      names.COL_POINT_T_INTERPOLATION_POSITION_F,
                                      names.COL_POINT_T_PRODUCTION_METHOD_F,
                                      names.COL_POINT_T_MONUMENTATION_F,
                                      names.OP_SURVEY_POINT_T_POINT_TYPE_F,
                                      names.COL_POINT_T_ORIGINAL_LOCATION_F],
            names.OP_CONTROL_POINT_T: [names.OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F,
                                       names.OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F,
                                       names.OP_CONTROL_POINT_T_ID_F,
                                       names.COL_POINT_T_INTERPOLATION_POSITION_F,
                                       names.COL_POINT_T_MONUMENTATION_F,
                                       names.OP_CONTROL_POINT_T_POINT_TYPE_F,
                                       names.COL_POINT_T_ORIGINAL_LOCATION_F],
            names.OP_BOUNDARY_T: [names.OP_BOUNDARY_T_LENGTH_F,
                                  names.COL_BFS_T_TEXTUAL_LOCATION_F,
                                  names.COL_BFS_T_GEOMETRY_F],
            names.OP_PLOT_T: [names.OP_PLOT_T_PLOT_AREA_F,
                              names.OP_PLOT_T_PLOT_VALUATION_F,
                              names.COL_SPATIAL_UNIT_T_DIMENSION_F,
                              names.COL_SPATIAL_UNIT_T_LABEL_F,
                              names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                              names.OP_PLOT_T_GEOMETRY_F],
            names.OP_BUILDING_T: [names.OP_BUILDING_T_BUILDING_VALUATION_F,
                                  names.OP_BUILDING_T_BUILDING_AREA_F,
                                  names.COL_SPATIAL_UNIT_T_DIMENSION_F,
                                  names.COL_SPATIAL_UNIT_T_LABEL_F,
                                  names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                                  names.COL_SPATIAL_UNIT_T_GEOMETRY_F],
            names.OP_BUILDING_UNIT_T: [names.OP_BUILDING_UNIT_T_BUILDING_VALUATION_F,
                                       names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F,
                                       names.OP_BUILDING_UNIT_T_BUILT_AREA_F,
                                       names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F,
                                       names.OP_BUILDING_UNIT_T_BUILDING_F,
                                       names.COL_SPATIAL_UNIT_T_DIMENSION_F,
                                       names.COL_SPATIAL_UNIT_T_LABEL_F,
                                       names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                                       names.COL_SPATIAL_UNIT_T_GEOMETRY_F],
            # Alphanumeric tables
            names.OP_PARTY_T: [names.OP_PARTY_T_DOCUMENT_ID_F,
                               names.OP_PARTY_T_DOCUMENT_TYPE_F],
            names.OP_PARCEL_T: [names.OP_PARCEL_T_DEPARTMENT_F,
                                names.OP_PARCEL_T_MUNICIPALITY_F,
                                names.OP_PARCEL_T_NUPRE_F,
                                names.OP_PARCEL_T_FMI_F,
                                names.OP_PARCEL_T_PARCEL_NUMBER_F,
                                names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F,
                                names.OP_PARCEL_T_VALUATION_F,
                                names.COL_BAUNIT_T_NAME_F,
                                names.OP_PARCEL_T_PARCEL_TYPE_F],
            names.OP_RIGHT_T: [names.OP_RIGHT_T_TYPE_F,
                               names.COL_RRR_T_DESCRIPTION_F,
                               names.COL_RRR_T_SHARE_CHECK_F,
                               names.COL_RRR_T_EFFECTIVE_USAGE_F,
                               names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                               names.COL_RRR_PARTY_T_OP_PARTY_F,
                               names.COL_BAUNIT_RRR_T_UNIT_F],
            names.OP_RESTRICTION_T: [names.OP_RESTRICTION_T_TYPE_F,
                                     names.COL_RRR_T_DESCRIPTION_F,
                                     names.COL_RRR_T_SHARE_CHECK_F,
                                     names.COL_RRR_T_EFFECTIVE_USAGE_F,
                                     names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                                     names.COL_RRR_PARTY_T_OP_PARTY_F,
                                     names.COL_BAUNIT_RRR_T_UNIT_F],
            names.OP_ADMINISTRATIVE_SOURCE_T: [names.OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F,
                                               names.COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F,
                                               names.COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F,
                                               names.OP_ADMINISTRATIVE_SOURCE_T_TYPE_F,
                                               names.COL_SOURCE_T_DATE_DOCUMENT_F,
                                               names.COL_SOURCE_T_AVAILABILITY_STATUS_F,
                                               names.COL_SOURCE_T_MAIN_TYPE_F,
                                               names.COL_SOURCE_T_OFFICIAL_F]
        }

    @staticmethod
    def get_custom_widget_configuration(names):
        return {
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
        }

    @staticmethod
    def get_custom_read_only_fields(names):
        # Read only fields might be declared in two scenarios:
        #   1. As soon as the layer is loaded (e.g., OP_PARCEL_T_DEPARTMENT_F)
        #   2. Only for a wizard (e.g., PARCEL_TYPE)
        # WARNING: Both modes are exclusive, if you list a field in 1, DO NOT do it in 2. and viceversa!
        return {
            names.OP_PARCEL_T: [names.OP_PARCEL_T_DEPARTMENT_F,
                                names.OP_PARCEL_T_MUNICIPALITY_F]  # list of fields of the layer to block its edition
        }
