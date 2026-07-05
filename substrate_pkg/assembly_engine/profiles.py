"""
Profile construction for the assembly engine substrate.
"""

from .signals import compute_confidence


def build_profile(signals):
    """
    Build a collapse-aware assembly profile from extracted signals.
    """
    return {
        "profile_type": "assembly-profile",
        "signal_vector": [
            signals["scenario_status"],
            signals["cascade_status"],
            signals["fragility_signal"],
        ],
        "confidence": compute_confidence(signals),
        "notes": "proto-profile constructed from substrate signals",
    }
