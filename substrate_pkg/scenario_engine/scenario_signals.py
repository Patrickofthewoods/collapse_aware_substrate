"""
Scenario-level numeric signals.

This module computes collapse severity, fragility, and
cascade pressure from telemetry records, producing a
scenario_state used by the assembly engine.
"""

from typing import Dict, Any, List

# Import numeric primitives (FIXED: now using absolute import)
from substrate_pkg.collapse_primitives.core import (
    compute_collapse_severity,
    compute_fragility,
    compute_cascade_pressure,
)


def build_scenario_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute scenario-level numeric signals from a telemetry frame.

    Expected frame structure:
        {
            "records": [
                {"pressure": ..., "volatility": ..., "stress": ...},
                ...
            ]
        }
    """

    records: List[Dict[str, float]] = frame.get("records", [])

    if not records:
        return {
            "scenario_state": "stable",
            "collapse_likely": False,
            "fragility_score": 0.0,
            "cascade_pressure": 0.0,
            "structure": "scenario-signals",
        }

    # Collapse severity from the most recent record
    latest_record = records[-1]
    collapse_severity = compute_collapse_severity(latest_record)

    # Fragility from all records
    fragility_score = compute_fragility(records)

    # Cascade pressure from acceleration across records
    cascade_pressure = compute_cascade_pressure(records)

    # Collapse likelihood threshold
    collapse_likely = collapse_severity >= 0.6

    # Scenario state classification
    if cascade_pressure >= 0.67:
        scenario_state = "cascade"
    elif collapse_likely:
        scenario_state = "collapse"
    elif fragility_score >= 0.5:
        scenario_state = "fragile"
    else:
        scenario_state = "stable"

    return {
        "scenario_state": scenario_state,
        "collapse_likely": collapse_likely,
        "fragility_score": fragility_score,
        "cascade_pressure": cascade_pressure,
        "structure": "scenario-signals",
    }
