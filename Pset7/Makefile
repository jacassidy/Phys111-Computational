.PHONY: lint format run-all run-matrix run-matrix-sympy

lint:
	flake8 Pset7

format:
	black Pset7

run-all: run-matrix run-matrix-sympy

run-matrix:
	python3 Matrix.py

run-matrix-sympy:
	python3 Matrix_sympy.py

clean:
	rm -rf figures
