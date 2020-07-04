from abc import ABC
"""
Definition of objects that are used by QGISLADMQuery to configure and execute the queries.
"""

class AbsFieldLADMQuery(ABC):
    def __init__(self, field_alias):
        super(AbsFieldLADMQuery, self).__init__()
        self.field_alias = field_alias


class OwnField(AbsFieldLADMQuery):
    """
    Table field that is directly accessible.

    :param field_name: Name of the field in the table (str)
    :param field_alias: Desired alias for the field (str)
    Used to: get field vale of level table
    """
    def __init__(self, field_name, field_alias):
        super(OwnField, self).__init__(field_alias)
        self.field_name = field_name


class DomainOwnField(OwnField):
    """
    Table field related to a domain.

    :param field_name: Name of the field in the referencing table (str)
    :param field_alias: Alias of the field in the referencing table (str)
    :param domain_table: Domain table associated with the field (str)
    Used to: get the value of a field associated with a domain table
    """
    def __init__(self, field_name, field_alias, domain_table):
        super(DomainOwnField, self).__init__(field_name, field_alias)
        self.domain_table = domain_table


class EvalExpressionOwnField(AbsFieldLADMQuery):
    """
    Table field, whose value can be obtained directly after evaluating an expression.

    :param field_alias: Alias of the field (str)
    :param expression: Expression to be evaluated (QgsExpression)
    Used to: evaluate a expression in the base table
    """
    def __init__(self, field_alias, expression):
        super(EvalExpressionOwnField, self).__init__(field_alias)
        self.expression = expression


class AbsRelatedFields(AbsFieldLADMQuery):
    def __init__(self, field_alias, referenced_layer, referenced_field):
        super(AbsRelatedFields, self).__init__(field_alias)
        self.referenced_layer = referenced_layer
        self.referenced_field = referenced_field


class RelatedOwnFieldObject(AbsRelatedFields):
    """
    Fields of a referenced layer that can be obtained from a referencing layer.
    This gets several rows and several columns, i.e., a list of dicts

    :param field_alias: Alias of the field (str)
    :param referenced_layer: Referenced layer name (str)
    :param required_fields_referenced_table: Fields to obtain from the referenced layer
           Can be a combination of list<(OwnField, DomainOwnField, EvalExprOwnField)>
    :param referenced_field: Referenced field of the relationship (str)
    """
    def __init__(self, field_alias, referenced_layer, required_fields_referenced_layer, referenced_field):
        super(RelatedOwnFieldObject, self).__init__(field_alias, referenced_layer, referenced_field)
        self.required_fields_referenced_layer = required_fields_referenced_layer


class RelatedOwnFieldValue(AbsRelatedFields):
    """
    Fields of a related table that can be obtained through a field of the consulted table
    This gets a single row and single column, i.e., a basic Python data value.

    :param field_alias: Alias of the field (str)
    :param referenced_layer: Referenced layer name (str)
    :param required_field_referenced_layer: Required field from referenced table
           Should be one of these: OwnField, DomainOwnField, EvalExprOwnField
    :param referenced_field: Relate table filter field (str)
    """
    def __init__(self, field_alias, referenced_layer, required_field_referenced_layer, referenced_field):
        super(RelatedOwnFieldValue, self).__init__(field_alias, referenced_layer, referenced_field)
        self.required_field_referenced_layer = required_field_referenced_layer


class RelatedRemoteFieldObject(RelatedOwnFieldObject):
    """
    Fields from a remote layer, i.e., a referenced layer of an intermediate table between "referenced" and referencing
    layer.
        (referencing layer --> intermediate layer --> referenced layer)

    The filter connects the referencing layer with the intermediate layer.

    :param field_alias: Alias of the field (str)
    :param referenced_layer: Referenced layer name (str)
    :param required_fields_referenced_layer: Fields to obtain from the referenced layer
           A combination of (OwnField, DomainOwnField, EvalExprOwnField) field objects.
    :param referenced_field: Relate table field to apply filter
    :param filter_sub_level: Custom filter to apply. It will get field values from the intermediate layer which will
            match the "referenced_field" to get thee "required_fields_referenced_layer".
    """
    def __init__(self, field_alias, referenced_layer, required_fields_referenced_layer, referenced_field, filter_sub_level):
        super(RelatedRemoteFieldObject, self).__init__(field_alias, referenced_layer, required_fields_referenced_layer, referenced_field)
        self.filter_sub_level = filter_sub_level


