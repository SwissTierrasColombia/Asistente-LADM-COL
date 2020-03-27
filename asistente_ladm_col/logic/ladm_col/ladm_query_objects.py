from abc import ABC
"""
Definition of objects that are used by QGISLADMQuery to execute the queries.
"""

class AbsFieldLADMQuery(ABC):
    def __init__(self, field_alias):
        super(AbsFieldLADMQuery, self).__init__()
        self.field_alias = field_alias


class OwnField(AbsFieldLADMQuery):
    """
    Field of a table that can be obtained directly
    :param field_name: Name of the field in the table (str)
    :param field_alias: Alias of the field (str)
    Used for: get field vale of level table

    """
    def __init__(self, field_name, field_alias):
        super(OwnField, self).__init__(field_alias)
        self.field_name = field_name


class DomainOwnField(OwnField):
    """
    Campo de una tabla que se puede obtener directamente pero tiene el valor del dominio
    :param field_name: Name of the field in the table (str)
    :param field_alias: Alias of the field (str)
    :param domain_table: Domain table associated with the field (str)
    Used for: get the value of a field associated with your domain table of level table
    """

    def __init__(self, field_name, field_alias, domain_table):
        super(DomainOwnField, self).__init__(field_name, field_alias)
        self.domain_table = domain_table


class EvalExprOwnField(AbsFieldLADMQuery):
    """
    Field of a table that can be obtained directly but it is necessary
    to evaluate an expression to perform a transformation of the data
    :param field_alias: Alias of the field (str)
    :param expression: Expression to execute (QgsExpression)
    Used for: evaluate a expression in level table
    """
    def __init__(self, field_alias, expression):
        super(EvalExprOwnField, self).__init__(field_alias)
        self.expression = expression


class AbsRelatedFields(AbsFieldLADMQuery):
    def __init__(self, field_alias, relate_table, relate_table_filter_field):
        super(AbsRelatedFields, self).__init__(field_alias)
        self.relate_table = relate_table
        self.relate_table_filter_field = relate_table_filter_field


class RelatedOwnFieldObject(AbsRelatedFields):
    """
    Fields of a related table that can be obtained through a field of the consulted table
    :param field_alias: Alias of the field (str)
    :param relate_table: Relate table name (str)
    :param relate_table_fields: Relate table fields (list<(OwnField, DomainOwnField, EvalExprOwnField)>)
    :param relate_table_filter_field: Relate table filter field (str)
    """
    def __init__(self, field_alias, relate_table, relate_table_fields, relate_table_filter_field):
        super(RelatedOwnFieldObject, self).__init__(field_alias, relate_table, relate_table_filter_field)
        self.relate_table_fields = relate_table_fields


class RelatedOwnFieldValue(AbsRelatedFields):
    """
    Fields of a related table that can be obtained through a field of the consulted table
    :param field_alias: Alias of the field (str)
    :param relate_table: Relate table name (str)
    :param relate_table_field: Relate table field (OwnField, DomainOwnField, EvalExprOwnField)
    :param relate_table_filter_field: Relate table filter field (str)
    """
    def __init__(self, field_alias, relate_table, relate_table_field, relate_table_filter_field):
        super(RelatedOwnFieldValue, self).__init__(field_alias, relate_table, relate_table_filter_field)
        self.relate_table_field = relate_table_field


class RelatedRemoteFieldObject(RelatedOwnFieldObject):
    """
    Fields from an unrelated table that can be obtained through a field
    from the queried table using a custom filter
    :param field_alias: Alias of the field (str)
    :param relate_table: Relate table name (str)
    :param relate_table_fields:  Relate table fields (list<(OwnField, DomainOwnField, EvalExprOwnField)>)
    :param relate_table_filter_field: Relate table field to apply filter
    :param filter_sub_level: Custom filter to apply
    """
    def __init__(self, field_alias, relate_table, relate_table_fields, relate_table_filter_field, filter_sub_level):
        super(RelatedRemoteFieldObject, self).__init__(field_alias, relate_table, relate_table_fields, relate_table_filter_field)
        self.filter_sub_level = filter_sub_level


class RelatedRemoteFieldValue(RelatedOwnFieldValue):
    """
    Fields from an unrelated table that can be obtained through a field
    from the queried table using a custom filter
    :param field_alias: Alias of the field (str)
    :param relate_table: Relate table name (str)
    :param relate_table_field:  Relate table fields (OwnField, DomainOwnField, EvalExprOwnField)
    :param relate_table_filter_field: Relate table field to apply filter
    :param filter_sub_level: Custom filter to apply
    """
    def __init__(self, field_alias, relate_table, relate_table_field, relate_table_filter_field, filter_sub_level):
        super(RelatedRemoteFieldValue, self).__init__(field_alias, relate_table, relate_table_field, relate_table_filter_field)
        self.filter_sub_level = filter_sub_level


class AbsFilterSubLevel(ABC):
    def __init__(self, required_field_sub_level_table, sub_level_table):
        super(AbsFilterSubLevel, self).__init__()
        self.required_field_sub_level_table = required_field_sub_level_table
        self.sub_level_table = sub_level_table


class FilterSubLevel(AbsFilterSubLevel):
    """
    Alphanumeric filter.
    This filter is used to obtains the values of a field according to another filtered field.
    For example:
        FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                       names.COL_UE_BAUNIT_T,
                       names.COL_UE_BAUNIT_T_OP_PLOT_F)

        Filter table COL_UE_BAUNIT_T by COL_UE_BAUNIT_T_OP_PLOT_F and return COL_UE_BAUNIT_T_PARCEL_F

    :param required_field_sub_level_table: Required field sub level table
    :param sub_level_table: Table name to be filtered (str)
    :param filter_field_in_sub_level_table: Filter field in sub level table
    :param filter_sub_level: : Custom filter to apply
    """
    def __init__(self, required_field_sub_level_table, sub_level_table, filter_field_in_sub_level_table, filter_sub_level=None):
        super(FilterSubLevel, self).__init__(required_field_sub_level_table, sub_level_table)
        self.filter_field_in_sub_level_table = filter_field_in_sub_level_table
        self.filter_sub_level = filter_sub_level


class SpatialFilterSubLevel(AbsFilterSubLevel):
    """
    Spatial filter
    This filter is used to obtains the values of a field according to another filtered field using a spatial operation.
    For example:
        SpatialFilterSubLevel(names.T_ID_F,
                              names.OP_SURVEY_POINT_T,
                              names.OP_PLOT_T,
                              EnumSpatialOperationType.INTERSECTS)
        Get T_ID_F field of OP_SURVEY_POINT_T that INTERSECTS with OP_PLOT_T

    :param required_field_sub_level_table: Required field sub level table
    :param sub_level_table: Table name to be filtered (str)
    :param level_table: name of the queried table at the nesting level above the query definition (str)
    :param spatial_operation: Enum value of EnumSpatialOperationType
    :param filter_sub_level: Custom filter to apply
    """
    def __init__(self, required_field_sub_level_table, sub_level_table, level_table, spatial_operation, filter_sub_level=None):
        super(SpatialFilterSubLevel, self).__init__(required_field_sub_level_table, sub_level_table)
        self.level_table = level_table
        self.spatial_operation = spatial_operation
        self.filter_sub_level = filter_sub_level

