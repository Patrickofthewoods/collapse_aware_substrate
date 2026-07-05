"""
Numeric collapse-signal analysis for the collapse-aware substrate.

This module detects collapse-relevant behavior in scenario record chains:
- divergence
- volatility spikes
- stress threshold crossings
- composite collapse severity

These signals feed into:
- fragility.py
- cascade.py
- scenario_engine.py
- assembly_engine (indirectly)
"""

from typing import List, Dict, Any


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def compute_delta(prev: float, curr: float) -> float:
    """
    Basic numeric delta between two values.
    """
    return curr - prev


def extract_metric_series(records: List[Dict[str, Any]], key: str) -> List[float]:
    """
    Extract a numeric series from records using a given key.
    Missing or non-numeric values are skipped.
    """
    series = []
    for rec in records:
        val = rec.get(key)
        if isinstance(val, (int, float)):
            series.append(float(val))
    return series


# ------------------------------------------------------------
# Collapse-signal detectors
# ------------------------------------------------------------

def is_divergent(series: List[float], threshold: float = 0.2) -> bool:
    """
    Detect divergence in a numeric series based on cumulative change.
    """
    if len(series) < 2:
        return False

    total_change = abs(series[-1] - series[0])
    return total_change >= threshold


def has_spike(series: List[float], spike_factor: float = 2.0) -> bool:
    """
    Detect a spike where a single step change is much larger
    than the typical change.
    """
    if len(series) < 3:
        return False

    deltas = [abs(series[i] - series[i - 1]) for i in range(1, len(series))]
    avg_delta = sum(deltas[:-1]) / max(len(deltas) - 1, 1)
    last_delta = deltas[-1]

    return avg_delta > 0 and last_delta >= spike_factor * avg_delta


def crosses_threshold(series: List[float], threshold: float = 0.8) -> bool:
    """
    Detect whether the series crosses a collapse-relevant threshold.
    """
    return any(val >= threshold for val in series)


# ------------------------------------------------------------
# Main collapse-signal analysis
# ------------------------------------------------------------

def analyze_collapse_signals(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze a record chain for collapse-relevant signals.

    Expected record structure:
    - each record may contain numeric metrics like:
      - "pressure"
      - "volatility"
      - "stress"

    Returns a collapse-signal bundle:
    - divergence
    - spike
    - threshold_cross
    - composite_severity
    """
    pressure_series = extract_metric_series(records, "pressure")
    volatility_series = extract_metric_series(records, "volatility")
    stress_series = extract_metric_series(records, "stress")

    pressure_divergent = is_divergent(pressure_series, threshold=0.2)
    volatility_spike = has_spike(volatility_series, spike_factor=2.0)
    stress_threshold = crosses_threshold(stress_series, threshold=0.8)

    # Simple composite severity: count how many signals are active
    active_signals = sum([
        1 if pressure_divergent else 0,
        1 if volatility_spike else 0,
        1 if stress_threshold else 0,
    ])

    composite_severity = round(active_signals / 3.0, 2)

    return {
        "pressure_divergent": pressure_divergent,
        "volatility_spike": volatility_spike,
        "stress_threshold_cross": stress_threshold,
        "composite_severity": composite_severity,
    }


# ------------------------------------------------------------
# Public primitive interface
# ------------------------------------------------------------

def build_collapse_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a collapse-signal bundle from a scenario frame.

    Assumes nested records live under:
    frame["frame"]["frame"]["frame"]["records"]
    (matching your lineage source chain).
    """
    records = (
        frame.get("frame", {})
             .get("frame", {})
             .get("frame", {})
             .get("records", [])
    )

    signals = analyze_collapse_signals(records)

    collapse_likely = signals["composite_severity"] >= 0.67

    return {
        "collapse_likely": collapse_likely,
        "signals": signals,
        "structure": "collapse-signals",
    }