class RelatedRemoteFieldValue(RelatedOwnFieldValue):
    """
    Field value from a remote layer, i.e., a referenced layer of an intermediate table between "referenced" and
    referencing layer.
        (referencing layer --> intermediate layer --> referenced layer)

    The filter connects the referencing layer with the intermediate layer.

    :param field_alias: Alias of the field (str)
    :param referenced_layer: Referenced layer name (str)
    :param required_field_referenced_layer: Field to obtain from the referenced layer
           A field from (OwnField, DomainOwnField, EvalExprOwnField).
    :param referenced_field: Relate table field to apply filter
    :param filter_sub_level: Custom filter to apply. It will get field values from the intermediate layer which will
            match the "referenced_field" to get thee "required_fields_referenced_layer".
    """
    def __init__(self, field_alias, referenced_layer, required_field_referenced_layer, referenced_field, filter_sub_level):
        super(RelatedRemoteFieldValue, self).__init__(field_alias, referenced_layer, required_field_referenced_layer, referenced_field)
        self.filter_sub_level = filter_sub_level


class AbsFilterSubLevel(ABC):
    def __init__(self, required_field_referenced_layer, referenced_layer):
        super(AbsFilterSubLevel, self).__init__()
        self.required_field_referenced_layer = required_field_referenced_layer
        self.referenced_layer = referenced_layer


class FilterSubLevel(AbsFilterSubLevel):
    """
    This filter is used to obtain the values of a field according to another filtered field.
    This gets several rows from a single column, that is, a list of field values.

    For example:
        FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                       names.COL_UE_BAUNIT_T,
                       names.COL_UE_BAUNIT_T_LC_PLOT_F)

        Filter table COL_UE_BAUNIT_T by COL_UE_BAUNIT_T_LC_PLOT_F and return COL_UE_BAUNIT_T_PARCEL_F

    :param required_field_referenced_layer: Required field from the referenced layer
    :param referenced_layer: Referenced layer (str)
    :param referenced_field: Referencing field of the relationship
    :param filter_sub_level: Additional custom filter to apply if nesting filters is needed.
    """
    def __init__(self, required_field_referenced_layer, referenced_layer, referenced_field, filter_sub_level=None):
        super(FilterSubLevel, self).__init__(required_field_referenced_layer, referenced_layer)
        self.referenced_field = referenced_field
        self.filter_sub_level = filter_sub_level


class SpatialFilterSubLevel(AbsFilterSubLevel):
    """
    This filter is used to obtain the values of a referenced field (e.g., t_id) according to a spatial operation over
    a subset of geometries from a base layer.
    This gets several rows from a single column, namely, a list of field values.

    For example:
        SpatialFilterSubLevel(names.T_ID_F,
                              names.LC_SURVEY_POINT_T,
                              names.LC_PLOT_T,
                              EnumSpatialOperationType.INTERSECTS)
        Get T_ID_F field of LC_SURVEY_POINT_T that INTERSECTS with a filtered LC_PLOT_T layer (several plots)

    :param referenced_field: Required field in the sub level table
    :param referenced layer: Table name to be filtered (str)
    :param referencing_layer: level table, i.e., name of the queried table at the nesting level above the query
                              definition (str)
    :param spatial_operation: Enum value of EnumSpatialOperationType
    :param filter_sub_level: Additional custom filter to apply if nesting filters is needed.
    """
    def __init__(self, required_field_referenced_layer, referenced_layer, referencing_layer, spatial_operation, filter_sub_level=None):
        super(SpatialFilterSubLevel, self).__init__(required_field_referenced_layer, referenced_layer)
        self.referencing_layer = referencing_layer
        self.spatial_operation = spatial_operation
        self.filter_sub_level = filter_sub_level

