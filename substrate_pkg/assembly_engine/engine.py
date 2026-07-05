from typing import Dict, Any

# FIXED IMPORT — now points to signals.py
from .signals import (
    build_assembly_signals,
    classify_regime,
)


class AssemblyEngine:
    """
    Assembly engine integrates scenario-level signals into
    a refined assembly profile with regime classification,
    confidence scoring, and signal vectors.
    """

    def assemble(self, scenario_frame: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a refined assembly profile from a single scenario frame.
        """

        # Numeric assembly signals
        signals = build_assembly_signals(scenario_frame)

        assembly_state = signals["assembly_state"]
        collapse_likely = signals["collapse_likely"]
        fragility_score = signals["fragility_score"]
        cascade_pressure = signals["cascade_pressure"]

        # Step 3: regime classification
        regime = classify_regime(
            assembly_state,
            collapse_likely,
            fragility_score,
            cascade_pressure,
        )

        # Step 3: confidence scoring
        confidence = round(
            fragility_score * 0.4 +
            cascade_pressure * 0.4 +
            (0.2 if collapse_likely else 0.0),
            2
        )
        confidence = min(confidence, 1.0)

        # Step 3: signal vector
        signal_vector = [
            assembly_state,
            collapse_likely,
            fragility_score,
            cascade_pressure,
        ]

        # Final assembly profile
        profile = {
            "profile_type": "assembly-profile",
            "regime": regime,
            "signal_vector": signal_vector,
            "confidence": confidence,
            "notes": "Refined assembly profile constructed from collapse-aware signals",
        }

        return {
            "assembly_state": assembly_state,
            "regime": regime,
            "confidence": confidence,
            "signal_vector": signal_vector,
            "collapse_likely": collapse_likely,
            "fragility_score": fragility_score,
            "cascade_pressure": cascade_pressure,
            "profile": profile,
            "structure": "assembly-profile",
        }

    def assemble_many(self, frames: list) -> Dict[str, Any]:
        """
        Multi-profile assembly aggregation with ensemble regime detection
        and aggregate confidence scoring.
        """

        profiles = [self.assemble(frame) for frame in frames]

        # Aggregate numeric signals
        avg_fragility = round(
            sum(p["fragility_score"] for p in profiles) / len(profiles),
            3
        )

        avg_cascade = round(
            sum(p["cascade_pressure"] for p in profiles) / len(profiles),
            3
        )

        collapse_rate = sum(
            1 for p in profiles if p["collapse_likely"]
        ) / len(profiles)

        # Aggregate regime (majority vote)
        regime_counts = {}
        for p in profiles:
            r = p["regime"]
            regime_counts[r] = regime_counts.get(r, 0) + 1

        ensemble_regime = max(regime_counts, key=regime_counts.get)

        # Ensemble confidence
        ensemble_confidence = round(
            avg_fragility * 0.4 +
            avg_cascade * 0.4 +
            (0.2 if collapse_rate >= 0.5 else 0.0),
            2
        )
        ensemble_confidence = min(ensemble_confidence, 1.0)

        # Ensemble signal vector
        ensemble_signal_vector = [
            ensemble_regime,
            collapse_rate,
            avg_fragility,
            avg_cascade,
        ]

        return {
            "profiles": profiles,
            "ensemble_regime": ensemble_regime,
            "ensemble_confidence": ensemble_confidence,
            "collapse_rate": collapse_rate,
            "avg_fragility": avg_fragility,
            "avg_cascade": avg_cascade,
            "ensemble_signal_vector": ensemble_signal_vector,
            "structure": "assembly-multi-profile",
        }
