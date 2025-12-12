# Phys111-Computational

Lightweight repo for physics computational projects (pendulums, matrices, etc.).

## Structure

- `ComputationalProject/` - canonical utility modules + scripts
  - `integrator.py` - functions to compute pendulum trajectories
  - `visualizer.py` - utilities to load theta CSV and convert to screen positions; includes a Pygame launcher in `__main__`
  - `numericalIntegrator.py` - thin CLI wrapper around `integrator.compute_pendulum_trajectory`
- `Pset6/` - problem set 6 scripts (double pendulum simulations)
- `Pset7/` - matrix algebra and eigenvalue scripts
- `tests/` - pytest tests for `integrator` and `visualizer`

## Quickstart

Create a venv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the integrator and save CSV (or use Makefiles in each folder):

```bash
# Run integrator directly (python must be on PATH and venv activated if used)
python ComputationalProject/numericalIntegrator.py --periods 50 --save theta_theta_dot.csv

# Or use the folder Makefile to run the default integrator behavior
make -C ComputationalProject run-integrator
```

Animate the results (requires a display):

```bash
python ComputationalProject/visualizer.py theta_theta_dot.csv --duration 20
```

Running tests and linting

```bash
# Run tests (requires pytest to be installed in your environment)
make test

# Lint/format (requires flake8 and black installed in your environment)
make lint
make format
```
