# ComputationalProject Makefile

Running `make` inside this directory will produce PNG visuals in the `figures/` directory:

- `make` (default) runs the integrator, saves a CSV to `figures/theta_theta_dot.csv`, produces a phase-space PNG (e.g., `figures/phase_YYYYMMDD_HHMMSS.png`) and a static pendulum snapshot `figures/pendulum_static.png`.
- `make clean` removes `figures/`.
- `make run-visualizer` launches the interactive pygame visualizer (requires a display).

Notes:
- The Makefile runs `black` and `flake8` if they are available, but will not fail if they are not installed.
- The Makefile sets `PYTHONPATH=..` when running scripts so package imports succeed when invoked from this directory.
