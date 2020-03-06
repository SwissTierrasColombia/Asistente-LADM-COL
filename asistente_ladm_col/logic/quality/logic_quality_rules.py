from qgis.PyQt.QtCore import (QCoreApplication,
                              QVariant)
from qgis.core import (Qgis,
                       QgsField,
                       QgsGeometry,
                       QgsVectorLayer,
                       QgsVectorLayerUtils)

from asistente_ladm_col.config.enums import QualityRuleEnum
from asistente_ladm_col.config.mapping_config import LADMNames
from asistente_ladm_col.config.translation_strings import (ERROR_PARCEL_WITH_NO_RIGHT,
                                                           ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT)
from asistente_ladm_col.logic.quality.utils_quality_rules import UtilsQualityRules
from asistente_ladm_col.lib.logger import Logger


class LogicQualityRules:
    def __init__(self, qgis_utils, translated_strings):
        self.translated_strings = translated_strings
        self.qgis_utils = qgis_utils
        self.logger = Logger()

    def check_parcel_right_relationship(self, db, query_manager):
        error_layer = None
        error_layer_exist = False
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Parcel table")
        group = self.qgis_utils.get_error_layers_group()
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break


        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField("id_predio", QVariant.Int),
                              QgsField(QCoreApplication.translate("LogicQualityRules", "error_type"), QVariant.String)])
            error_layer.updateFields()

        new_features = list()

        res, records = query_manager.get_parcels_with_not_right(db)
        if res:
            for record in records:
                new_feature = QgsVectorLayerUtils().createFeature(
                    error_layer,
                    QgsGeometry(),
                    {0: record[db.names.T_ID_F],
                     1: self.translated_strings[ERROR_PARCEL_WITH_NO_RIGHT]})
                new_features.append(new_feature)

        res, records = query_manager.get_parcels_with_repeated_domain_right(db)
        if res:
            for record in records:
                new_feature = QgsVectorLayerUtils().createFeature(
                    error_layer,
                    QgsGeometry(),
                    {0: record[db.names.T_ID_F],
                     1: self.translated_strings[ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT]})
                new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        if len(new_features) > 0:
            if error_layer_exist is False:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)
            else:
                added_layer = error_layer

            return (QCoreApplication.translate("LogicQualityRules", "A memory layer with {} parcel errors has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

        else:
            return (QCoreApplication.translate("LogicQualityRules", "Parcel-Right relationships are correct!"), Qgis.Success)

    def check_duplicate_records_in_a_table(self, db, query_manager, table, fields):
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Duplicate records in '{table}'").format(table=table)
        error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
        pr = error_layer.dataProvider()
        pr.addAttributes([QgsField(QCoreApplication.translate("LogicQualityRules", "duplicate_ids"), QVariant.String),
                          QgsField(QCoreApplication.translate("LogicQualityRules", "count"), QVariant.Int)])
        error_layer.updateFields()
        res, records = query_manager.get_duplicate_records_in_table(db, table, fields)

        if res:
            new_features = list()
            for record in records:
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                                  {0: record['duplicate_ids'],
                                                                   1: record['duplicate_total']})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)
        else:
            self.logger.error_msg(__name__, "Error executing query for rule check duplicate records in a table: {}".format(records))

        if error_layer.featureCount() > 0:
            added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules",
                                                        "A memory layer with {error_count} duplicate records from {table} has been added to the map!").format(error_count=added_layer.featureCount(), table=table), Qgis.Critical)

        else:
            return (QCoreApplication.translate("LogicQualityRules", "There are no repeated records in {table}!").format(table=table), Qgis.Success)

    def check_group_party_fractions_that_do_not_add_one(self, db, query_manager):
        rule_name = self.translated_strings[QualityRuleEnum.Logic.FRACTION_SUM_FOR_PARTY_GROUPS]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Fractions do not add up to 1")

        error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
        pr = error_layer.dataProvider()
        pr.addAttributes([QgsField(QCoreApplication.translate("LogicQualityRules", "party_group"), QVariant.Int),
                          QgsField(QCoreApplication.translate("LogicQualityRules", "members"), QVariant.String),
                          QgsField(QCoreApplication.translate("LogicQualityRules", "fraction_sum"), QVariant.Double)])
        error_layer.updateFields()

        res, records = query_manager.get_group_party_fractions_that_do_not_add_one(db)

        if res:
            new_features = list()
            for record in records:
                new_feature = QgsVectorLayerUtils().createFeature(
                    error_layer,
                    QgsGeometry(),
                    {0: record['agrupacion'],  # Fields alias was defined in the sql query
                     1: ",".join([str(f) for f in record['miembros']]),
                     2: record['suma_fracciones']})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)
        else:
            self.logger.error_msg(__name__, "Error executing query for rule {}: {}".format(rule_name, records))

        if error_layer.featureCount() > 0:
            added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules",
                                                        "A memory layer with {} fractions which do not sum 1 has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)
        else:
            return (QCoreApplication.translate("LogicQualityRules", "Group Party Fractions are correct!"), Qgis.Success)

    def check_parcels_with_invalid_department_code(self, db, query_manager):
        rule_name = self.translated_strings[QualityRuleEnum.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Parcel table")
        table = QCoreApplication.translate("LogicQualityRules", "Parcel")

        res, records = query_manager.get_parcels_with_invalid_department_code(db)
        if res:
            return self.basic_logic_validations(db, records, error_table_name, table, rule_name)

    def check_parcels_with_invalid_municipality_code(self, db, query_manager):
        rule_name = self.translated_strings[QualityRuleEnum.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Parcel table")
        table = QCoreApplication.translate("LogicQualityRules", "Parcel")

        res, records = query_manager.get_parcels_with_invalid_municipality_code(db)
        if res:
            return self.basic_logic_validations(db, records, error_table_name, table, rule_name)

    def check_parcels_with_invalid_parcel_number(self, db, query_manager):
        rule_name = self.translated_strings[QualityRuleEnum.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Parcel table")
        table = QCoreApplication.translate("LogicQualityRules", "Parcel")

        res, records = query_manager.get_parcels_with_invalid_parcel_number(db)
        if res:
            return self.basic_logic_validations(db, records, error_table_name, table, rule_name)

    def check_parcels_with_invalid_previous_parcel_number(self, db, query_manager):
        rule_name = self.translated_strings[QualityRuleEnum.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Parcel table")
        table = QCoreApplication.translate("LogicQualityRules", "Parcel")

        res, records = query_manager.get_parcels_with_invalid_previous_parcel_number(db)
        if res:
            return self.basic_logic_validations(db, records, error_table_name, table, rule_name)

    def check_invalid_col_party_type_natural(self, db, query_manager):
        error_layer = None
        error_layer_exist = False
        rule_name = self.translated_strings[QualityRuleEnum.Logic.COL_PARTY_NATURAL_TYPE]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Party table")
        table = QCoreApplication.translate("LogicQualityRules", "Party")

        group = self.qgis_utils.get_error_layers_group()  # Check if error layer exist
        layers = group.findLayers()  # Check if layer is loaded
        for layer in layers:
            if layer.name() == error_table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes(
                [QgsField(QCoreApplication.translate("LogicQualityRules", "{table}_id").format(table=table), QVariant.Int),
                 QgsField(QCoreApplication.translate("LogicQualityRules", "error_type"), QVariant.String)])
            error_layer.updateFields()

        res, records = query_manager.get_invalid_col_party_type_natural(db)

        if res:
            new_features = list()
            for record in records:
                errors_list = list()
                if record[db.names.OP_PARTY_T_BUSINESS_NAME_F] > 0:
                    errors_list.append(
                        QCoreApplication.translate("LogicQualityRules", "{business_name} must be NULL").format(
                            business_name=db.names.OP_PARTY_T_BUSINESS_NAME_F))
                if record[db.names.OP_PARTY_T_SURNAME_1_F] > 0:
                    errors_list.append(QCoreApplication.translate("LogicQualityRules",
                                                                  "{surname_party} must not be NULL and It must be filled in").format(
                        surname_party=db.names.OP_PARTY_T_SURNAME_1_F))
                if record[db.names.OP_PARTY_T_FIRST_NAME_1_F] > 0:
                    errors_list.append(QCoreApplication.translate("LogicQualityRules",
                                                                  "{first_name_party} must not be NULL and It must be filled in").format(
                        first_name_party=db.names.OP_PARTY_T_FIRST_NAME_1_F))
                if record[db.names.OP_PARTY_T_DOCUMENT_TYPE_F] > 0:
                    errors_list.append(QCoreApplication.translate("LogicQualityRules",
                                                                  "{doc_type} must be different from NIT").format(
                        doc_type=db.names.OP_PARTY_T_DOCUMENT_TYPE_F))

                mgs_error = ', '.join(errors_list)
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                                  {0: record[db.names.T_ID_F], 1: mgs_error})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)
        else:
            self.logger.error_msg(__name__, "Error executing query for rule {}: {}".format(rule_name, records))

        if len(new_features) > 0:
            if error_layer_exist is False:
                UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules", "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(error_count=len(new_features), table=table), Qgis.Critical)
        else:
            return (QCoreApplication.translate("LogicQualityRules", "No errors found when checking '{rule_name}' for '{table}'!").format(rule_name=rule_name, table=table), Qgis.Success)

    def check_invalid_col_party_type_no_natural(self, db, query_manager):
        error_layer = None
        error_layer_exist = False
        rule_name = self.translated_strings[QualityRuleEnum.Logic.COL_PARTY_NOT_NATURAL_TYPE]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Party table")
        table = QCoreApplication.translate("LogicQualityRules", "Party")

        group = self.qgis_utils.get_error_layers_group()  # Check if error layer exist
        layers = group.findLayers()  # Check if layer is loaded
        for layer in layers:
            if layer.name() == error_table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes(
                [QgsField(QCoreApplication.translate("LogicQualityRules", "{table}_id").format(table=table), QVariant.Int),
                 QgsField(QCoreApplication.translate("LogicQualityRules", "error_type"), QVariant.String)])
            error_layer.updateFields()

        res, records = query_manager.get_invalid_col_party_type_no_natural(db)

        new_features = list()
        if res:
            for record in records:
                errors_list = list()
                if record[db.names.OP_PARTY_T_BUSINESS_NAME_F] > 0:
                    errors_list.append(QCoreApplication.translate("LogicQualityRules",
                                                                  "{business_name} must not be NULL and It must be filled in").format(
                        business_name=db.names.OP_PARTY_T_BUSINESS_NAME_F))
                if record[db.names.OP_PARTY_T_SURNAME_1_F] > 0:
                    errors_list.append(
                        QCoreApplication.translate("LogicQualityRules", "{surname_party} must be NULL").format(
                            surname_party=db.names.OP_PARTY_T_SURNAME_1_F))
                if record[db.names.OP_PARTY_T_FIRST_NAME_1_F] > 0:
                    errors_list.append(QCoreApplication.translate("LogicQualityRules",
                                                                  "{first_name_party} must be NULL").format(
                        first_name_party=db.names.OP_PARTY_T_FIRST_NAME_1_F))
                if record[db.names.OP_PARTY_T_DOCUMENT_TYPE_F] > 0:
                    errors_list.append(QCoreApplication.translate("LogicQualityRules",
                                                                  "{doc_type} must be equal to NIT or Secuencial_IGAC or Secuencial_SNR").format(
                        doc_type=db.names.OP_PARTY_T_DOCUMENT_TYPE_F))

                mgs_error = ', '.join(errors_list)
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                                  {0: record[db.names.T_ID_F], 1: mgs_error})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)
        else:
            self.logger.error_msg(__name__, "Error executing query for rule {}: {}".format(rule_name, records))

        if len(new_features) > 0:
            if error_layer_exist is False:
                UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules",
                                                        "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(error_count=len(new_features), table=table), Qgis.Critical)
        else:
            return (QCoreApplication.translate("LogicQualityRules",
                                                        "No errors found when checking '{rule_name}' for '{table}'!").format(rule_name=rule_name, table=table), Qgis.Success)

    def check_parcels_with_invalid_parcel_type_and_22_position_number(self, db, query_manager):
        error_layer = None
        error_layer_exist = False
        rule_name = self.translated_strings[QualityRuleEnum.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Logic Consistency Errors in Parcel table")
        table = QCoreApplication.translate("LogicQualityRules", "Parcel")

        group = self.qgis_utils.get_error_layers_group()
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("LogicQualityRules", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("LogicQualityRules", "error_type"), QVariant.String)])
            error_layer.updateFields()

        res, records = query_manager.get_parcels_with_invalid_parcel_type_and_22_position_number(db)

        new_features = list()
        if res:
            for record in records:
                mgs_error =  None
                if record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY:
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 0").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] in (LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT, LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT):
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 9").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT + " or " + LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] in (LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT, LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT):
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 8").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT + " or " + LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] in (LADMNames.PARCEL_TYPE_CEMETERY_PARENT, LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT):
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 7").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_CEMETERY_PARENT + " or " + LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA:
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 5").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA:
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 5").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_ROAD:
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 4").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_ROAD)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_PUBLIC_USE:
                    mgs_error = QCoreApplication.translate("LogicQualityRules", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 3").format(table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=LADMNames.PARCEL_TYPE_PUBLIC_USE)

                new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(), {0: record[db.names.T_ID_F], 1: mgs_error})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)
        else:
            self.logger.error_msg(__name__, "Error executing query for rule {}: {}".format(rule_name, records))

        if len(new_features) > 0:
            if error_layer_exist is False:
                UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules",
                                                        "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(error_count=len(new_features), table=table), Qgis.Critical)
        else:
            return (QCoreApplication.translate("LogicQualityRules",
                                                        "No errors found when checking '{rule_name}' for '{table}'!").format(rule_name=rule_name, table=table), Qgis.Success)

    def check_uebaunit_parcel(self, db, query_manager):
        error_layer = None
        error_layer_exist = False
        rule_name = self.translated_strings[QualityRuleEnum.Logic.UEBAUNIT_PARCEL]
        error_table_name = QCoreApplication.translate("LogicQualityRules", "Errors in relationships between Spatial Units and Parcels")
        table = "Parcel"

        group = self.qgis_utils.get_error_layers_group()
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes(
                [QgsField(QCoreApplication.translate("LogicQualityRules", "{parcel_id"), QVariant.Int),
                 QgsField(QCoreApplication.translate("LogicQualityRules", "associated_parcels"), QVariant.Int),
                 QgsField(QCoreApplication.translate("LogicQualityRules", "associated_buildings"), QVariant.Int),
                 QgsField(QCoreApplication.translate("LogicQualityRules", "associated_building_units"), QVariant.Int),
                 QgsField(QCoreApplication.translate("LogicQualityRules", "error_type"), QVariant.String)])
            error_layer.updateFields()

        res, records = query_manager.get_uebaunit_parcel(db)

        new_features = list()
        if res:
            for record in records:
                mgs_error = None

                plot_count = record['sum_t']  # count of plots associated to the parcel
                building_count = record['sum_c']  # count of buildings associated to the parcel
                building_unit_count = record['sum_uc']  # count of building units associated to the parcel

                if record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_unit_count=building_unit_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_unit_count=building_unit_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_unit_count=building_unit_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_CEMETERY_PARENT:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_unit_count=building_unit_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_CEMETERY_PARENT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_PUBLIC_USE:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_unit_count=building_unit_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_PUBLIC_USE)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_unit_count=building_unit_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_ROAD:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count,
                        table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_ROAD)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count,
                        table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT)
                elif record[
                    db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 0 plot and 0 building but you have {plot_count} plot(s) and {building_count} building(s)").format(
                        plot_count=plot_count, building_count=building_count, table=db.names.OP_PARCEL_T,
                        parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 0 plot and 1 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count,
                        table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA)
                elif record[db.names.OP_PARCEL_T_PARCEL_TYPE_F] == LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA:
                    mgs_error = QCoreApplication.translate("LogicQualityRules",
                                                           "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 0 plot and 1 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(
                        plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count,
                        table=db.names.OP_PARCEL_T, parcel_type_field=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                        parcel_type=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA)

                new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                                  {0: record[db.names.T_ID_F],
                                                                   1: plot_count,
                                                                   2: building_count,
                                                                   3: building_unit_count,
                                                                   4: mgs_error})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)
        else:
            self.logger.error_msg(__name__, "Error executing query for rule {}: {}".format(rule_name, records))

        if len(new_features) > 0:
            if error_layer_exist is False:
                UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules",
                                                        "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(error_count=len(new_features), table=table), Qgis.Critical)
        else:
            return (QCoreApplication.translate("LogicQualityRules",
                                                        "No errors found when checking '{rule}' for '{table}'!").format(rule=rule_name, table=table), Qgis.Success)

    # UTILS METHODS

    def basic_logic_validations(self, db, records, error_table_name, table, rule_name):
        """
        Create a error table with error found
        :param db: db connection
        :param records: Result of execute the query
        :param error_table_name: Error table name
        :param table: Table name where error was found
        :param rule_name: Rule error description (Name of rule to show in log quality rules).

        Note: rule_name is used by _log_quality_checks decorator
        """
        error_layer = None
        error_layer_exist = False

        # Check if error layer exist
        group = self.qgis_utils.get_error_layers_group()

        # Check if layer is loaded
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if error_layer_exist is False:
            error_layer = QgsVectorLayer("NoGeometry", error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("LogicQualityRules", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("LogicQualityRules", "error_type"), QVariant.String)])
            error_layer.updateFields()

        new_features = []
        for record in records:
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                              {0: record[db.names.T_ID_F], 1: rule_name})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        if len(new_features) > 0:
            if error_layer_exist is False:
                UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            return (QCoreApplication.translate("LogicQualityRules",
                                                        "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(error_count=len(new_features), table=table), Qgis.Critical)

        else:
            return (QCoreApplication.translate("LogicQualityRules",
                                                        "No errors found when checking '{rule_name}' for '{table}'!").format(rule_name=rule_name, table=table), Qgis.Success)
