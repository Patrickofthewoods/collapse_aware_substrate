"""
Full end-to-end substrate test.

This script:
    - generates telemetry streams
    - builds scenario signals
    - runs assembly engine
    - runs multi-profile ensemble inference
    - prints results cleanly

Place this file in the project root and run:
    python test_substrate.py
"""

from substrate_pkg.telemetry.generator import (
    generate_stable_stream,
    generate_fragile_stream,
    generate_collapse_stream,
    generate_cascade_stream,
)

# FIXED IMPORT — moved into scenario_engine folder
from substrate_pkg.scenario_engine.scenario_signals import build_scenario_signals

from substrate_pkg.assembly_engine.engine import AssemblyEngine


def run_single_test(name: str, records):
    print("\n==============================")
    print(f"=== {name.upper()} TEST ===")
    print("==============================")

    frame = {"records": records}

    # Scenario signals
    scenario = build_scenario_signals(frame)
    print("\nScenario Signals:")
    for k, v in scenario.items():
        print(f"  {k}: {v}")

    # Assembly profile
    engine = AssemblyEngine()
    assembly = engine.assemble(frame)
    print("\nAssembly Profile:")
    for k, v in assembly.items():
        print(f"  {k}: {v}")


def run_multi_profile_test():
    print("\n==============================")
    print("=== MULTI-PROFILE ENSEMBLE TEST ===")
    print("==============================")

    engine = AssemblyEngine()

    frames = [
        {"records": generate_stable_stream()},
        {"records": generate_fragile_stream()},
        {"records": generate_collapse_stream()},
        {"records": generate_cascade_stream()},
    ]

    ensemble = engine.assemble_many(frames)

    print("\nEnsemble Output:")
    for k, v in ensemble.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    # Run individual tests
    run_single_test("stable", generate_stable_stream())
    run_single_test("fragile", generate_fragile_stream())
    run_single_test("collapse", generate_collapse_stream())
    run_single_test("cascade", generate_cascade_stream())

    # Run ensemble test
    run_multi_profile_test()
