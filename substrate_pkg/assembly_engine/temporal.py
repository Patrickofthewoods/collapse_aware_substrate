"""
Temporal delta computation and regime-shift classification
for the assembly engine substrate.
"""


def build_deltas(trajectories):
    """
    Compute deltas (transitions, regime shifts, stability)
    from temporal trajectories.
    """
    deltas = []

    for traj in trajectories:
        path = traj.get("path", [])
        transitions = []
        regime_shifts = 0

        for i in range(1, len(path)):
            prev_state = path[i - 1]
            curr_state = path[i]
            transitions.append({"from": prev_state, "to": curr_state})

            if prev_state != curr_state:
                regime_shifts += 1

        stability = 1.0 / (1 + regime_shifts)

        deltas.append({
            "index": traj.get("index"),
            "transitions": transitions,
            "regime_shifts": regime_shifts,
            "stability": round(stability, 2),
        })

    return deltas


def classify_regime_shift(delta):
    """
    Classify regime behavior based on regime shifts and stability.
    """
    regime_shifts = delta.get("regime_shifts", 0)
    stability = delta.get("stability", 0.0)

    if regime_shifts == 0 and stability == 1.0:
        return "stable"
    if regime_shifts > 2 and stability < 0.4:
        return "highly-volatile"
    if regime_shifts == 1 and stability >= 0.5:
        return "mild-transition"
    if regime_shifts >= 1 and stability < 0.5:
        return "destabilizing"

    return "neutral"


def build_regimes(deltas):
    """
    Build regime classifications for each delta entry.
    """
    regimes = []

    for delta in deltas:
        classification = classify_regime_shift(delta)
        regimes.append({
            "index": delta.get("index"),
            "classification": classification,
            "regime_shifts": delta.get("regime_shifts", 0),
            "stability": delta.get("stability", 0.0),
        })

    return regimes
