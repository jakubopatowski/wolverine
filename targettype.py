from enum import Enum


# target type
class TargetType(Enum):
    EXECUTABLE = 1
    LIBRARY = 2
    HEADER_LIBRARY = 3
    UNKNOWN = 4
