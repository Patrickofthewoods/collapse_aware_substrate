# Collapse‑Aware Substrate

A minimal, collapse‑aware inference substrate for modeling fragility, cascade pressure, and regime transitions across arbitrary systems.

## Overview

The Collapse‑Aware Substrate is a lightweight, domain‑independent inference framework designed to detect early‑stage fragility, estimate cascade pressure, and classify regime transitions across arbitrary systems. It provides a clean, minimal architecture suitable for:

- risk and fragility analysis
- simulation pipelines
- inference engines
- collapse‑aware decision systems
- research environments
- commercial modeling stacks

The substrate is intentionally minimal: no external dependencies, no domain coupling, and no heavy frameworks. It is built to be interpretable, portable, and commercial‑ready.

## Architecture

### Scenario Engine

Processes telemetry frames into numeric collapse‑aware signals:

- scenario state
- collapse likelihood
- fragility score
- cascade pressure

### Assembly Engine

Integrates scenario signals into refined assembly profiles:

- regime classification
- confidence scoring
- signal vectors
- multi‑profile ensemble inference

### Collapse Primitives

Core numeric primitives for:

- collapse severity
- fragility accumulation
- cascade acceleration

These primitives are intentionally simple and interpretable.

## Quickstart

```python
from substrate_pkg.scenario_engine.scenario_signals import build_scenario_signals
from substrate_pkg.assembly_engine.engine import AssemblyEngine

# Example telemetry frame
frame = {
    "records": [
        {"pressure": 0.2, "volatility": 0.1, "stress": 0.3},
        {"pressure": 0.4, "volatility": 0.2, "stress": 0.5},
    ]
}

# Scenario signals
scenario = build_scenario_signals(frame)

# Assembly profile
engine = AssemblyEngine()
profile = engine.assemble(scenario)

print(profile)
```

## Package Structure

```
collapse-aware-substrate/
│
├── substrate_pkg/
│   ├── scenario_engine/
│   │   └── scenario_signals.py
│   ├── assembly_engine/
│   │   ├── engine.py
│   │   └── signals.py
│   └── collapse_primitives/
│       └── core.py
│
├── test_substrate.py
├── LICENSE.txt
└── COMMERCIAL_LICENSE.md
```

## Licensing

This project uses a dual‑license model:

### Noncommercial Use

Licensed under PolyForm Noncommercial 1.0.0. See: `LICENSE.txt`

### Commercial Use

Requires a paid commercial license. See: `COMMERCIAL_LICENSE.md`

Commercial use includes:

- internal use at for‑profit organizations
- integration into commercial products
- AI/model training
- enterprise inference pipelines
- consulting deliverables
- any revenue‑generating or cost‑reducing system

To obtain a commercial license, contact: pdn.nyhan@gmail.com

## Status: Early Commercial Release (v0.1.0)

The architecture is stable, the pipeline runs end‑to‑end, and the commercial license is active.

Upcoming improvements include:

- enhanced numeric assembly signals
- refined confidence scoring
- expanded collapse primitives
- coordination rules
- example notebooks
- API documentation

## Roadmap

- v0.2 — Full numeric assembly layer
- v0.3 — Coordination rules + regime refinement
- v0.4 — Collapse primitive extensions
- v0.5 — Visualization utilities
- v1.0 — Commercial‑ready substrate release

## Citation

```
Nyhan, Patrick D. (2026). Collapse‑Aware Substrate: A Minimal Parity‑Driven Inference Framework.
```

## Contact

For licensing, collaboration, or enterprise integration: pdn.nyhan@gmail.com
