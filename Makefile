UV := uv run --directory scorer

.DEFAULT_GOAL := help
.PHONY: help setup format test

help:
	@echo Targets:
	@echo	setup	- setup python env from uv.lock
	@echo   format  - format and lint python code
	@echo   test    - run pytest

setup:
	uv sync --directory scorer

format:
	$(UV) ruff format .
	$(UV) ruff check --fix .

test:
	$(UV) pytest
