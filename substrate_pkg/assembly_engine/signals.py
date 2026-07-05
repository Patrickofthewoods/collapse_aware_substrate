"""
Signal extraction and basic status/confidence logic
for the assembly engine substrate.
"""


def find_nested(frame, key):
    """
    Recursively search for `key` inside nested `frame` structures.
    Assumes nested frames are stored under the "frame" key.
    """
    if key in frame:
        return frame[key]

    inner = frame.get("frame")
    if isinstance(inner, dict):
        return find_nested(inner, key)

    return {}


def extract_signals(scenario_frame):
    """
    Extract core signals from a scenario frame:
    - scenario status
    - cascade status
    - fragility signal
    """
    scenario_block = find_nested(scenario_frame, "scenario")
    cascade_block = find_nested(scenario_frame, "cascade")
    fragility_block = find_nested(scenario_frame, "fragility")

    return {
        "scenario_status": scenario_block.get("status", "unknown"),
        "cascade_status": cascade_block.get("status", "unknown"),
        "fragility_signal": fragility_block.get("signal", "unknown"),
    }


def compute_status(signals):
    """
    Compute assembly status from extracted signals.
    """
    if signals["scenario_status"] != "unresolved":
        return "structured"

    if signals["cascade_status"] == "unresolved":
        return "tentative"

    return "unknown"


def compute_confidence(signals):
    """
    Compute a simple confidence score based on signal presence.
    """
    score = 0.0

    if signals["scenario_status"] != "unknown":
        score += 0.4
    if signals["cascade_status"] != "unknown":
        score += 0.3
    if signals["fragility_signal"] != "unknown":
        score += 0.3

    return round(score, 2)


# ============================================================
# NEW REQUIRED FUNCTIONS
# ============================================================

def build_assembly_signals(frame):
    """
    Build numeric assembly signals from a scenario frame.
    This wraps extract_signals + compute_status + compute_confidence.
    """

    signals = extract_signals(frame)

    assembly_state = compute_status(signals)
    confidence = compute_confidence(signals)

    return {
        "assembly_state": assembly_state,
        "collapse_likely": signals["scenario_status"] == "collapse",
        "fragility_score": 1.0 if signals["fragility_signal"] != "unknown" else 0.0,
        "cascade_pressure": 1.0 if signals["cascade_status"] != "unknown" else 0.0,
        "confidence": confidence,
    }


def classify_regime(assembly_state, collapse_likely, fragility_score, cascade_pressure):
    """
    Classify the regime based on numeric assembly signals.
    """

    if cascade_pressure >= 0.67:
        return "cascade"

    if collapse_likely:
        return "collapse"

    if fragility_score >= 0.5:
        return "fragile"

    return "stable"
