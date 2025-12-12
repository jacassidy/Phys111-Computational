.PHONY: lint format run-all run-parta run-partb run-partc clean

lint:
	flake8 Pset5

format:
	black Pset5

run-all: run-parta run-partb run-partc

run-parta:
	python3 Pset5-2.py --part a

run-partb:
	python3 Pset5-2.py --part b

run-partc:
	python3 Pset5-2.py --part c

clean:
	rm -rf figures
