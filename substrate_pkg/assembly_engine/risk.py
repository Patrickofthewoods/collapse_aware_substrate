"""
Severity scoring and collapse-risk curve construction
for the assembly engine substrate.
"""


def score_severity(classification, regime_shifts, stability):
    """
    Compute severity score from regime classification,
    number of regime shifts, and stability.
    """
    base = 0.0

    if classification == "stable":
        base = 0.0
    elif classification == "neutral":
        base = 0.2
    elif classification == "mild-transition":
        base = 0.4
    elif classification == "destabilizing":
        base = 0.7
    elif classification == "highly-volatile":
        base = 0.9

    shift_factor = min(regime_shifts * 0.1, 0.3)
    stability_factor = (1.0 - stability) * 0.3

    severity = base + shift_factor + stability_factor
    return round(min(severity, 1.0), 2)


def build_severity(regimes):
    """
    Build severity entries for each regime classification.
    """
    severity_list = []

    for reg in regimes:
        classification = reg.get("classification")
        regime_shifts = reg.get("regime_shifts", 0)
        stability = reg.get("stability", 0.0)

        severity = score_severity(classification, regime_shifts, stability)

        severity_list.append({
            "index": reg.get("index"),
            "classification": classification,
            "severity": severity,
            "regime_shifts": regime_shifts,
            "stability": stability,
        })

    return severity_list


def build_risk_curve(severity_list):
    """
    Build collapse-risk curve from severity values.
    """
    curve = []

    for sev in severity_list:
        idx = sev.get("index")
        severity = sev.get("severity", 0.0)

        risk = severity  # direct mapping for now

        curve.append({
            "index": idx,
            "risk": risk,
            "severity": severity,
            "classification": sev.get("classification"),
        })

    return curve


def summarize_risk_curve(curve):
    """
    Summarize collapse-risk curve:
    - max/min/avg risk
    - peak index
    """
    if not curve:
        return {
            "max_risk": 0.0,
            "min_risk": 0.0,
            "avg_risk": 0.0,
            "peak_index": None,
        }

    risks = [pt["risk"] for pt in curve]
    max_risk = max(risks)
    min_risk = min(risks)
    avg_risk = sum(risks) / len(risks)

    peak_index = next(
        (pt["index"] for pt in curve if pt["risk"] == max_risk),
        None
    )

    return {
        "max_risk": round(max_risk, 2),
        "min_risk": round(min_risk, 2),
        "avg_risk": round(avg_risk, 2),
        "peak_index": peak_index,
    }
