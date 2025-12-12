.PHONY: lint format run-integrator run-visualizer run-save

lint:
	flake8 ComputationalProject

format:
	black ComputationalProject

run-integrator:
	python3 numericalIntegrator.py --periods 50 --save ../theta_theta_dot.csv

run-visualizer:
	python3 visualizer.py ../theta_theta_dot.csv --duration 20

run-save:
	python3 numericalIntegrator.py --periods 50 --save theta_theta_dot.csv
