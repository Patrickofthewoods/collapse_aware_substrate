"""
Lineage attachment and temporal trajectory construction
for the assembly engine substrate.
"""

from .signals import find_nested


def attach_lineage(profiles, frames):
    """
    Attach lineage metadata to each profile:
    - index
    - source record chain
    - ancestry (cascade/scenario/fragility)
    """
    lineage = []

    for idx, (profile, frame) in enumerate(zip(profiles, frames)):
        lineage.append({
            "index": idx,
            "source": (
                frame.get("frame", {})
                     .get("frame", {})
                     .get("frame", {})
                     .get("records", [])
            ),
            "ancestry": {
                "cascade": find_nested(frame, "cascade").get("status", "unknown"),
                "scenario": find_nested(frame, "scenario").get("status", "unknown"),
                "fragility": find_nested(frame, "fragility").get("signal", "unknown"),
            }
        })

    return lineage


def build_trajectories(lineage):
    """
    Build temporal trajectories from lineage ancestry.
    Each trajectory is a sequence of states:
    [cascade_status, scenario_status, fragility_signal]
    """
    trajectories = []

    for entry in lineage:
        ancestry = entry.get("ancestry", {})
        trajectories.append({
            "index": entry.get("index"),
            "path": [
                ancestry.get("cascade", "unknown"),
                ancestry.get("scenario", "unknown"),
                ancestry.get("fragility", "unknown"),
            ],
        })

    return trajectories
