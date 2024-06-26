"""Methods to compare BPMNs by comparing all nodes with selected attributes."""

from exceptions import PrivateInternalException
from transformer.equality.utils import create_type_dict, to_comp_string
from transformer.models.bpmn.base import GenericBPMNNode
from transformer.models.bpmn.bpmn import (
    BPMN,
    Flow,
    LaneSet,
    Process,
)


def bpmn_element_to_comp_value(e: GenericBPMNNode | Flow):
    """Returns a concatenation of a by in/source and out/target comparable BPMN node."""
    if isinstance(e, LaneSet):
        return to_comp_string(
            [
                (lane.name, sorted(lane.flowNodeRefs))
                for lane in sorted(e.lanes, key=lambda x: x.id)
            ]
        )
    elif isinstance(e, GenericBPMNNode):
        return to_comp_string(e.id, e.name, sorted(e.outgoing), sorted(e.incoming))
    elif isinstance(e, Flow):
        return to_comp_string(e.name, e.sourceRef, e.targetRef)
    else:
        raise PrivateInternalException(f"Not supported BPMN Element: {type(e)}")


def bpmn_type_map(bpmn: Process):
    """Returns a by type grouped dictionary of the bpmn elements."""
    return create_type_dict(
        [*bpmn._flatten_node_typ_map(), *bpmn.flows, *bpmn.lane_sets],
        bpmn_element_to_comp_value,
    )


def get_all_processes_by_id(bpmn: Process, m: dict[str, Process]):
    """Get all subprocesses as a dictionary by ID (Recursive function)."""
    if bpmn.id not in m:
        m[bpmn.id] = bpmn
    if len(bpmn.subprocesses) == 0:
        return
    for subprocess in bpmn.subprocesses:
        m[subprocess.id] = subprocess
        get_all_processes_by_id(subprocess, m)


def get_organization(bpmn: BPMN):
    """Get the name of the organization of the pool if it exists."""
    if not bpmn.collaboration:
        return None
    if not bpmn.collaboration.participant:
        return None
    return bpmn.collaboration.participant.name


def compare_bpmn(bpmn1_comp: BPMN, bpmn2_comp: BPMN):
    """Returns a boolean if the diagrams are equal and an optional error message."""
    bpmn1_processes: dict[str, Process] = {}
    get_all_processes_by_id(bpmn1_comp.process, bpmn1_processes)
    bpmn2_processes: dict[str, Process] = {}
    get_all_processes_by_id(bpmn2_comp.process, bpmn2_processes)

    if bpmn1_processes.keys() != bpmn2_processes.keys():
        return False, "Wrong processes IDs"

    if get_organization(bpmn1_comp) != get_organization(bpmn2_comp):
        return False, "Wrong organizations"

    errors = []
    for bpmn_id, bpmn1 in bpmn1_processes.items():
        bpmn2 = bpmn2_processes[bpmn_id]

        bpmn1_types = bpmn_type_map(bpmn1)
        bpmn2_types = bpmn_type_map(bpmn2)

        if bpmn1_types.keys() != bpmn2_types.keys():
            return (
                False,
                f"""
Different Elements keys 1:
{bpmn1_types.keys()}
keys 2:
{bpmn2_types.keys()}""",
            )

        for k in bpmn1_types.keys():
            if bpmn1_types[k] != bpmn2_types[k]:
                diff_1_to_2 = bpmn1_types[k].difference(bpmn2_types[k])
                diff_2_to_1 = bpmn2_types[k].difference(bpmn1_types[k])
                errors.append(
                    f"{bpmn_id}\n{k} difference equality| 1 to 2: {
                        diff_1_to_2}| 2 to 1: {diff_2_to_1}"
                )
    if len(errors) > 0:
        joined_errors = "\n".join(errors)
        return False, f"Issues BPMN equality for types:\n{joined_errors}"
    return True, None
