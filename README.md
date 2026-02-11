# GIAMS — General Infrastructure Asset Management Systems

**Open-source, extensible, and modular platform for infrastructure asset management** at both project- and network-levels. GIAMS is developed in Python to support research and practice in lifecycle analysis, maintenance–repair–rehabilitation (MRR) planning, and optimization for civil infrastructure (e.g. bridges, buildings).

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Concepts](#concepts)
- [Testing](#testing)
- [Extending GIAMS](#extending-giams)
- [Citing](#citing)
- [License](#license)

---

## Overview

GIAMS provides a unified framework to:

- **Model assets** (bridges, buildings) as collections of elements with condition states, deterioration, agency and user costs, and utility.
- **Simulate life cycles** via Monte Carlo over a planning horizon, with optional hazard (e.g. seismic) events, response, loss, and recovery.
- **Optimize MRR plans** at project level (single asset) or network level (multiple assets under budget) using genetic algorithms, particle swarm, hill climbing, brute force, or custom objectives.
- **Plug in new models** by extending base classes for assets, elements, deterioration, condition rating, hazards, MRR actions, and optimizers.

Example applications include the **Indiana bridge network** (4,600+ bridges) with HAZUS-based seismic response and Texas DOT–style user costs, dummy building retrofit with the Rank optimizer, and structural health monitoring (SHM) scenarios.

---

## Features

| Area | Description |
|------|-------------|
| **Modular design** | Pluggable models for deterioration, condition rating, agency and user costs, hazards (generator, response, loss, recovery), and MRR actions. |
| **Project-level optimization** | Life-cycle analysis (LCA) with Monte Carlo simulation; optimization via genetic algorithms (GA), particle swarm (PSO), hill climbing, brute force, and custom objectives. |
| **Network-level analysis** | Multiple assets, budget constraints, and network-wide objectives (e.g. utility holism, IUC). |
| **Extensibility** | Base classes for assets, elements, simulators, and optimizers so you can add new asset types and models without changing core logic. |
| **Real-world data** | Indiana bridge network with HAZUS-based seismic response and Texas DOT–style user costs; additional networks (First, Random, Dummy) for experimentation. |
| **RL support** | Reinforcement learning environments (e.g. `IndianaEnv`) for agent-based optimization. |

---

## Installation

**Requirements:** Python 3.9+. Dependencies are declared in `pyproject.toml` (numpy, pandas, matplotlib, scipy, deap, pyswarms).

### Using [uv](https://github.com/astral-sh/uv) (recommended)

```bash
git clone <your-repo-url>
cd GIAMS
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Using pip

```bash
cd GIAMS
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

The `[dev]` extra adds pytest and pytest-cov for running tests.

---

## Quick Start

**Run the default project-level Indiana bridge example** (single asset, LCA + NPV output):

```bash
python run.py
```

From Python:

```python
from Examples import Example1
Example1.example1()
```

**Try different optimizers** (uncomment in `run.py` or call directly):

```python
from Examples import Example1

# Life-cycle analysis only
Example1.example1()

# Optimization
Example1.GA_test()        # Genetic algorithm
Example1.hill_climbing()  # Hill climbing
Example1.brute_force()    # Brute force
Example1.pso()            # Particle swarm
```

---

## Project Structure

```
GIAMS/
├── Asset/                    # Asset types and element models
│   ├── AssetTypes/          # BaseAsset, Bridge, Building
│   ├── Elements/            # Bridge/Building elements; condition rating, deterioration,
│   │                        # agency cost, utility (e.g. BRIDGIT, NBI, Sinha, Bai, HAZUS)
│   ├── HazardModels/        # Generator, Response, Loss, Recovery (e.g. Poisson, HAZUS)
│   ├── MRRModels/           # MRR plans and effectiveness (e.g. MRRTwoActions, SHM)
│   └── UserCostModels/      # Texas DOT, dummy building, etc.
├── Network/                 # Network loaders and budget setup
│   ├── Networks/            # Data: INDIANA2019.csv, FirstNetwork.csv
│   ├── BaseNetwork.py
│   ├── IndianaNetwork.py
│   ├── FirstNetwork.py, RandomNetwork.py
│   └── DummyBuildingNetwork.py, DummySHMNetwork.py
├── LifeCycleAnalyzer/       # LCA engine and simulators
│   ├── BaseLCA.py, LCA.py
│   └── Simulators/          # MainSimulator, EnvSimulator, SHMSimulator, DummyRiskAnalyzer
├── Optimizer/               # GA, PSO, HillClimbing, BruteForce, IUC, Rank; objectives
├── utils/                   # NPV, accumulators, distributions, predictive models,
│                            # logging, timing, GeneralSettings
├── Examples/                # Example1–3, EstLca, BuildingRetrofitDummy, SHMExample
├── RLEnvs/                  # BaseEnv, IndianaEnv (reinforcement learning)
├── tests/                   # Pytest suite
├── run.py                   # Entry point (Example1.example1 by default)
└── pyproject.toml
```

| Package | Description |
|---------|-------------|
| **Asset** | Asset types (Bridge, Building), elements (deck, superstructure, substructure, etc.), condition rating (NBI, BRIDGIT, PONTIS, China, Japan, Korea), deterioration (Markovian, continuous), agency/user costs, hazard (generator, response, loss, recovery), MRR models and effectiveness. |
| **Network** | Network loaders (Indiana, First, Random, DummyBuilding, DummySHM), budget limits and NPV budget; data in `Network/Networks/`. |
| **LifeCycleAnalyzer** | Base LCA and Monte Carlo LCA; simulators (Main, Env, SHM, Dummy) that produce single-asset or network life-cycle instances. |
| **Optimizer** | GA, PSO, hill climbing, brute force, IUC, Rank; objective wrappers for LCA-based fitness. |
| **utils** | NPV, accumulators (AccumulatorThree, AccumulatorX), containers, distributions (Normal, LogNormal, Beta, etc.), predictive models (Linear, GBM, Wiener drift, etc.), logging, timing, general settings. |
| **Examples** | Example1 (project-level Indiana LCA + optimizers), Example2 (IUC), Example3 (GA validation), EstLca, BuildingRetrofitDummy, SHMExample. |
| **RLEnvs** | RL environments (e.g. IndianaEnv) for agent-based optimization. |

---

## Examples

| Example | Purpose |
|---------|---------|
| **Example1** | Project-level LCA and optimization for a single Indiana bridge: `example1()` (LCA only), `GA_test()`, `hill_climbing()`, `brute_force()`, `pso()`. |
| **Example2** | Network-level IUC (Incremental Utility–Cost) optimization over the Indiana network. |
| **Example3** | GA validation and project selection (multiprocessing, near-optimal comparison). |
| **EstLca** | Estimated LCA with random network and multiprocessing. |
| **BuildingRetrofitDummy** | Dummy building retrofit with Rank optimizer. |
| **SHMExample** | Structural health monitoring (SHM) actions and effectiveness. |

Data files (`INDIANA2019.csv`, `FirstNetwork.csv`) are in `Network/Networks/`.

---

## Concepts

- **LCA (Life-Cycle Analysis):** Monte Carlo simulation over a planning horizon; each run uses a simulator to generate user costs, element costs, utilities, and condition states; results are accumulated and used for NPV and objectives.
- **MRR (Maintenance, Repair, Rehabilitation):** Actions applied to elements over time; modeled via MRR plans (e.g. MRRTwoActions, MRRFourActions, SHMActions) and effectiveness models.
- **Hazard:** Optional events (e.g. earthquakes via Poisson process); each event triggers response (e.g. HAZUS fragility), loss, and recovery.
- **Optimization:** Optimizers search over MRR (or similar) decision variables; fitness is typically an LCA-derived objective (e.g. utility / user-cost trade-off). IUC and Rank support network-level project selection under budget.

---

## Testing

Run the test suite:

```bash
uv run pytest
# or
pytest
```

With coverage:

```bash
uv run pytest --cov=Asset --cov=LifeCycleAnalyzer --cov=Optimizer --cov=Network --cov=utils --cov-report=term-missing
```

---

## Extending GIAMS

The codebase is structured for drop-in extensions:

| Extension | Base / pattern |
|-----------|----------------|
| **New asset type** | Extend `Asset.AssetTypes.BaseAsset`; use in network and simulators. |
| **New deterioration / condition / utility / agency cost / MRR** | Implement the corresponding base class under `Asset.Elements` or `Asset.MRRModels`. |
| **New hazard (generator, response, loss, recovery)** | Extend classes in `Asset.HazardModels` (Generator, Response, Loss, Recovery). |
| **New network** | Extend `Network.BaseNetwork` and implement `load_asset()` (and any loader-specific logic). |
| **New simulator** | Extend `LifeCycleAnalyzer.Simulators.BaseSimulator` and implement `get_one_instance()`. |
| **New optimizer** | Follow the pattern of `Optimizer.GA` or `Optimizer.HillClimbing`; use `_objectives.LCASolution` for LCA-based objectives. |

For optional refactoring ideas (e.g. type hints, docstrings, layout), see [REFACTORING_REMAINING.md](REFACTORING_REMAINING.md).

---

## Citing

If you use GIAMS in your research, please cite the paper that describes the platform and its modules (the open-source, extensible asset management system and the Indiana bridge applications). See the project repository or publication list for the exact reference.

---

## License

This project is licensed under the MIT License — see [LICENSE.md](LICENSE.md) for details.
