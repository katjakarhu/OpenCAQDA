import enum


class CodeRelationshipEnum(enum.Enum):
    CUSTOM = 1  # User can assign a label for the relationship
    PARENT = 2
    RELATES_TO = 3
    POSITIVELY_IMPACTS = 4
    NEGATIVELY_IMPACTS = 5
    CO_OCCURS = 6
    RESULTS_FROM = 7
