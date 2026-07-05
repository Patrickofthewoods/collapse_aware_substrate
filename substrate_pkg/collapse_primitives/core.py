"""
Core collapse primitives.

These functions convert raw telemetry records into
collapse-aware numeric signals used by scenario and
assembly engines.
"""

from typing import Dict, List


def compute_collapse_severity(record: Dict[str, float]) -> float:
    """
    Compute collapse severity from a single telemetry record.

    Expected fields:
        - pressure
        - volatility
        - stress
    """

    pressure = record.get("pressure", 0.0)
    volatility = record.get("volatility", 0.0)
    stress = record.get("stress", 0.0)

    # Weighted combination (simple but real)
    severity = (
        0.4 * pressure +
        0.3 * volatility +
        0.3 * stress
    )

    return max(0.0, min(severity, 1.0))


def compute_fragility(records: List[Dict[str, float]]) -> float:
    """
    Fragility = average of the top 3 collapse severities.
    """

    if not records:
        return 0.0

    severities = [compute_collapse_severity(r) for r in records]
    top = sorted(severities, reverse=True)[:3]

    return round(sum(top) / len(top), 3)


def compute_cascade_pressure(records: List[Dict[str, float]]) -> float:
    """
    Cascade pressure = acceleration of collapse severity.
    """

    if len(records) < 2:
        return 0.0

    severities = [compute_collapse_severity(r) for r in records]

    deltas = [
        severities[i+1] - severities[i]
        for i in range(len(severities) - 1)
    ]

    avg_delta = sum(deltas) / len(deltas)

    # Positive acceleration → higher cascade pressure
    pressure = avg_delta * 3.0

    return round(max(0.0, min(pressure, 1.0)), 3)
