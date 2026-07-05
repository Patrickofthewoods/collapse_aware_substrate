"""
Numeric fragility layer integrating collapse signals.
"""

from typing import Dict, Any
from .collapse_signals import build_collapse_signals


def compute_fragility_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute numeric fragility fields for a scenario frame.
    """
    collapse_bundle = build_collapse_signals(frame)
    signals = collapse_bundle["signals"]

    # FIXED: composite severity lives inside collapse_bundle["signals"]
    fragility_score = signals["composite_severity"]

    return {
        "fragility_score": fragility_score,
        "collapse_likely": collapse_bundle["collapse_likely"],
        "pressure_divergent": signals["pressure_divergent"],
        "volatility_spike": signals["volatility_spike"],
        "stress_threshold_cross": signals["stress_threshold_cross"],
        "structure": "fragility-signals",
    }


def build_fragility_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public interface for scenario_engine and cascade.
    """
    return compute_fragility_signals(frame)
