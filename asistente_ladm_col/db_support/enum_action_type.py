from enum import Enum


class EnumActionType(Enum):
    SCHEMA_IMPORT = 1
    IMPORT = 2
    EXPORT = 3
    OTHER = 100
