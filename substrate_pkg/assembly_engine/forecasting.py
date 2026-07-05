"""
Windowed collapse-pressure forecasting utilities
for the assembly engine substrate.
"""


def forecast_next_risk_linear(smoothed_curve, window=3):
    """
    Simple linear forecast using the last `window` smoothed points.
    Predicts next risk by extrapolating recent trend.
    """
    if not smoothed_curve:
        return {
            "forecast_risk": 0.0,
            "trend": "unknown",
            "window_used": 0,
        }

    # Use last `window` points
    tail = smoothed_curve[-window:]
    if len(tail) == 1:
        # Not enough points for a trend, just repeat last
        last = tail[-1]["smoothed_risk"]
        return {
            "forecast_risk": round(last, 3),
            "trend": "flat",
            "window_used": len(tail),
        }

    xs = [pt["index"] for pt in tail]
    ys = [pt["smoothed_risk"] for pt in tail]

    # Avoid division by zero if indices are identical
    dx = xs[-1] - xs[0]
    if dx == 0:
        slope = 0.0
    else:
        slope = (ys[-1] - ys[0]) / dx

    last_risk = ys[-1]
    forecast = last_risk + slope  # one-step linear extrapolation

    # Clamp to [0.0, 1.0]
    forecast = max(0.0, min(1.0, forecast))

    # Qualitative trend
    if slope > 0.01:
        trend = "rising"
    elif slope < -0.01:
        trend = "falling"
    else:
        trend = "flat"

    return {
        "forecast_risk": round(forecast, 3),
        "trend": trend,
        "window_used": len(tail),
        "slope": round(slope, 4),
    }


def build_forecast(smoothing):
    """
    Build windowed collapse-forecasting from smoothing outputs.
    Uses exponential smoothing by default.
    """
    exp_curve = smoothing.get("exponential", [])
    forecast = forecast_next_risk_linear(exp_curve, window=3)

    return {
        "method": "linear_windowed_over_exponential_smoothing",
        "forecast": forecast,
    }
