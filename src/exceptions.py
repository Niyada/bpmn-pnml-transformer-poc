from enum import Enum

class DeterminedException(Exception, Enum):
    """Base class for all known exceptions."""

    ENV_VARIABLE_NOT_SET = 1
    QUERY_PARAMS_NOT_SUPPORTED = 2
    BPMN_ELEMENT_NOT_SUPPORTED = 3
    PETRI_NET_ELEMENT_NOT_SUPPORTED = 4
    PAGE_SUBNET_ID_MISSING = 5
    TAG_NOT_SUPPORTED = 6
    FLOW_ALREADY_EXISTS = 7
    NO_BPMN_NODE = 8
    NODE_NOT_EXIST = 9
    IDENTICAL_PETRINET_ELEMENTS = 10
    ARC_ALREADY_EXISTS = 11
    NO_PETRINET_NODE = 12
    NONEXISTING_NODE = 13
    PAGE_NOT_FOUND = 14
    NO_PETRINET_NODE = 15
    OLD_ELEMENT_NOT_EXISTING = 16
    NEW_ID_ALREADY_EXISTS = 17
    UNNAMED_LANES = 18
    INVALID_PETRINET_NODE = 19
    WRONG_INTERMEDIATE_EVENT_TYPE = 20
    SUBPROCESS_FLOW_REQUIREMENT = 21
    NODE_TYPE_NOT_SUPPORTED = 22
    SUBPROCESS_START_END_EVENTS = 23
    SHOULD_NOT_HAPPEN = 24
    INVALID = 25
    NOT_POSSIBLE = 26
    RESOURCES_ORGANIZATION = 27
    SHOULD_NOT_BE_POSSIBLE = 28
    SOURCE_TARGET_MISSING = 29

    def __str__(self):
        """Return a string representation of the exception."""
        return self.name.replace("_", " ").capitalize()