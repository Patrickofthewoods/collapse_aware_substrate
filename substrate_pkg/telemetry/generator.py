"""
Telemetry generator for collapse-aware substrate.

Produces synthetic telemetry streams with fields:
    - pressure
    - volatility
    - stress

Used to drive scenario and assembly engines for testing
and demonstration.
"""

from typing import List, Dict
import random


def _clamp(x: float) -> float:
    return max(0.0, min(x, 1.0))


def generate_stable_stream(
    length: int = 20,
    base_pressure: float = 0.2,
    base_volatility: float = 0.2,
    base_stress: float = 0.2,
) -> List[Dict[str, float]]:
    """
    Stable: low, gently varying signals.
    """

    records = []
    for _ in range(length):
        pressure = _clamp(base_pressure + random.uniform(-0.05, 0.05))
        volatility = _clamp(base_volatility + random.uniform(-0.05, 0.05))
        stress = _clamp(base_stress + random.uniform(-0.05, 0.05))

        records.append({
            "pressure": pressure,
            "volatility": volatility,
            "stress": stress,
        })

    return records


def generate_fragile_stream(
    length: int = 20,
    start_pressure: float = 0.3,
    end_pressure: float = 0.7,
    base_volatility: float = 0.4,
    base_stress: float = 0.4,
) -> List[Dict[str, float]]:
    """
    Fragile: rising pressure, moderate volatility/stress.
    """

    records = []
    for i in range(length):
        t = i / max(1, length - 1)
        pressure = _clamp(start_pressure + t * (end_pressure - start_pressure) + random.uniform(-0.05, 0.05))
        volatility = _clamp(base_volatility + random.uniform(-0.1, 0.1))
        stress = _clamp(base_stress + random.uniform(-0.1, 0.1))

        records.append({
            "pressure": pressure,
            "volatility": volatility,
            "stress": stress,
        })

    return records


def generate_collapse_stream(
    length: int = 20,
    base_pressure: float = 0.7,
    base_volatility: float = 0.6,
    base_stress: float = 0.7,
) -> List[Dict[str, float]]:
    """
    Collapse: high, noisy signals.
    """

    records = []
    for _ in range(length):
        pressure = _clamp(base_pressure + random.uniform(-0.1, 0.1))
        volatility = _clamp(base_volatility + random.uniform(-0.15, 0.15))
        stress = _clamp(base_stress + random.uniform(-0.1, 0.1))

        records.append({
            "pressure": pressure,
            "volatility": volatility,
            "stress": stress,
        })

    return records


def generate_cascade_stream(
    length: int = 20,
    start_pressure: float = 0.4,
    end_pressure: float = 1.0,
    start_stress: float = 0.4,
    end_stress: float = 1.0,
    base_volatility: float = 0.6,
) -> List[Dict[str, float]]:
    """
    Cascade: accelerating severity (pressure + stress ramp).
    """

    records = []
    for i in range(length):
        t = i / max(1, length - 1)
        pressure = _clamp(start_pressure + t * (end_pressure - start_pressure) + random.uniform(-0.05, 0.05))
        stress = _clamp(start_stress + t * (end_stress - start_stress) + random.uniform(-0.05, 0.05))
        volatility = _clamp(base_volatility + random.uniform(-0.1, 0.1))

        records.append({
            "pressure": pressure,
            "volatility": volatility,
            "stress": stress,
        })

    return records


def generate_random_stream(
    length: int = 20,
) -> List[Dict[str, float]]:
    """
    Random: exploratory noise.
    """

    records = []
    for _ in range(length):
        records.append({
            "pressure": random.uniform(0.0, 1.0),
            "volatility": random.uniform(0.0, 1.0),
            "stress": random.uniform(0.0, 1.0),
        })

    return records
