"""
Numeric cascade layer integrating fragility signals.

This module determines whether fragility signals should trigger
cascade propagation across frames.
"""

from typing import Dict, Any
from .fragility_signals import build_fragility_signals


def compute_cascade_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute numeric cascade triggers based on fragility signals.
    """

    frag = build_fragility_signals(frame)

    # Core cascade trigger: collapse-likely OR high fragility score
    cascade_trigger = (
        frag["collapse_likely"] or
        frag["fragility_score"] >= 0.67
    )

    # Additional cascade pressure indicators
    pressure = frag["pressure_divergent"]
    spike = frag["volatility_spike"]
    stress = frag["stress_threshold_cross"]

    cascade_pressure = sum([
        1 if pressure else 0,
        1 if spike else 0,
        1 if stress else 0,
    ])

    cascade_pressure = round(cascade_pressure / 3.0, 2)

    return {
        "cascade_trigger": cascade_trigger,
        "cascade_pressure": cascade_pressure,
        "pressure_divergent": pressure,
        "volatility_spike": spike,
        "stress_threshold_cross": stress,
        "structure": "cascade-signals",
    }


def build_cascade_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public interface for scenario_engine and assembly_engine.
    """
    return compute_cascade_signals(frame)
