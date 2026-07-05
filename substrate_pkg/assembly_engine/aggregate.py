"""
Aggregation utilities for multi-profile assembly
in the collapse-aware substrate.
"""


def aggregate_profiles(profiles):
    """
    Aggregate multiple assembly profiles:
    - count
    - average confidence
    - distinct profile types
    """
    if not profiles:
        return {
            "count": 0,
            "avg_confidence": 0.0,
            "profile_types": [],
        }

    count = len(profiles)
    avg_conf = sum(p.get("confidence", 0.0) for p in profiles) / count
    types = list({p.get("profile_type", "unknown") for p in profiles})

    return {
        "count": count,
        "avg_confidence": round(avg_conf, 2),
        "profile_types": types,
    }
