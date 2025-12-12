Cleanup summary

What I changed:

- `ComputationalProject`:
  - Introduced `integrator.py` as canonical numerical code; refactored `numericalIntegrator.py` and `visualizer.py` to import from it.
  - Added `__init__.py` for package imports.
  - Added Makefile to run integrator and visualizer.

- `Pset6`:
  - Canonical scripts: `6b.py`, `6c.py`, `partcatt4.py`, `Pset6a.py`.
  - Archived scripts: `6catt2.py`, `catt3.py`. These files are now marked as archived with a short stub; full original copies are preserved in `Pset6/archive/` as `*_original.py`.
  - Updated `Pset6/Makefile` to run only canonical scripts by default.

- `Pset7`:
  - Canonical scripts: `Matrix.py` (numeric eigenvalues) and `Matrix_sympy.py` (symbolic eigenvalues/analysis).
  - `Matrixatt2.py` was archived (preserved in `Pset7/archive`) and replaced with a small stub that instructs users to see archive.
  - Updated `Pset7/Makefile` to run `Matrix.py` and `Matrix_sympy.py`.

- Added tests in `tests/` for `integrator` and `visualizer` modules and a root `Makefile` to run tests, lint, format, and run folder-level tasks.

Why:
- Avoid confusion between alternate attempts (att2) and canonical implementations.
- Make it easier to run folder-specific examples via `make -C <folder> run-all`.
- Keep historical versions safe in `archive/` while keeping the main folder tidy.

How to use:
- Activate your venv and install requirements via `pip install -r requirements.txt`.
- Run the integrator and the visualizer or pset scripts via the folder Makefiles, e.g. `make -C Pset6 run-all`.

Notes:
- If you want archived scripts to be runnable again, run them from `archive/` (they contain full content).
- If you prefer the archived scripts as primary for any task, let me know and I can rename or replace them as canonical.
