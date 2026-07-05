"""
Temporal smoothing utilities for collapse-risk curves
in the assembly engine substrate.
"""


def smooth_moving_average(curve, window=3):
    """
    Apply a simple moving-average smoothing over the risk curve.
    """
    if not curve:
        return []

    smoothed = []
    risks = [pt["risk"] for pt in curve]

    for i in range(len(risks)):
        start = max(0, i - window + 1)
        window_vals = risks[start:i + 1]
        avg = sum(window_vals) / len(window_vals)

        smoothed.append({
            "index": curve[i]["index"],
            "smoothed_risk": round(avg, 3),
        })

    return smoothed


def smooth_exponential(curve, alpha=0.5):
    """
    Apply exponential smoothing over the risk curve.
    """
    if not curve:
        return []

    smoothed = []
    prev = curve[0]["risk"]

    for pt in curve:
        risk = pt["risk"]
        smoothed_val = alpha * risk + (1 - alpha) * prev
        prev = smoothed_val

        smoothed.append({
            "index": pt["index"],
            "smoothed_risk": round(smoothed_val, 3),
        })

    return smoothed


def build_smoothing(risk_curve):
    """
    Build both moving-average and exponential smoothing outputs.
    """
    return {
        "moving_average": smooth_moving_average(risk_curve, window=3),
        "exponential": smooth_exponential(risk_curve, alpha=0.5),
    }
