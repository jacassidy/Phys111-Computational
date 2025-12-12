.PHONY: lint format run-all run-6b run-6c run-partcatt4 run-pset6a

lint:
	flake8 Pset6

format:
	black Pset6

run-all: run-6b run-6c run-partcatt4 run-pset6a

run-6b:
	python3 6b.py

run-6c:
	python3 6c.py

## archived scripts are not run by default, use them from `archive/` if needed

run-partcatt4:
	python3 partcatt4.py

run-pset6a:
	python3 Pset6a.py
