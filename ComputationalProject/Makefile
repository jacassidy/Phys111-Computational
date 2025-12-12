.PHONY: lint format run-integrator run-visualizer run-save figures all
.DEFAULT_GOAL := all

lint:
	@command -v flake8 >/dev/null 2>&1 && flake8 ComputationalProject || echo "flake8 not installed; skipping lint"

format:
	@command -v black >/dev/null 2>&1 && black ComputationalProject || echo "black not installed; skipping format"

run-integrator:
	PYTHONPATH=.. python3 numericalIntegrator.py --periods 50 --save figures/theta_theta_dot.csv --plot --outdir figures

run-visualizer:
	# Run the interactive pygame visualizer (requires display)
	PYTHONPATH=.. python3 visualizer.py figures/theta_theta_dot.csv --duration 20

run-save:
	PYTHONPATH=.. python3 numericalIntegrator.py --periods 50 --save figures/theta_theta_dot.csv

figures: lint format
	mkdir -p figures
	# Generate CSV and a phase-space PNG using the canonical integrator
	PYTHONPATH=.. python3 numericalIntegrator.py --periods 50 --save figures/theta_theta_dot.csv --plot --outdir figures || true
	# Create a static pendulum snapshot (matplotlib) from the CSV
	PYTHONPATH=.. python3 visualizer_static.py figures/theta_theta_dot.csv --out figures/pendulum_static.png

all: figures

clean:
	rm -rf figures
