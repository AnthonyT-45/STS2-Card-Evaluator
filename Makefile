ifeq ($(OS),Windows_NT)
    SHELL := powershell.exe
    .SHELLFLAGS := -NoProfile -NonInteractive -Command
    RM_DB := if (Test-Path scorer/runs.db) { Remove-Item -Force scorer/runs.db }
else
    SHELL := /bin/sh
    .SHELLFLAGS := -c
    RM_DB := rm -f scorer/runs.db
endif

UV := uv run --directory scorer

.DEFAULT_GOAL := help
.PHONY: help setup format test run reset rebuild view-db

help:
	@echo "Targets:"
	@echo "  setup   - setup python env from uv.lock"
	@echo "  format  - format and lint python code"
	@echo "  test    - run pytest"
	@echo "  run     - build runs.db from fixtures data"
	@echo "  reset   - delete runs.db"
	@echo "  rebuild - delete runs.db and rebuild from scratch"
	@echo "  view-db - view tables within runs.db"

setup:
	uv sync --directory scorer

format:
	$(UV) ruff format .
	$(UV) ruff check --fix .

test:
	$(UV) pytest

run:
	$(UV) python -m spire.main

reset:
	$(RM_DB)

rebuild: reset run

view-db:
	sqlite3 scorer/runs.db
