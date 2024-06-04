"""Shared PNML related helper functions."""

from transformer.models.pnml.base import NetElement
from transformer.models.pnml.pnml import Net


def generate_explicit_transition_id(id: str):
    """Prepend EXPLICIT to the id."""
    return f"EXPLICIT{id}"


def generate_explicit_trigger_id(id: str):
    """Prepend EXPLICIT to the id."""
    return f"TRIGGER{id}"


def generate_source_id(id: str):
    """Prepend SOURCE to the id."""
    return f"SOURCE{id}"


def generate_sink_id(id: str):
    """Prepend SINK to the id."""
    return f"SINK{id}"


def find_triggers(net: Net):
    """Find all event triggers."""
    net_elements: list[NetElement] = [*net.transitions, *net.places]
    triggers: list[NetElement] = [
        trigger for trigger in net_elements if trigger.is_workflow_event_trigger()
    ]
    return triggers
