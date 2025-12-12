.PHONY: lint format test run-pset5 run-visual run-pset6 run-pset7

# Provide convenient cross-folder commands that delegate to subfolder Makefiles
lint:
	flake8 .

format:
	black .

test:
	pytest -q

run-pset5:
	python3 Pset5-2.py

run-visual:
	python3 ComputationalProject/numericalIntegrator.py --plot

run-pset6:
	make -C Pset6 run-all

run-pset7:
	make -C Pset7 run-all
