# Remaining Refactoring Opportunities

This document lists optional improvements that were **not** required for the initial refactor. They can be done incrementally without changing behavior.

---

## 1. **Wildcard imports** (low risk, improves clarity)

Many files use `from module import *`, which pollutes the namespace and makes it unclear what is used.

**Examples:**
- `from utils.GeneralSettings import *` → replace with explicit imports, e.g. `from utils.GeneralSettings import DONOT, MAINT, REHAB, RECON, n_steps, ...` (or a single `import utils.GeneralSettings as gs` and use `gs.DONOT`).
- `from .BaseNetwork import *` in network subclasses → import only the symbols each file needs (e.g. `Bridge`, `AccumulatorThree`, `Linear`, ...).
- Same idea for `BaseElement`, `BaseMRRPlan`, `BaseRecovery`, `BaseHazard`, `BaseMRREffectiveness`, `BridgeElementsUtilityBai2013`, `AgencyCostSinha2009`.

**Where:** `Network/BaseNetwork.py`, all `Network/*.py`, `LifeCycleAnalyzer/Simulators/*.py`, `Asset/MRRModels/**`, `Asset/HazardModels/**`, `Asset/Elements/**`, `utils/Container.py`, `utils/Accumulator*.py`, `Examples/*.py`.

---

## 2. **Type hints** (optional, improves IDE and docs)

Add type annotations to public functions and constructors, e.g.:

- `def NPV(costs_list: Sequence[float], dt: float, r: float = 0.06) -> float`
- `def __init__(self, *, settings: Any, ID: int, ...) -> None`

Start with `utils` and main entry points; use `typing` and `from __future__ import annotations` if needed for forward refs.

---

## 3. **Assert vs ValueError in library code** (optional)

Some checks use `assert` (e.g. `BaseElement.add_age`, `GA.__init__`). Asserts can be disabled with `python -O`. For a library, raising `ValueError` (or `TypeError`) is often preferred so callers always get clear errors.

**Example:** `assert isinstance(increment, int)` → `if not isinstance(increment, int): raise TypeError("increment must be integer")`.

---

## 4. **Docstrings and comments** (optional)

- Ensure all public modules have a one-line module docstring.
- Standardize docstring style (e.g. Google or NumPy) for public classes and methods.
- Fix remaining typos in comments (e.g. "mdoels" in BasePredictiveModel, "paassed" in LCA).

---

## 5. **GeneralSettings constants** (done in this pass)

- Removed duplicate `DONOT = 0` in SHM section and added a short comment.
- Consider grouping constants in a dataclass or namespace if you want to avoid star imports and get better discovery.

---

## 6. **File and package layout** (larger change)

The original plan mentioned:

- Moving to `src/giams/` layout.
- Renaming packages to lowercase/snake_case (e.g. `LifeCycleAnalyzer` → `life_cycle_analyzer`).
- Renaming module files to snake_case (e.g. `BaseAsset.py` → `base_asset.py`).

This would require updating every import and is best done in a dedicated branch/PR.

---

## 7. **Testing**

- Add tests for more modules (e.g. `AccumulatorThree` update, `LCA.check_budget` with mocks, one `Network` loader with a tiny CSV).
- Add a single integration test that runs one example (e.g. dummy building) end-to-end if data files are present.
- Consider `pytest.ini` or `pyproject.toml` for coverage thresholds and markers.

---

## 8. **CI and tooling** (optional)

- Run tests and a linter (e.g. ruff) in CI.
- Add `ruff format` or `black` and `isort` for consistent style (already have ruff in pyproject.toml).

---

## Summary of what was done in this pass

- Fixed typos: `optimiztion` → `optimization`, `rehabiliation` → `rehabilitation`, `replcement` → `replacement`, `conidtion` → `condition` in comments.
- Removed duplicate `DONOT` in `GeneralSettings` and clarified with a comment.

Everything above is optional; the codebase is already in a good state for use and further refactoring.
